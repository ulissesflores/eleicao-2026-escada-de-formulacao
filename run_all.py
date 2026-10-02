#!/usr/bin/env python3
"""Entry-point único: gate da tabela -> pytest -> verificação do selo.

Sai com código diferente de zero se qualquer etapa falhar. Sem a pasta ``fontes/`` (cópias em
texto dos relatórios, não redistribuídas), o gate roda com ``--sem-ancoras`` e a saída diz isso.
"""

import csv
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FONTES = RAIZ / "fontes"


def locais_necessarios():
    """Liste as cópias em texto das fontes que o gate precisa para conferir âncoras.

    Returns
    -------
    set of str
        Caminhos relativos a ``fontes/`` citados em ``fontes.csv`` (``arquivo_local``),
        ``instrumentos.csv`` e ``tabela-codificada.csv`` (``arquivo``).
    """
    nomes = set()
    for csv_nome, col in (
        ("fontes.csv", "arquivo_local"),
        ("instrumentos.csv", "arquivo"),
        ("tabela-codificada.csv", "arquivo"),
    ):
        with open(RAIZ / "data" / csv_nome, newline="") as fh:
            nomes |= {r[col] for r in csv.DictReader(fh)}
    return nomes


def rodar(titulo, cmd):
    """Execute uma etapa na raiz do repositório.

    Parameters
    ----------
    titulo : str
        Rótulo impresso antes da etapa.
    cmd : list of str
        Comando a executar.

    Returns
    -------
    int
        Código de saída do comando.
    """
    print(f"\n=== {titulo} ===", flush=True)
    return subprocess.run(cmd, cwd=RAIZ).returncode


def main():
    """Rode as três etapas; todas rodam mesmo se a anterior falhar.

    Returns
    -------
    int
        ``0`` se as três etapas saírem com zero; ``1`` caso contrário.
    """
    faltam = sorted(n for n in locais_necessarios() if not (FONTES / n).exists())
    gate = [sys.executable, "data/checar-tabela.py"]
    if FONTES.is_dir() and not faltam:
        modo = "com ancoras (fontes/ completa)"
    else:
        gate.append("--sem-ancoras")
        motivo = "fontes/ ausente" if not FONTES.is_dir() else f"faltam {len(faltam)} arquivos"
        print(f"ATENCAO: {motivo}; gate em modo --sem-ancoras, ANCORAS NAO CONFERIDAS.")
        modo = "SEM ancoras"
    codigos = [
        rodar(f"1/3 gate da tabela ({modo})", gate),
        rodar("2/3 pytest", [sys.executable, "-m", "pytest"]),
        rodar("3/3 proveniencia", [sys.executable, "make_provenance.py", "--verify"]),
    ]
    ok = not any(codigos)
    print("\nrun_all: " + ("OK" if ok else f"FALHOU (codigos {codigos})") + f" [{modo}]")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
