# Roadmap

O pacote faz uma coisa — reproduzir a tabela e os números do artigo — e está completo para
isso. O que segue são candidatos honestos, não compromissos; cada um traz a condição que o
justificaria.

## Em consideração

**6ª rodada do ITS Rio.** O MPF anunciou em 25/09/2026 uma 6ª rodada "com divulgação dos
resultados antes do primeiro turno"; até 2026-10-02 ela não estava publicada. *Gatilho: a
publicação do relatório.* A tabela é recodificada pela mesma régua, os testes ganham os
números novos e sai uma versão menor (1.1.0), com o artigo atualizado no mesmo dia.

**Coluna `indicador` na tabela.** A 5ª rodada criou um indicador de "recomendação" distinto do
de ranqueamento; hoje ele vive nas notas e nas linhas narrativas, porque `agregado_pct` é
sempre ranqueamento (REGUA.md §7.7). *Gatilho: uma segunda fonte que publique os dois
indicadores separados.*

**Notebook de replicação.** Um Colab que clona, roda `run_all.py` e confere o selo sem
instalação local. *Gatilho: pedido de leitor; o caminho de dois comandos do README já
dispensa instalação além do `pytest`.*

## Fora de questão

- Redistribuir as cópias em texto dos relatórios. O texto é dos autores; o repositório ensina
  a recriá-las a partir dos PDFs públicos (REPRODUCIBILITY.md).
- Publicar qual candidato cada sistema citou ou ranqueou. A tabela registra a forma da
  resposta, nunca o conteúdo (REGUA.md §6); quem precisar da ordem abre o PDF na página citada.
- Medição própria dos assistentes. O artigo é releitura de medições publicadas; medir seria
  outro projeto, com outro desenho e outro repositório.
