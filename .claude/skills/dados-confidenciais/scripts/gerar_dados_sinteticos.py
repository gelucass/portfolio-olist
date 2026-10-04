"""Gera um CSV de dados falsos a partir da estrutura de uma tabela, sem tocar nos dados reais.

Formato do schema.yml:
    tabela: pedidos
    colunas:
      - {nome: pedido_id, tipo: id}
      - {nome: data_compra, tipo: data, de: 2024-01-01, ate: 2024-12-31}
      - {nome: estado, tipo: categoria, valores: [SP, RJ, MG]}
      - {nome: valor_total, tipo: decimal, min: 10, max: 2000}
      - {nome: qtd_itens, tipo: inteiro, min: 1, max: 5}
      - {nome: entregue, tipo: booleano, prob: 0.95}
      - {nome: nota, tipo: inteiro, min: 1, max: 5, nulos: 0.1}

Uso: python gerar_dados_sinteticos.py schema.yml --linhas 5000 [--saida pedidos_sintetico.csv] [--semente 42]
"""
import argparse
import csv
import random
import uuid
from datetime import date, timedelta

import yaml


def gerar_valor(col, rng):
    if rng.random() < col.get("nulos", 0):
        return ""
    tipo = col["tipo"]
    if tipo == "id":
        return uuid.UUID(int=rng.getrandbits(128)).hex
    if tipo == "inteiro":
        return rng.randint(col.get("min", 0), col.get("max", 100))
    if tipo == "decimal":
        return round(rng.uniform(col.get("min", 0), col.get("max", 1000)), 2)
    if tipo == "categoria":
        return rng.choice(col["valores"])
    if tipo == "booleano":
        return rng.random() < col.get("prob", 0.5)
    if tipo == "data":
        de, ate = date.fromisoformat(str(col["de"])), date.fromisoformat(str(col["ate"]))
        return de + timedelta(days=rng.randint(0, (ate - de).days))
    if tipo == "texto":
        return f"{col['nome']}_{rng.randint(1, col.get('distintos', 1000))}"
    raise ValueError(f"tipo desconhecido: {tipo} (coluna {col['nome']})")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("schema")
    p.add_argument("--linhas", type=int, default=1000)
    p.add_argument("--saida")
    p.add_argument("--semente", type=int, default=42)
    args = p.parse_args()

    spec = yaml.safe_load(open(args.schema, encoding="utf-8"))
    saida = args.saida or f"{spec['tabela']}_sintetico.csv"
    rng = random.Random(args.semente)
    colunas = spec["colunas"]

    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(c["nome"] for c in colunas)
        for _ in range(args.linhas):
            w.writerow(gerar_valor(c, rng) for c in colunas)
    print(f"{args.linhas:,} linhas sintéticas -> {saida}")


if __name__ == "__main__":
    main()
