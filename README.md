<div align="center">

# Escada de formulação

### Régua, tabela codificada e gate de oito medições sobre IA e voto no Brasil (2026)

**Pedido com a palavra "ranking", o ChatGPT não respondeu; pedido com "nota", deu notas de 0 a
10 aos candidatos e os ordenou. Este repositório reorganiza oito medições publicadas pela forma
do pedido — e deixa cada linha conferível contra a página do relatório de onde ela saiu.**

[![Licença do código: Apache 2.0](https://img.shields.io/badge/c%C3%B3digo-Apache--2.0-blue.svg)](LICENSES/Apache-2.0.txt)
[![Licença dos dados: CC BY 4.0](https://img.shields.io/badge/r%C3%A9gua%20e%20tabelas-CC--BY--4.0-lightgrey.svg)](LICENSES/CC-BY-4.0.txt)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Dependências: só pytest](https://img.shields.io/badge/depend%C3%AAncias-s%C3%B3_pytest-brightgreen.svg)](requirements.txt)
[![Testes: 30 passando](https://img.shields.io/badge/testes-30_passando-brightgreen.svg)](tests/)
[![Reproduzível: cadeia SHA-256](https://img.shields.io/badge/reproduz%C3%ADvel-cadeia_SHA--256-blueviolet.svg)](output/hash-chain.md)
[![CI](https://github.com/ulissesflores/eleicao-2026-escada-de-formulacao/actions/workflows/ci.yml/badge.svg)](https://github.com/ulissesflores/eleicao-2026-escada-de-formulacao/actions/workflows/ci.yml)

</div>

> [!IMPORTANT]
> **Achado.** Quatro equipes independentes, cada uma com instrumento próprio, publicaram oito
> ondas de coleta, de março a agosto de 2026, sobre o que os assistentes de IA de consumo
> respondem quando o eleitor pede juízo sobre candidatos. Acima do pedido de informação (R0), os
> **22 enunciados distintos de pedido de juízo** sobem uma escada de quatro degraus — de "em quem
> devo votar" (R1) a "dê uma nota para as propostas" (R4) —, e o resultado acompanha o
> **verbo**, não o tema nem quem pergunta. No teste do JOTA de 18–19/08/2026, o ChatGPT "não
> respondeu" ao pedido com o termo "ranking" e, com "nota", deu notas de 0 a 10 e ordenou os
> candidatos. Na 5ª rodada do ITS Rio (17–21/08), o relatório ainda contou ranqueamento, pelo seu
> critério largo, em **86%** das respostas sobre governadores e em 86% das sobre a presidência.

Este é o pacote de reprodução do artigo
**[Os termos de uso impedem até medir se a IA cumpre a lei eleitoral](https://ulissesflores.com/artigos/ia-eleicao-2026)**
(Carlos Ulisses Flores, 2026). Todo número do artigo que sai da tabela é recalculado pelos
testes a partir dos CSVs deste repositório.

> *In English:* reproduction package for a Portuguese-language article that re-reads eight
> published Brazilian audits (March–August 2026) of consumer AI assistants asked to judge
> election candidates, recoded along one axis — how the request is phrased — against the
> Electoral Court (TSE) rule that bars AI providers from ranking or recommending candidates
> "even when the user asks". No new measurement was made. Coding rubric, coded tables, a
> validating gate, tests that lock every table-derived number in the article, and a SHA-256
> provenance seal. Data and documentation are in Portuguese.

---

## O que este repositório contribui

1. **Uma régua escrita antes da tabela.** [`REGUA.md`](REGUA.md) fixa os critérios de
   inclusão de uma fonte, os cinco degraus de formulação (R0 a R4) e a codificação do desfecho
   em **dois campos** — o que a resposta *diz* que vai fazer (`postura_declarada`) e o que ela
   *faz* com os candidatos (`saida_observada`). É essa separação que mostra a célula
   "recusou e ordenou", que uma contagem de recusas esconde.
2. **Uma tabela auditável linha a linha.** Cada uma das 162 linhas de
   [`data/tabela-codificada.csv`](data/tabela-codificada.csv) aponta o arquivo, a linha e um
   trecho verbatim da fonte; o gate [`data/checar-tabela.py`](data/checar-tabela.py) reprova a
   linha cuja âncora não está lá, o enumerado fora da régua, o juízo incoerente com a saída e
   qualquer nome de candidato na tabela.
3. **Números do artigo como asserções.** [`tests/`](tests/) recalcula a partir dos CSVs cada
   número que o artigo e suas figuras tiram da tabela. Texto e dado não divergem sem o CI
   ficar vermelho; um selo SHA-256 encadeado prova que os arquivos são os que produziram o
   artigo.

## Em resumo

| | |
|---|---|
| **Pergunta** | A salvaguarda que o art. 28, § 1º-C da Res. TSE 23.610/2019 exige dos provedores de IA está presa à palavra usada no pedido? |
| **Corpus** | 8 ondas de coleta publicadas (ITS Rio, 5 rodadas — a 4ª e a 5ª com o MPF; Observatório IA nas Eleições; Ekō; JOTA), março a agosto de 2026 |
| **Tabela** | 8 fontes · 55 enunciados (30 na escada, 25 excluídos com motivo) · 162 linhas codificadas · 22 enunciados distintos de pedido de juízo (25 contando um a um os quatro temas do JOTA) |
| **Eixo** | a forma do pedido: R0 informação -> R1 voto -> R2 "o melhor" -> R3 ranking -> R4 nota |
| **Dependências** | Python 3.11+ e a biblioteca padrão; `pytest` só para os testes |
| **Rede** | Nenhuma para rodar; só para recriar as cópias das fontes e conferir as âncoras |
| **O que não é** | Medição própria. Nada aqui diz como os assistentes se comportam hoje — ver [O que é e o que não é afirmado](#o-que-é-e-o-que-não-é-afirmado) |

## Como rodar

```bash
git clone https://github.com/ulissesflores/eleicao-2026-escada-de-formulacao.git
cd eleicao-2026-escada-de-formulacao
python3 -m pip install -r requirements.txt
python3 run_all.py
```

Saída esperada num clone limpo (sem a pasta `fontes/`, que não é redistribuída):

```text
ATENCAO: fontes/ ausente; gate em modo --sem-ancoras, ANCORAS NAO CONFERIDAS.

=== 1/3 gate da tabela (SEM ancoras) ===
fontes 8 · instrumentos 55 · linhas codificadas 162
APROVADO — enums, derivação de juizo, datas, ids, instrumentos; ÂNCORAS NÃO CONFERIDAS (--sem-ancoras); trava 4 limpa.

=== 2/3 pytest ===
..............................                                           [100%]
30 passed in 0.09s

=== 3/3 proveniencia ===
proveniencia verificada: chain_hash fc485b271d810acc3a5b871070800b33a93fca8c214735c3c7de3df38f671725

run_all: OK [SEM ancoras]
```

O aviso da primeira linha é deliberado: sem as cópias em texto dos relatórios, o gate confere
tudo menos as âncoras, e diz isso. Para conferir as âncoras contra as fontes originais,
siga [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) — com `fontes/` completa, a última linha passa
a ser `run_all: OK [com ancoras (fontes/ completa)]`.

## Resultados

A escada, com os enunciados e o que cada degrau devolveu, está no artigo. Os números
por sistema que mais mudaram entre julho e agosto são os do ITS Rio — percentual de respostas
com ranqueamento pelo critério largo do relatório (inclui destaque e omissão), governadores
(27 UFs) / presidência:

| Sistema | 4ª rodada (2–6/07) gov / pres | 5ª rodada (17–21/08) gov / pres |
|---|---|---|
| ChatGPT | 100 / 67 | 85 / 86 |
| Claude | 100 / 100 | 100 / 100 |
| DeepSeek | 81 / 100 | 78 / 71 |
| Gemini | 85 / 67 | 41 / 71 |
| Grok | 100 / 100 | 100 / 71 |
| Meta AI | 100 / 83 | 100 / 100 |
| Perplexity | 81 / 50 | 100 / 100 |

Os percentuais são os publicados pelo ITS Rio (Tabela 2 da 4ª rodada; Tabela 9 da v2 da 5ª) e
cada um é uma asserção em [`tests/`](tests/). O relatório também publica as médias dos sete
sistemas — 93% (governadores) e 81% (presidência) na 4ª rodada, 86% e 86% na 5ª —, que não são
recalculadas aqui. O 27 dos governadores é declarado (uma pergunta por estado); os
denominadores da presidência, 6 na 4ª rodada e 7 na 5ª, foram reconstruídos pela aritmética e
estão marcados `n_origem = reconstruido`. A 4ª rodada declara que não compara médias com as
anteriores; a comparação julho -> agosto é leitura do artigo, não do relatório.

## Como ler os dados

- **`instrumentos.csv` reproduz prompts de terceiros**, como citação e atribuídos às equipes que
  os publicaram — inclusive as perguntas de desinformação da Ekō que nomeiam candidatos. São
  instrumentos de teste dessas equipes, não afirmações deste repositório (REGUA.md §6). Dois
  enunciados do JOTA não são verbatim: `JOTA-voto` é string parcial e `JOTA-ranking` descreve um
  pedido cujo texto a reportagem não publicou; a coluna `enunciado` diz isso.
- **`quem_codificou`**: `fonte` quando o desfecho é o que o relatório afirma; `redacao` quando é
  leitura do autor do artigo sobre uma resposta publicada na íntegra (REGUA.md §5).
- **`fontes.csv`, coluna `publicacao`**: data do documento codificado, não necessariamente a da
  divulgação. 1ª rodada e Observatório: data dos metadados do PDF; 2ª e 3ª rodadas: 29/07/2026,
  data dos arquivos no servidor (cabeçalho `Last-Modified`); 4ª e 5ª: data da versão codificada
  (a 5ª foi divulgada pelo MPF em 25/09/2026); Ekō e JOTA: data impressa na página.
- **"recusou"** é codificação: a régua chama de recusa a resposta que declara não atender. No
  JOTA, a reportagem diz que o ChatGPT "não respondeu" ao pedido com "ranking".

## O que é e o que não é afirmado

**Afirmado.** A releitura é reproduzível a partir da régua e dos CSVs; cada linha da tabela
tem evidência verbatim na fonte, conferível pelo gate; cada número do artigo derivado da
tabela é uma asserção em [`tests/`](tests/).

**Não afirmado.** Nenhuma medição própria foi feita: são oito ondas publicadas, relidas. Os
percentuais são das fontes. A tabela não diz que algum provedor *violou* a Resolução — isso
cabe à Justiça Eleitoral; ela registra o que foi publicado como resposta. Nada aqui estima a
conduta atual de nenhum sistema: a última coleta do corpus é de 21/08/2026.

**Congelado.** As cópias em texto dos relatórios ficam fora do repositório (o texto é dos
autores); a tabela guarda só âncoras curtas, valores e URLs. A tabela também não carrega o
nome de nenhum candidato nem a ordem de nenhum ranking: quem precisar da ordem abre o PDF na
página citada.

## Integridade

Um único `chain_hash` SHA-256 encadeado sela a régua, os três CSVs, o gate, os testes e
`run_all.py`:

```text
fc485b271d810acc3a5b871070800b33a93fca8c214735c3c7de3df38f671725
```

```bash
python3 make_provenance.py --verify
```

Os hashes por arquivo estão em [`output/hash-chain.md`](output/hash-chain.md). O contrato de
reprodução — o que se refaz sem rede e o que depende das fontes — está em
[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Estrutura

```text
README.md                    este arquivo
REGUA.md                     régua de codificação (escrita antes da tabela)
data/fontes.csv              8 fontes: datas de coleta, URL, superfície, sha256 da cópia em texto
data/instrumentos.csv        55 enunciados, com degrau, eixo e motivo de exclusão
data/tabela-codificada.csv   162 linhas codificadas, cada uma com arquivo, linha e âncora
data/checar-tabela.py        o gate (o mesmo arquivo que produziu a tabela do artigo)
tests/                       números do artigo como asserções
run_all.py                   entry-point único: gate -> testes -> selo
make_provenance.py           gera e confere (--verify) o selo SHA-256
output/                      provenance.json e hash-chain.md
REPRODUCIBILITY.md           como recriar fontes/ e conferir as âncoras
ROADMAP.md                   próximas versões possíveis, com o gatilho de cada uma
CHANGELOG.md                 histórico de versões
CITATION.cff, codemeta.json  metadados de citação legíveis por máquina
.zenodo.json                 metadados do depósito no Zenodo
LICENSE, LICENSES/, NOTICE   Apache-2.0 (código), CC BY 4.0 (régua, tabelas, documentação)
pyproject.toml               configuração de lint (ruff), docstrings (interrogate) e pytest
requirements.txt, .lock      pytest (só para os testes) e as versões usadas na verificação
.github/workflows/ci.yml     CI: selo, replicação em Python 3.11 e 3.12, lint
fontes/                      NÃO versionada: cópias em texto dos relatórios (você recria)
```

O que pode vir depois — a 6ª rodada do ITS Rio, se sair, e outros candidatos — está em
[`ROADMAP.md`](ROADMAP.md).

## Autor

**Carlos Ulisses Flores**

[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--6034--7765-a6ce39.svg)](https://orcid.org/0000-0002-6034-7765)
[![Website](https://img.shields.io/badge/Website-ulissesflores.com-1f6feb.svg)](https://ulissesflores.com)
[![Lattes](https://img.shields.io/badge/Lattes-6905246706890561-2b7489.svg)](http://lattes.cnpq.br/6905246706890561)

Se uma linha da tabela estiver errada, abra uma
[issue](https://github.com/ulissesflores/eleicao-2026-escada-de-formulacao/issues) citando o
`id` da linha: eu corrijo, credito e registro no [`CHANGELOG.md`](CHANGELOG.md). Se você
discordar de uma linha, discorde de uma regra escrita — é para isso que a régua está lá.

## Como citar

```bibtex
@software{flores_escada_de_formulacao_2026,
  author  = {Flores, Carlos Ulisses},
  title   = {Escada de formula{\c{c}}{\~a}o: r{\'e}gua, tabela codificada e gate de oito
             medi{\c{c}}{\~o}es sobre {IA} e voto no {Brasil} (2026)},
  year    = {2026},
  version = {1.0.0},
  url     = {https://github.com/ulissesflores/eleicao-2026-escada-de-formulacao}
}
```

O DOI do Zenodo é cunhado na primeira release do GitHub. Quando existir, cite o **DOI de
conceito** — que sempre resolve para a versão mais recente —; cada release ganha também um
DOI de versão, para quando for preciso apontar uma versão específica. Metadados legíveis por
máquina: [`CITATION.cff`](CITATION.cff) e [`codemeta.json`](codemeta.json).

## Licença

Licença dupla. Código (`run_all.py`, `make_provenance.py`, `data/checar-tabela.py`, `tests/`)
sob **Apache-2.0** ([`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)); régua, tabelas e
documentação sob **CC BY 4.0** ([`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt)). Os
relatórios de origem são de seus autores e não são redistribuídos — ver [`NOTICE`](NOTICE).

## Referências

- ITS Rio, [*Boca de IA*, 1ª rodada](https://itsrio.org/wp-content/uploads/2017/01/Boca-de-IA.pdf) (coleta em março de 2026, publicada em 15/04/2026)
- ITS Rio, [*Boca de IA*, 2ª rodada](https://www.bocadeia.com.br/_files/ugd/6dff39_95b3073654734a529db561c79e66516e.pdf) (maio de 2026)
- ITS Rio, [*Boca de IA*, 3ª rodada](https://www.bocadeia.com.br/_files/ugd/6dff39_c408fd0ea61d49d686bae9bf95959baf.pdf) (10–12/06/2026)
- ITS Rio e MPF, [*Boca de IA*, 4ª rodada, versão corrigida de 13/08/2026](https://www.bocadeia.com.br/_files/ugd/6dff39_dc906ae8680b4b30af8493dae8a2706b.pdf) (2–6/07/2026)
- ITS Rio e MPF, [*Relatório Boca de IA — 5ª Edição*, versão de 17/09/2026](https://www.bocadeia.com.br/_files/ugd/6dff39_e2da7ee562784c4e9c894e36a4b8564f.pdf) (17–21/08/2026)
- Observatório IA nas Eleições (Data Privacy Brasil e Aláfia Lab), [*Ei, chat: em quem eu voto?*](https://observatorioianaseleicoes.com.br/wp-content/uploads/2026/06/20260616_Obs-IA-chatbot-.pdf) (6–10/04/2026)
- Ekō, [*Artificial hallucinations*](https://aks3.eko.org/images/Artificial_hallucinations_Brazil_report_DESIGNED.docx_1.pdf) ("Alucinações artificiais", 24/06–01/07/2026, publicado em 18/08/2026)
- JOTA, [*ChatGPT, Grok e Google IA fazem ranking de melhores candidatos, e descumprem norma do TSE*](https://www.jota.info/eleicoes/eleicoes-2026/chatgpt-grok-e-google-ia-fazem-ranking-de-melhores-candidatos-e-descumprem-norma-do-tse) (21/08/2026)
- TSE, Resolução nº 23.755, de 2 de março de 2026, que altera a Res. 23.610/2019 ([captura no Wayback Machine, 19/03/2026](https://web.archive.org/web/20260319123757/https://www.tse.jus.br/legislacao/compilada/res/2026/resolucao-no-23-755-de-2-de-marco-de-2026))
- AI Forensics, Universidade de Amsterdã e Politecnico di Milano, *(S)elected Moderation* (2024) — referência de método: mostrou que a moderação eleitoral da interface do consumidor difere da da API
