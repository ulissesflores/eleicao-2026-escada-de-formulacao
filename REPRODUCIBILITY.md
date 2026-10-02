# Reprodutibilidade

O repositório tem dois selos, com garantias diferentes. Os dois estão aqui para que o leitor
saiba exatamente o que pode refazer sozinho e o que depende de material de terceiros.

## Selo 1 — derivação reproduzível (roda em qualquer máquina, sem rede)

O que é re-executável sem as fontes:

- o gate `data/checar-tabela.py`: enumerados da régua, derivação de `juizo` a partir de
  `saida_observada`, datas, ids, coerência entre instrumentos e tabela, e a trava 4 (nenhum nome
  de candidato em âncora ou nota da tabela codificada);
- os testes de `tests/`, que travam cada número do artigo derivado da tabela;
- o selo `output/provenance.json`: `chain_hash` SHA-256 encadeado sobre a régua, os três CSVs, o
  gate, os testes e `run_all.py`.

```bash
python3 -m pip install -r requirements.txt
python3 run_all.py
```

Sem a pasta `fontes/`, o `run_all.py` roda o gate com `--sem-ancoras` e **diz isso na saída**:
enumerados, derivações e números ficam verificados; a conferência texto-a-texto das âncoras, não.

## Selo 2 — evidência congelada, não redistribuída

A tabela codifica relatórios de terceiros. As cópias em texto desses relatórios são dos autores
e não estão neste repositório (`fontes/` está no `.gitignore`). Para conferir as âncoras, recrie
cada cópia com o nome exato da coluna `arquivo_local` de `data/fontes.csv`, dentro de `fontes/`
na raiz do repositório (ao lado de `data/`):

| Fonte | Documento (coluna `url`) | Como extrair | Arquivo em `fontes/` |
|---|---|---|---|
| ITS1 | PDF da 1ª rodada | `pdftotext -layout` | `boca-de-ia-itsrio.txt` |
| ITS2 | PDF da 2ª rodada | `pdftotext -layout` | `bocadeia-r2-maio.txt` |
| ITS3 | PDF da 3ª rodada | `pdftotext -layout` | `bocadeia-r3-junho.txt` |
| ITS4 | PDF da 4ª rodada (versão corrigida de 13/08) | `pdftotext -layout` | `bocadeia-r4-julho-governamental.txt` |
| ITS5 | PDF da 5ª rodada (v2, de 17/09) | MinerU, backend `pipeline` | `mineru_out/bocadeia-r5-wix/auto/bocadeia-r5-wix.md` |
| DPBR | PDF do Observatório IA nas Eleições | `pdftotext -layout` | `dpbr-alafia-ei-chat.txt` |
| EKO | PDF da Ekō | `pdftotext -layout` | `eko-artificial-hallucinations.txt` |
| JOTA | reportagem (página renderizada por JavaScript) | texto da página via `https://r.jina.ai/<url>` | `jota-ranking-2026-08-21.jina.md` |

Passo a passo:

```bash
mkdir -p fontes
# um PDF por vez, com a URL da coluna `url` de data/fontes.csv:
curl -sL -o its1.pdf "<url de ITS1>"
pdftotext -layout its1.pdf fontes/boca-de-ia-itsrio.txt
# ... idem para ITS2, ITS3, ITS4, DPBR e EKO

# ITS5 (MinerU 3.x; gera a árvore mineru_out/<nome>/auto/<nome>.md):
curl -sL -o bocadeia-r5-wix.pdf "<url de ITS5>"
mineru -p bocadeia-r5-wix.pdf -o fontes/mineru_out -b pipeline

# JOTA:
curl -sL "https://r.jina.ai/<url de JOTA>" -o fontes/jota-ranking-2026-08-21.jina.md

# confira cada hash contra a coluna sha256 de data/fontes.csv:
shasum -a 256 fontes/boca-de-ia-itsrio.txt

python3 run_all.py   # com fontes/ completa: "run_all: OK [com ancoras (fontes/ completa)]"
```

Versões usadas na extração selada: `pdftotext` 26.09.0 (Poppler) e MinerU 3.4.5, backend
`pipeline`. Com o `pdftotext` 26.09.0, a recriação das seis cópias em `-layout` a partir dos
PDFs arquivados reproduziu os seis `sha256` de `data/fontes.csv` byte a byte (conferido em
2026-10-02).

> [!WARNING]
> Versões diferentes do extrator (`pdftotext`, MinerU) ou um proxy que mude a formatação da
> página do JOTA podem mudar o texto, logo o `sha256` e o número da linha. Por isso cada âncora
> tem folga de ±8 linhas e é comparada com espaços em branco colapsados. Hash divergente com
> âncoras conferindo indica extração diferente, não adulteração; **âncora que não confere é o
> sinal real**. O editor também pode trocar o PDF na mesma URL; quando houve mais de uma
> versão publicada, a coluna `titulo` de `data/fontes.csv` diz qual foi a codificada.

## O que não é re-executável

Nenhuma coleta de resposta de IA foi feita aqui. Os percentuais são dos relatórios; onde o
denominador não é declarado e a aritmética fecha, ele foi reconstruído e a linha diz isso
(`n_origem = reconstruido`). Os assistentes mudam de comportamento ao longo do tempo: a tabela
descreve o que foi publicado sobre coletas feitas até 21/08/2026, não a conduta atual de
nenhum sistema.
