#!/usr/bin/env python3
"""Sela o repositório com um chain_hash SHA-256 (build e --verify).

Arquivos selados, em ordem lexicografica: REGUA.md, data/*.csv, data/checar-tabela.py,
tests/*.py, run_all.py. O hash encadeado e h_i = sha256(h_{i-1} + caminho + sha256(arquivo)).
Fora do selo (informativo): versao do Python e plataforma.
"""

import hashlib
import json
import platform
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / "output"


def arquivos():
    """Liste os arquivos selados.

    Returns
    -------
    list of pathlib.Path
        Caminhos relativos à raiz do repositório, em ordem lexicográfica de ``as_posix()``.
    """
    achados = {Path("REGUA.md"), Path("run_all.py")}
    achados |= {p.relative_to(RAIZ) for p in (RAIZ / "data").glob("*.csv")}
    achados.add(Path("data/checar-tabela.py"))
    achados |= {p.relative_to(RAIZ) for p in (RAIZ / "tests").glob("*.py")}
    return sorted(achados, key=lambda p: p.as_posix())


def calcular():
    """Calcule o sha256 de cada arquivo selado e o hash encadeado.

    Returns
    -------
    itens : list of dict
        Um ``{"path": str, "sha256": str}`` por arquivo, na ordem de :func:`arquivos`.
    cadeia : str
        ``chain_hash`` final: ``h_i = sha256(h_{i-1} + caminho + sha256(arquivo))``, com
        ``h_0 = sha256(b"")``.
    """
    cadeia = hashlib.sha256(b"").hexdigest()
    itens = []
    for rel in arquivos():
        h = hashlib.sha256((RAIZ / rel).read_bytes()).hexdigest()
        itens.append({"path": rel.as_posix(), "sha256": h})
        cadeia = hashlib.sha256((cadeia + rel.as_posix() + h).encode()).hexdigest()
    return itens, cadeia


def gravar():
    """Grave ``output/provenance.json`` e ``output/hash-chain.md`` e imprima o selo.

    A versão do Python e a plataforma vão para a seção "Informational (NOT hashed)" de
    ``hash-chain.md``: variam por máquina e não entram no selo.
    """
    itens, cadeia = calcular()
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "provenance.json").write_text(
        json.dumps(
            {"algorithm": "sha256-chain", "chain_hash": cadeia, "files": itens},
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    linhas = [
        "# Hash chain",
        "",
        f"chain_hash: `{cadeia}`",
        "",
        "| arquivo | sha256 |",
        "|---|---|",
    ]
    linhas += [f"| `{i['path']}` | `{i['sha256']}` |" for i in itens]
    linhas += [
        "",
        "## Informational (NOT hashed)",
        "",
        f"- Python {platform.python_version()} em {platform.system()}",
        "",
    ]
    (SAIDA / "hash-chain.md").write_text("\n".join(linhas))
    print(f"chain_hash {cadeia}")


def verificar():
    """Recompute o selo e compare com ``output/provenance.json``.

    Returns
    -------
    int
        ``0`` se todos os arquivos e o ``chain_hash`` conferem; ``1`` se o arquivo de selo
        falta ou se algo diverge (cada arquivo divergente é impresso).
    """
    alvo = SAIDA / "provenance.json"
    if not alvo.exists():
        print("provenance.json ausente: rode python make_provenance.py")
        return 1
    gravado = json.loads(alvo.read_text())
    itens, cadeia = calcular()
    if gravado["files"] != itens or gravado["chain_hash"] != cadeia:
        antigo = {i["path"]: i["sha256"] for i in gravado["files"]}
        for i in itens:
            if antigo.get(i["path"]) != i["sha256"]:
                print(f"DIVERGE: {i['path']}")
        print("PROVENIENCIA REPROVADA")
        return 1
    print(f"proveniencia verificada: chain_hash {cadeia}")
    return 0


if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(verificar())
    gravar()
