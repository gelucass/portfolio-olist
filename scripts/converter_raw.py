"""Converte os CSVs do Kaggle (raw/) em Parquet (data/raw/), versionados no repositório.

Roda uma vez, depois de baixar o dataset. Parquet comprime ~5x e preserva tipos,
o que permite ao CI rodar o pipeline sem depender do Kaggle.
"""
import duckdb

TABELAS = ["orders", "order_items", "products", "customers", "order_reviews"]

con = duckdb.connect()
for t in TABELAS:
    con.execute(f"""
        copy (select * from read_csv('raw/olist_{t}_dataset.csv', header = true, all_varchar = true))
        to 'data/raw/{t}.parquet' (format parquet, compression zstd)
    """)
    n = con.execute(f"select count(*) from 'data/raw/{t}.parquet'").fetchone()[0]
    print(f"{t:<14} {n:>8,} linhas")
