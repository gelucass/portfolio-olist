"""Lê os marts do DuckDB (gerados pelo dbt) e monta as saídas:

  _site/index.html + _site/data.json   painel web (publicado no GitHub Pages)
  _site/docs/index.html                documentação do dbt (se tiver sido gerada)
  exports/pedidos_olist.csv            1 linha por pedido, para o Looker Studio

Uso: python scripts/exportar.py   (depois de `dbt build` e, opcional, `dbt docs generate --static`)
"""
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get("OLIST_DUCKDB_PATH", RAIZ / "olist_dbt" / "olist.duckdb"))
SITE = RAIZ / "_site"
EXPORTS = RAIZ / "exports"

# coluna do mart -> chave curta usada pelo painel (mantém o data.json pequeno)
COLUNAS = {
    "pedidos": "ped", "receita": "rec", "valor_frete": "fre", "valor_produtos": "pro",
    "pedidos_entregues": "ent", "pedidos_atrasados": "atr", "pedidos_cancelados": "canc",
    "soma_dias_entrega": "dias", "pedidos_com_prazo": "nd", "soma_notas": "nota", "pedidos_avaliados": "nn",
    **{f"soma_nota_faixa_{i}": f"s{i}" for i in range(5)},
    **{f"avaliados_faixa_{i}": f"n{i}" for i in range(5)},
    "soma_nota_atrasados": "sa", "avaliados_atrasados": "na",
    "soma_nota_no_prazo": "sp", "avaliados_no_prazo": "np",
}


def exportar_painel(con):
    df = con.execute("select * from mart_painel_mensal").df()
    df["mes"] = df["mes_compra"].dt.strftime("%Y-%m")
    meses, estados, cats = (sorted(df[c].unique()) for c in ("mes", "estado", "categoria"))
    idx = {c: {v: i for i, v in enumerate(vals)} for c, vals in
           (("mes", meses), ("estado", estados), ("categoria", cats))}

    linhas = []
    for r in df.itertuples(index=False):
        linha = [idx["mes"][r.mes], idx["estado"][r.estado], idx["categoria"][r.categoria]]
        for col in COLUNAS:
            v = float(getattr(r, col))
            linha.append(int(v) if v.is_integer() else round(v, 2))
        linhas.append(linha)

    SITE.mkdir(exist_ok=True)
    payload = {"gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "meses": meses, "estados": estados, "cats": cats,
               "cols": list(COLUNAS.values()), "rows": linhas}
    (SITE / "data.json").write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    shutil.copy(RAIZ / "site" / "index.html", SITE / "index.html")
    print(f"painel: {len(linhas):,} linhas agregadas -> _site/data.json")

    docs = RAIZ / "olist_dbt" / "target" / "static_index.html"
    if docs.exists():
        (SITE / "docs").mkdir(exist_ok=True)
        shutil.copy(docs, SITE / "docs" / "index.html")
        print("docs do dbt -> _site/docs/")


def exportar_looker(con):
    EXPORTS.mkdir(exist_ok=True)
    destino = EXPORTS / "pedidos_olist.csv"
    con.execute(f"""
        copy (
            select
                pedido_id, strftime(data_compra, '%Y-%m-%d') as data_compra, status, estado, cidade, categoria,
                qtd_itens, valor_produtos, valor_frete, valor_total,
                case when is_entregue then 'Sim' else 'Não' end as entregue,
                dias_entrega,
                case is_atrasado when true then 'Sim' when false then 'Não' end as entrega_atrasada,
                nota_avaliacao
            from fct_pedidos
            order by data_compra, pedido_id
        ) to '{destino}' (header, delimiter ',')
    """)
    n = con.execute("select count(*) from fct_pedidos").fetchone()[0]
    print(f"looker: {n:,} pedidos -> exports/pedidos_olist.csv")


if __name__ == "__main__":
    with duckdb.connect(str(DB), read_only=True) as con:
        exportar_painel(con)
        exportar_looker(con)
