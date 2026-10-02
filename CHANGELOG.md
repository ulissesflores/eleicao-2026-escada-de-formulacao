# Changelog

Formato [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento
[SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] - não lançado

Primeira versão pública, que acompanha o artigo
[ulissesflores.com/artigos/ia-eleicao-2026](https://ulissesflores.com/artigos/ia-eleicao-2026).

### Adicionado

- `REGUA.md`: régua de codificação escrita antes da tabela (2026-09-09, ajustada em
  2026-09-11 e 2026-10-02 com a 5ª rodada do ITS Rio).
- `data/fontes.csv` (8 fontes), `data/instrumentos.csv` (55 enunciados) e
  `data/tabela-codificada.csv` (162 linhas), cada linha com arquivo, linha e âncora verbatim.
- `data/checar-tabela.py`: o gate que produziu a tabela do artigo, byte a byte; modo
  `--sem-ancoras` para quem ainda não recriou as cópias em texto das fontes.
- `tests/`: cada número do artigo que deriva da tabela vira asserção.
- `make_provenance.py` e `output/`: selo SHA-256 encadeado, com `--verify`.
- `run_all.py`: entry-point único (gate -> testes -> selo).
- CI em Python 3.11 e 3.12 (selo, replicação, lint, cobertura de docstring).
- `CITATION.cff`, `codemeta.json`, `.zenodo.json`; licença dual Apache-2.0 + CC BY 4.0.

### Alterado

- 2026-10-02: o artigo trocou de título antes de ir ao ar — agora *Os termos de uso impedem até
  medir se a IA cumpre a lei eleitoral*. README, `CITATION.cff`, `codemeta.json`, `.zenodo.json`,
  `pyproject.toml` e a docstring dos testes citam o título novo; dados, régua e testes não mudaram.
