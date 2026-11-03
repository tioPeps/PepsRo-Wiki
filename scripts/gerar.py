"""Gerador de dados da Wiki PepsRO.

Lê o banco do rAthena da PRODUÇÃO (somente leitura) e grava páginas em
Markdown dentro de docs/database/. Nunca escreve na pasta do servidor.

Uso:
    .venv\\Scripts\\python scripts\\gerar.py --resumo

Etapas previstas (ainda não implementadas): monstros, drops e mapas.
Itens ficam para depois, a pedido do usuário.
"""

import argparse
import sys
from pathlib import Path

import yaml

WIKI = Path(__file__).resolve().parent.parent
SERVIDOR_PADRAO = Path(r"D:\Servidor Ragnarok\PepsRo\rathena-producao")
SAIDA = WIKI / "docs" / "database"

# Arquivo de topo de cada banco: primeiro o oficial (db/re), depois o do PepsRO (db/import).
BANCOS = {
    "itens": ["db/re/item_db.yml", "db/import/item_db.yml"],
    "monstros": ["db/re/mob_db.yml", "db/import/mob_db.yml"],
    "drops_mapa": ["db/re/map_drops.yml", "db/import/map_drops.yml"],
}


def ler_yaml(servidor, relativo, vistos):
    """Lê um YAML do rAthena e os arquivos do Footer/Imports, na ordem do rAthena."""
    caminho = (servidor / relativo).resolve()
    if caminho in vistos or not caminho.exists():
        return []
    vistos.add(caminho)
    with open(caminho, encoding="utf-8") as f:
        dados = yaml.safe_load(f) or {}
    entradas = list(dados.get("Body") or [])
    for imp in (dados.get("Footer") or {}).get("Imports") or []:
        entradas += ler_yaml(servidor, imp["Path"], vistos)
    return entradas


def juntar(servidor, arquivos, chave="Id"):
    """Junta as entradas campo a campo pela chave, como o rAthena faz com o db/import."""
    resultado = {}
    vistos = set()
    for relativo in arquivos:
        for entrada in ler_yaml(servidor, relativo, vistos):
            if chave not in entrada:
                continue
            resultado.setdefault(entrada[chave], {}).update(entrada)
    return resultado


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--servidor", type=Path, default=SERVIDOR_PADRAO, help="pasta do rathena (só leitura)")
    ap.add_argument("--resumo", action="store_true", help="só mostra quantos registros foram lidos")
    args = ap.parse_args()

    servidor = args.servidor.resolve()
    if WIKI in servidor.parents or servidor == WIKI:
        sys.exit("A pasta do servidor não pode ficar dentro da Wiki.")
    if not (servidor / "db").is_dir():
        sys.exit(f"Pasta do servidor inválida: {servidor}")

    itens = juntar(servidor, BANCOS["itens"])
    monstros = juntar(servidor, BANCOS["monstros"])
    mapas = juntar(servidor, BANCOS["drops_mapa"], chave="Map")

    print(f"Servidor: {servidor}")
    print(f"Itens: {len(itens)}  Monstros: {len(monstros)}  Mapas com drop próprio: {len(mapas)}")

    if args.resumo:
        return
    print("Geração de páginas ainda não implementada.")


if __name__ == "__main__":
    main()
