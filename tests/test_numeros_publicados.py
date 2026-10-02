"""Trava os números do artigo contra os CSVs de data/ (fonte única).

Cada teste recalcula, a partir de `data/*.csv`, um número que o artigo
"O ChatGPT recusa 'ranking' e entrega 'nota': oito medições e a regra do TSE" publica, e cita
a seção do artigo onde ele aparece. Números que vêm só do texto das fontes (médias publicadas
pelo ITS Rio, datas da Resolução, contagens que o relatório faz em prosa) não derivam da tabela
e ficam fora daqui — o artigo os atribui à fonte.
"""

import ast
import csv
import re
import subprocess
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
PRAZO_DOS_PLANOS = "2026-08-16"  # marco dos planos de conformidade (REGUA.md §2 e §7.2)
DATA_DO_ARTIGO = "2026-10-03"


def ler(nome):
    with open(DATA / nome, newline="") as fh:
        return list(csv.DictReader(fh))


FONTES = ler("fontes.csv")
INSTR = ler("instrumentos.csv")
TABELA = ler("tabela-codificada.csv")
FONTE = {r["fonte"]: r for r in FONTES}


def linhas(**filtro):
    """Linhas da tabela codificada cujos campos batem com todos os pares do filtro."""
    return [r for r in TABELA if all(r[k] == v for k, v in filtro.items())]


def agregados(fonte):
    """Mapa sistema -> (gov, pres) em pct inteiro, dos agregados da fonte."""
    out = {}
    for r in TABELA:
        m = re.fullmatch(rf"{fonte}-agg-(gov|pres)-(.+)", r["id"])
        if m:
            out.setdefault(m[2], {})[m[1]] = int(r["valor_pct"])
    return {s: (v["gov"], v["pres"]) for s, v in out.items()}


def serie(fonte):
    """Mapa sistema -> pct do agregado único da rodada (1ª a 3ª do ITS Rio)."""
    return {
        r["sistema"]: int(r["valor_pct"])
        for r in TABELA
        if r["fonte"] == fonte and r["saida_observada"] == "agregado_pct"
    }


def equipe(autoria):
    """Normaliza a autoria: a 4ª e a 5ª rodadas são do ITS Rio, em parceria com o MPF."""
    return autoria.split(",")[0].split(" (")[0]


# --- Corpus: título, lede e "Cinco jeitos de pedir a mesma coisa" ----------------------------


def test_contagens_gerais():
    assert len(FONTES) == 8  # "oito medições", "oito ondas"
    assert len(INSTR) == 55  # "a lista dos 55 enunciados do corpus"
    assert len(TABELA) == 162  # "162 linhas"
    assert {r["fonte"] for r in TABELA} == set(FONTE)  # toda onda tem linha codificada


def test_quatro_equipes():
    assert {equipe(r["autoria"]) for r in FONTES} == {
        "ITS Rio",
        "Observatório IA nas Eleições",
        "Ekō",
        "JOTA",
    }


def test_mpf_parceiro_na_4a_e_na_5a():
    assert {f for f, r in FONTE.items() if "MPF" in r["autoria"]} == {"ITS4", "ITS5"}


def test_janela_de_coleta_marco_a_agosto():
    assert min(r["coleta_inicio"] for r in FONTES) == "2026-03"
    assert max(r["coleta_fim"] for r in FONTES) == "2026-08-21"  # "respondida até 21 de agosto"
    assert max(r["publicacao"] for r in FONTES) < DATA_DO_ARTIGO  # "já publicadas"


def test_tabela_do_corpus_datas_e_sistemas():
    esperado = {
        "ITS1": ("2026-03", "2026-03", 7),
        "DPBR": ("2026-04-06", "2026-04-10", 5),
        "ITS2": ("2026-05", "2026-05", 7),
        "ITS3": ("2026-06-10", "2026-06-12", 7),
        "EKO": ("2026-06-24", "2026-07-01", 4),
        "ITS4": ("2026-07-02", "2026-07-06", 7),
        "ITS5": ("2026-08-17", "2026-08-21", 7),
        "JOTA": ("2026-08-14", "2026-08-19", 7),
    }
    obtido = {
        f: (r["coleta_inicio"], r["coleta_fim"], len(r["sistemas"].split(";")))
        for f, r in FONTE.items()
    }
    assert obtido == esperado


def test_tabela_do_corpus_enunciados():
    por_fonte = {f: sum(r["fonte"] == f for r in INSTR) for f in FONTE}
    assert por_fonte["ITS1"] == 9
    assert por_fonte["DPBR"] == 14
    assert por_fonte["EKO"] == 25
    assert por_fonte["JOTA"] == 5
    # 4ª e 5ª rodadas: 27 governadores + presidência (6 e 7) + a pergunta das urnas
    gov4, pres4 = (
        int(r["n"]) for r in linhas(id="ITS4-agg-gov-Claude") + linhas(id="ITS4-agg-pres-Claude")
    )
    gov5, pres5 = (
        int(r["n"]) for r in linhas(id="ITS5-agg-gov-Claude") + linhas(id="ITS5-agg-pres-Claude")
    )
    assert gov4 + pres4 + 1 == 34
    assert gov5 + pres5 + 1 == 35


def test_jota_datado_em_duas_faixas():
    jota = linhas(fonte="JOTA")
    cedo = {r["sistema"] for r in jota if r["coleta_inicio"] == "2026-08-14"}
    tarde = {r["sistema"] for r in jota if r["coleta_inicio"] == "2026-08-18"}
    assert cedo == {"Gemini", "Claude", "Copilot", "Meta AI"}  # "14–19 para quatro sistemas"
    assert tarde == {"ChatGPT", "Grok", "Google AI Mode"}  # "18 e 19 de agosto"
    assert {r["coleta_fim"] for r in jota} == {"2026-08-19"}


def test_22_formas_distintas_r1_r4_e_25_com_os_temas_do_jota():
    escada = [
        r
        for r in INSTR
        if r["degrau"] in {"R1", "R2", "R3", "R4"}
        and r["eixo"] == "formulacao"
        and r["inclusao"] == "sim"
    ]
    assert len({r["enunciado"] for r in escada}) == 22
    temas_jota = next(r for r in escada if r["prompt_uid"] == "JOTA-nota-tema")["tema"]
    assert temas_jota == "4 temas"
    assert 22 + (4 - 1) == 25


def test_cinco_degraus_e_quem_submeteu_cada_um():
    formulacao = [r for r in INSTR if r["eixo"] == "formulacao" and r["inclusao"] == "sim"]
    assert {r["degrau"] for r in formulacao} == {"R0", "R1", "R2", "R3", "R4"}
    por_degrau = {}
    for r in formulacao:
        por_degrau.setdefault(r["degrau"], set()).add(equipe(FONTE[r["fonte"]]["autoria"]))
    assert por_degrau["R1"] == {"ITS Rio", "Ekō", "JOTA"}
    assert por_degrau["R2"] == {"ITS Rio", "Ekō"}
    assert por_degrau["R3"] == {"Observatório IA nas Eleições", "JOTA"}
    assert por_degrau["R4"] == {"JOTA"}


# --- Nota metodológica: denominadores ---------------------------------------------------------


def test_denominadores_reconstruidos_e_declarados():
    blocos = {
        (r["fonte"], r["tema"]): (r["n"], r["n_origem"])
        for r in TABELA
        if r["unidade"] == "agregado_bloco"
    }
    assert blocos == {
        ("ITS1", "misto"): ("11", "reconstruido"),
        ("ITS2", "misto"): ("11", "reconstruido"),
        ("ITS3", "misto"): ("16", "reconstruido"),
        ("ITS4", "governador"): ("27", "declarado"),
        ("ITS4", "presidência"): ("6", "reconstruido"),
        ("ITS5", "governador"): ("27", "declarado"),
        ("ITS5", "presidência"): ("7", "reconstruido"),
    }


def test_percentuais_do_its_fecham_com_o_denominador():
    """Todo pct publicado é k/n arredondado para algum k inteiro — com UMA exceção declarada.

    O Claude da 1ª rodada (17%) não fecha com 11 respostas (2/11 = 18%); por isso a nota da
    linha diz que o 11 fecha só 91/82/73%, e o artigo diz "onde a aritmética fecha".
    """
    nao_fecham = {
        r["id"]
        for r in TABELA
        if r["unidade"] == "agregado_bloco"
        and not any(
            round(100 * k / int(r["n"])) == int(r["valor_pct"]) for k in range(int(r["n"]) + 1)
        )
    }
    assert nao_fecham == {"ITS1-agg-Claude"}
    assert "11 fecha 91/82/73%" in linhas(id="ITS1-agg-Claude")[0]["nota"]


# --- "Onde a recusa e a resposta se separam" -------------------------------------------------


def test_recusou_e_ordenou_descrito_pelas_fontes():
    """Três sistemas, duas equipes, abril e julho; a 5ª rodada fica fora por critério declarado."""
    descritas = [
        r
        for r in linhas(postura_declarada="recusou", saida_observada="ordenou_ou_pontuou")
        if r["quem_codificou"] == "fonte" and r["fonte"] != "ITS5"
    ]
    assert {r["sistema"] for r in descritas} == {"Meta AI", "Claude", "Grok"}
    assert {equipe(FONTE[r["fonte"]]["autoria"]) for r in descritas} == {
        "ITS Rio",
        "Observatório IA nas Eleições",
    }
    assert {r["coleta_inicio"][:7] for r in descritas} == {"2026-04", "2026-07"}
    meta = {r["tema"] for r in descritas if r["sistema"] == "Meta AI"}
    assert meta == {"segurança", "educação"}


def test_claude_100_na_4a_e_no_criterio_largo_da_5a():
    assert agregados("ITS4")["Claude"] == (100, 100)
    assert agregados("ITS5")["Claude"] == (100, 100)
    assert linhas(id="ITS5-n-Claude-bloco")[0]["valor_pct"] == "100"


def test_jota_quatro_recusaram_a_nota_mas_compararam():
    recusas = linhas(fonte="JOTA", degrau="R4", postura_declarada="recusou")
    assert {r["sistema"] for r in recusas} == {"Gemini", "Claude", "Copilot", "Meta AI"}
    assert {r["saida_observada"] for r in recusas} == {"nomeou_sem_juizo"}


# --- "O corpus inteiro numa figura" (F5) -----------------------------------------------------


def test_jota_r1_tres_de_tres_recusaram():
    r1 = linhas(fonte="JOTA", degrau="R1")
    assert len(r1) == 3 and all(r["postura_declarada"] == "recusou" for r in r1)


def test_jota_r4_tres_de_sete_pontuaram():
    nota = linhas(fonte="JOTA", prompt_id="nota-tema") + linhas(id="JOTA-nota-Gemini")
    nota += linhas(id="JOTA-nota-Claude") + linhas(id="JOTA-nota-Copilot")
    nota += linhas(id="JOTA-nota-Meta AI")
    por_sistema = {r["sistema"]: r for r in nota}
    assert len(por_sistema) == 7
    pontuaram = {s for s, r in por_sistema.items() if r["saida_observada"] == "ordenou_ou_pontuou"}
    assert pontuaram == {"ChatGPT", "Grok", "Google AI Mode"}


def test_chatgpt_ranking_atendido_em_abril_recusado_em_agosto_nota_atendida():
    assert linhas(id="DPBR-p2-ChatGPT")[0]["juizo"] == "sim"  # abril, "faça um ranking"
    ranking = linhas(id="JOTA-ranking-ChatGPT")[0]
    assert (ranking["degrau"], ranking["postura_declarada"]) == ("R3", "recusou")
    nota = linhas(id="JOTA-nota-tema-ChatGPT")[0]
    assert (nota["degrau"], nota["saida_observada"]) == ("R4", "ordenou_ou_pontuou")
    assert ranking["coleta_inicio"] == nota["coleta_inicio"] == "2026-08-18"


def test_dpbr_r3_cinco_de_cinco_seguranca_e_educacao_quatro_de_cinco_economia():
    def com_juizo(prompt):
        rs = linhas(fonte="DPBR", prompt_id=prompt)
        return sum(r["juizo"] == "sim" for r in rs), len(rs)

    assert com_juizo("p3") == (5, 5)  # segurança
    assert com_juizo("p4") == (5, 5)  # educação
    assert com_juizo("p2") == (4, 5)  # economia


def test_quinta_rodada_gov_pres():
    esperado = {
        "Claude": (100, 100),
        "Meta AI": (100, 100),
        "Perplexity": (100, 100),
        "Grok": (100, 71),
        "ChatGPT": (85, 86),
        "DeepSeek": (78, 71),
        "Gemini": (41, 71),
    }
    assert agregados("ITS5") == esperado


def test_quinta_rodada_media_dos_governadores_86():
    gov = [g for g, _ in agregados("ITS5").values()]
    assert round(sum(gov) / len(gov)) == 86


# --- F6 e a série do ITS Rio -----------------------------------------------------------------


def test_quarta_rodada_gov_pres():
    esperado = {
        "ChatGPT": (100, 67),
        "Claude": (100, 100),
        "Grok": (100, 100),
        "Meta AI": (100, 83),
        "Gemini": (85, 67),
        "DeepSeek": (81, 100),
        "Perplexity": (81, 50),
    }
    assert agregados("ITS4") == esperado


def test_quarta_rodada_nenhuma_barra_abaixo_de_50_e_governadores_entre_81_e_100():
    valores = agregados("ITS4").values()
    assert min(v for par in valores for v in par) == 50
    assert {g for g, _ in valores} <= set(range(81, 101))
    assert 27 * len(agregados("ITS4")) == 189  # "as 189 respostas sobre governador"


def test_julho_para_agosto_nos_governadores():
    j, a = agregados("ITS4"), agregados("ITS5")
    assert (j["Gemini"][0], a["Gemini"][0]) == (85, 41)
    assert (j["ChatGPT"][0], a["ChatGPT"][0]) == (100, 85)
    assert (j["Perplexity"][0], a["Perplexity"][0]) == (81, 100)


def test_perplexity_its5_recomendou_em_31_de_35():
    linhas_p = [
        r
        for r in TABELA
        if r["fonte"] == "ITS5"
        and r["sistema"] == "Perplexity"
        and r["unidade"] == "narrativa_fonte"
    ]
    assert linhas_p and all(r["n"] == "31" for r in linhas_p)
    assert round(100 * 31 / 35) == 89  # o "89%" da Tabela 8 da 5ª rodada


def test_serie_marco_maio_junho():
    esperado = {
        "ChatGPT": (82, 91, 100),
        "Grok": (100, 82, 100),
        "Meta AI": (0, 100, 100),
        "Perplexity": (100, 91, 100),
        "Gemini": (91, 91, 94),
        "Claude": (17, 55, 31),
        "DeepSeek": (73, 36, 31),
    }
    s1, s2, s3 = serie("ITS1"), serie("ITS2"), serie("ITS3")
    assert {k: (s1[k], s2[k], s3[k]) for k in s1} == esperado
    medias = tuple(round(sum(s.values()) / len(s)) for s in (s1, s2, s3))
    assert medias == (66, 78, 79)  # linha "média" da tabela do artigo


# --- "Por que agora" (F8) --------------------------------------------------------------------


def test_so_duas_coletas_depois_do_prazo_dos_planos():
    depois = {f for f, r in FONTE.items() if r["coleta_fim"] > PRAZO_DOS_PLANOS}
    assert depois == {"ITS5", "JOTA"}


def test_marcos_da_linha_do_tempo():
    def mes(r):
        return r["coleta_inicio"][:7]

    mar_abr = {f for f, r in FONTE.items() if mes(r) in {"2026-03", "2026-04"}}
    mai_jul = {
        f
        for f, r in FONTE.items()
        if mes(r) in {"2026-05", "2026-06", "2026-07"} and r["coleta_fim"] <= PRAZO_DOS_PLANOS
    }
    assert mar_abr == {"ITS1", "DPBR"}
    assert mai_jul == {"ITS2", "ITS3", "EKO", "ITS4"}  # "maio a julho: quatro ondas"
    rodadas = sorted(f for f in FONTE if f.startswith("ITS"))
    assert [FONTE[f]["coleta_inicio"][:7] for f in rodadas] == [
        "2026-03",
        "2026-05",
        "2026-06",
        "2026-07",
        "2026-08",
    ]  # "cinco rodadas em seis meses"


# --- Travas e gate ---------------------------------------------------------------------------


def test_trava4_sem_nome_de_candidato():
    texto = (DATA / "checar-tabela.py").read_text()
    nomes = next(
        ast.literal_eval(n.value)
        for n in ast.parse(texto).body
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "NOMES"
    )
    assert len(nomes) > 20
    for r in TABELA:
        for campo in ("ancora", "nota"):
            for nome in nomes:
                assert nome.lower() not in r[campo].lower(), (r["id"], campo, nome)


def test_gate_sem_ancoras_sai_zero():
    res = subprocess.run(
        [sys.executable, str(DATA / "checar-tabela.py"), "--sem-ancoras"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert "APROVADO" in res.stdout


def test_gate_reprova_tabela_adulterada(tmp_path):
    """Teste negativo: um enumerado fora da régua tem de derrubar o gate."""
    for nome in ("fontes.csv", "instrumentos.csv"):
        (tmp_path / nome).write_bytes((DATA / nome).read_bytes())
    texto = (DATA / "tabela-codificada.csv").read_text()
    alvo = ",ordenou_ou_pontuou,"
    assert alvo in texto
    (tmp_path / "tabela-codificada.csv").write_text(texto.replace(alvo, ",ordenou_talvez,", 1))
    res = subprocess.run(
        [sys.executable, str(DATA / "checar-tabela.py"), "--dir", str(tmp_path), "--sem-ancoras"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 1, res.stdout + res.stderr
