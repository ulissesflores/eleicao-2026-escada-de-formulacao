#!/usr/bin/env python3
"""Gate da tabela codificada de `ia-eleicao-2026`.

Reprova (exit 1) se qualquer linha de `tabela-codificada.csv` ou `instrumentos.csv`:
  1. usar valor fora dos enumerados da REGUA.md (degrau, eixo, postura, saída, unidade, quem);
  2. tiver `juizo` diferente do derivado de `saida_observada` (§ 4.2 da régua);
  3. citar `fonte` ausente de `fontes.csv`, ou `prompt_id` de instrumento excluído;
  4. citar `arquivo` inexistente, ou `ancora` que não apareça a até FOLGA linhas de `linha`
     (comparação com espaços em branco colapsados; a âncora pode atravessar quebra de linha);
  5. carregar data fora de AAAA-MM ou AAAA-MM-DD, ou coleta_fim < coleta_inicio;
  6. repetir `id` / `prompt_uid`;
  7. ter `n_origem` sem `n`, ou `valor_pct` fora de 0..100;
  8. (trava 4) carregar em `ancora`/`nota` da TABELA CODIFICADA um sobrenome da lista de
     candidatos do corpus. `instrumentos.csv` fica de fora de propósito: prompt publicado é
     instrumento, não saída de modelo (REGUA §6).

Uso: python3 checar-tabela.py [--dir <pasta codificacao>] [--sem-ancoras]
  --sem-ancoras: pula a regra 4 (e a existência dos arquivos locais) quando as cópias em texto das
  fontes não estão ao lado — elas não são redistribuídas, o texto é dos autores. O resto vale igual.
Teste negativo (obrigatório antes de confiar no gate): alterar uma âncora e confirmar exit 1.
"""
import csv, pathlib, re, sys

AQUI = pathlib.Path(__file__).resolve().parent
DIR = pathlib.Path(sys.argv[sys.argv.index('--dir') + 1]) if '--dir' in sys.argv else AQUI
FONTES_DIR = DIR.parent / 'fontes'
FOLGA = 8
SEM_ANCORAS = '--sem-ancoras' in sys.argv

DEGRAU = {'R0', 'R1', 'R2', 'R3', 'R4', 'R0-R2', 'R1-R2', 'P', 'fora'}
EIXO = {'formulacao', 'persona', 'fora', 'confianca_institucional', 'perfil_de_candidato', 'desinformacao', 'logistica'}
POSTURA = {'aceitou', 'recusou', 'nao_reportada'}
SAIDA_JUIZO = {'ordenou_ou_pontuou': 'sim', 'recomendou_ou_sugeriu': 'sim', 'nomeou_sem_juizo': 'nao',
               'nao_nomeou': 'nao', 'sem_juizo_nao_detalhado': 'nao', 'agregado_pct': 'pct',
               'nao_reportada': 'nao_reportado'}
UNIDADE = {'agregado_bloco', 'resposta_verbatim', 'narrativa_fonte'}
QUEM = {'fonte', 'redacao'}
N_ORIGEM = {'', 'declarado', 'reconstruido'}
DATA = re.compile(r'^\d{4}-\d{2}(-\d{2})?$')
# trava 4: nenhum destes sobrenomes/apelidos pode aparecer em âncora ou nota da tabela codificada
NOMES = ['Lula', 'Bolsonaro', 'Caiado', 'Zema', 'Tarcísio', 'Tarcisio', 'Renan Santos', 'Rebelo', 'Daciolo',
         'Cury', 'Ratinho', 'Eduardo Leite', 'Ciro', 'Boulos', 'Haddad', 'Michelle', 'Elmano', 'Edmilson',
         'Rui Costa', 'Van Hattem', 'Zucco', 'Girão', 'Cavalcanti', 'Thabatta', 'Edna Sampaio', 'Samara', 'Hertz']

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

_cache = {}
def janela(arquivo, linha):
    if SEM_ANCORAS:
        return 'ok'
    if arquivo not in _cache:
        p = FONTES_DIR / arquivo
        if not p.exists():
            return None
        _cache[arquivo] = p.read_text(errors='replace').split('\n')  # split('\n'), não splitlines(): o pdftotext põe \f entre páginas e splitlines() quebraria neles, desalinhando a linha citada da linha do editor
    ls = _cache[arquivo]
    lo, hi = max(0, linha - 1 - FOLGA), min(len(ls), linha + FOLGA)
    return norm(' '.join(ls[lo:hi]))

def ler(nome):
    with open(DIR / nome, newline='') as fh:
        return list(csv.DictReader(fh))

erros = []
def erro(msg):
    erros.append(msg)

fontes = {r['fonte']: r for r in ler('fontes.csv')}
for r in fontes.values():
    if not SEM_ANCORAS and not (FONTES_DIR / r['arquivo_local']).exists():
        erro(f"fontes.csv {r['fonte']}: arquivo local ausente {r['arquivo_local']}")
    for c in ('coleta_inicio', 'coleta_fim', 'publicacao'):
        if not DATA.match(r[c]):
            erro(f"fontes.csv {r['fonte']}: data inválida em {c}: {r[c]!r}")

instrumentos = ler('instrumentos.csv')
uids, incluidos = set(), {}
for r in instrumentos:
    if r['prompt_uid'] in uids:
        erro(f"instrumentos.csv: prompt_uid repetido {r['prompt_uid']}")
    uids.add(r['prompt_uid'])
    if r['fonte'] not in fontes:
        erro(f"instrumentos.csv {r['prompt_uid']}: fonte desconhecida {r['fonte']}")
    if r['degrau'] not in DEGRAU:
        erro(f"instrumentos.csv {r['prompt_uid']}: degrau inválido {r['degrau']!r}")
    if r['eixo'] not in EIXO:
        erro(f"instrumentos.csv {r['prompt_uid']}: eixo inválido {r['eixo']!r}")
    if r['inclusao'] not in ('sim', 'nao'):
        erro(f"instrumentos.csv {r['prompt_uid']}: inclusao inválida {r['inclusao']!r}")
    if r['inclusao'] == 'nao' and not r['motivo_exclusao']:
        erro(f"instrumentos.csv {r['prompt_uid']}: excluído sem motivo")
    if (r['inclusao'] == 'sim') != (r['degrau'] != 'fora'):
        erro(f"instrumentos.csv {r['prompt_uid']}: inclusao {r['inclusao']} incoerente com degrau {r['degrau']}")
    incluidos.setdefault(r['fonte'], {})[r['prompt_id']] = r['degrau']
    jan = janela(r['arquivo'], int(r['linha']))
    if jan is None:
        erro(f"instrumentos.csv {r['prompt_uid']}: arquivo ausente {r['arquivo']}")
    elif not SEM_ANCORAS and norm(r['ancora']) not in jan:
        erro(f"instrumentos.csv {r['prompt_uid']}: âncora não encontrada a ±{FOLGA} linhas de {r['arquivo']}:{r['linha']}: {r['ancora']!r}")

tabela = ler('tabela-codificada.csv')
ids = set()
for r in tabela:
    i = r['id']
    if i in ids:
        erro(f"tabela: id repetido {i}")
    ids.add(i)
    if r['fonte'] not in fontes:
        erro(f"tabela {i}: fonte desconhecida {r['fonte']}")
    if r['degrau'] not in DEGRAU or r['degrau'] == 'fora':
        erro(f"tabela {i}: degrau inválido {r['degrau']!r}")
    if r['eixo'] not in ('formulacao', 'persona'):
        erro(f"tabela {i}: eixo inválido {r['eixo']!r}")
    if r['eixo'] == 'persona' and not r['persona']:
        erro(f"tabela {i}: eixo persona sem campo persona")
    if r['postura_declarada'] not in POSTURA:
        erro(f"tabela {i}: postura inválida {r['postura_declarada']!r}")
    if r['saida_observada'] not in SAIDA_JUIZO:
        erro(f"tabela {i}: saída inválida {r['saida_observada']!r}")
    elif r['juizo'] != SAIDA_JUIZO[r['saida_observada']]:
        erro(f"tabela {i}: juizo {r['juizo']!r} não deriva de saída {r['saida_observada']!r}")
    if r['unidade'] not in UNIDADE:
        erro(f"tabela {i}: unidade inválida {r['unidade']!r}")
    if r['quem_codificou'] not in QUEM:
        erro(f"tabela {i}: quem_codificou inválido {r['quem_codificou']!r}")
    if r['n_origem'] not in N_ORIGEM:
        erro(f"tabela {i}: n_origem inválido {r['n_origem']!r}")
    if r['n_origem'] and not r['n']:
        erro(f"tabela {i}: n_origem sem n")
    if r['n'] and not r['n'].isdigit():
        erro(f"tabela {i}: n não numérico {r['n']!r}")
    if r['saida_observada'] == 'agregado_pct' and r['unidade'] != 'agregado_bloco':
        erro(f"tabela {i}: agregado_pct exige unidade agregado_bloco")
    if r['valor_pct']:
        try:
            v = float(r['valor_pct'])
            if not 0 <= v <= 100:
                raise ValueError
        except ValueError:
            erro(f"tabela {i}: valor_pct fora de 0..100: {r['valor_pct']!r}")
    elif r['saida_observada'] == 'agregado_pct':
        erro(f"tabela {i}: agregado sem valor_pct")
    for c in ('coleta_inicio', 'coleta_fim'):
        if not DATA.match(r[c]):
            erro(f"tabela {i}: data inválida em {c}: {r[c]!r}")
    if r['coleta_fim'] < r['coleta_inicio']:
        erro(f"tabela {i}: coleta_fim antes de coleta_inicio")
    # cada prompt_id da linha tem de existir nos instrumentos INCLUÍDOS da fonte (ids compostos separados por vírgula)
    pids = [p.strip() for p in re.split(r'[,;]', r['prompt_id'].split(' (')[0]) if p.strip()]
    for p in pids:
        base = re.sub(r'\s.*$', '', p)
        base = re.sub(r'^p4\.\d+(-p4\.\d+)?$', 'p4', base)
        base = re.sub(r'^p1-p7$', 'p1', base)
        base = 'p1' if base == 'todas' else base
        # rodadas do ITS Rio herdam os prompts da 1ª; a rodada que renumera (5ª: p8 = meio ambiente) sobrepõe os seus
        alvo = ({**incluidos.get('ITS1', {}), **incluidos.get(r['fonte'], {})} if r['fonte'].startswith('ITS')
                else incluidos.get(r['fonte'], {}))
        if base not in alvo:
            erro(f"tabela {i}: prompt_id {p!r} não é instrumento incluído de {r['fonte']}")
        elif alvo[base] == 'fora':
            erro(f"tabela {i}: prompt_id {p!r} está excluído nos instrumentos")
    jan = janela(r['arquivo'], int(r['linha']))
    if jan is None:
        erro(f"tabela {i}: arquivo ausente {r['arquivo']}")
    elif not SEM_ANCORAS and norm(r['ancora']) not in jan:
        erro(f"tabela {i}: âncora não encontrada a ±{FOLGA} linhas de {r['arquivo']}:{r['linha']}: {r['ancora']!r}")
    for campo in ('ancora', 'nota'):
        for nome in NOMES:
            if nome.lower() in r[campo].lower():
                erro(f"tabela {i}: trava 4 — nome de candidato em {campo}: {nome!r}")

print(f"fontes {len(fontes)} · instrumentos {len(instrumentos)} · linhas codificadas {len(tabela)}")
if erros:
    print(f"REPROVADO — {len(erros)} erro(s):")
    for e in erros:
        print('  -', e)
    sys.exit(1)
print("APROVADO — enums, derivação de juizo, datas, ids, instrumentos" + ("; ÂNCORAS NÃO CONFERIDAS (--sem-ancoras)" if SEM_ANCORAS else " e âncoras conferem") + "; trava 4 limpa.")
