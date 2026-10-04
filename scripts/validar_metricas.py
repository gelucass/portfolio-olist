"""Executa as métricas de metricas/metricas.yml sobre o CSV exportado e gera metricas/valores_esperados.md.

Esse arquivo é o gabarito: o painel de cada ferramenta (Power BI, Tableau, Metabase, Looker Studio)
precisa mostrar exatamente esses números nos mesmos recortes.

Uso: python scripts/validar_metricas.py   (depois de scripts/exportar.py)
"""
from pathlib import Path

import duckdb
import yaml

RAIZ = Path(__file__).resolve().parent.parent
FERRAMENTAS = ["powerbi", "tableau", "metabase", "looker_studio"]


def formatar(valor, formato):
    if valor is None:
        return "–"
    if formato == "moeda":
        texto = f"R$ {valor:,.2f}"
    elif formato == "inteiro":
        texto = f"{valor:,.0f}"
    elif formato == "percentual":
        texto = f"{valor * 100:,.2f}%"
    else:
        texto = f"{valor:,.3f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    spec = yaml.safe_load((RAIZ / "metricas" / "metricas.yml").read_text())
    metricas, recortes = spec["metricas"], spec["recortes"]

    for m in metricas:
        faltando = [f for f in FERRAMENTAS + ["sql", "rotulo", "formato"] if not m.get(f)]
        if faltando:
            raise SystemExit(f"métrica '{m['nome']}' sem: {', '.join(faltando)}")

    con = duckdb.connect()
    con.execute(f"create view pedidos as select * from read_csv('{RAIZ / spec['fonte']}', header = true)")

    selects = ", ".join(f"{m['sql']} as {m['nome']}" for m in metricas)
    linhas = []
    for r in recortes:
        valores = con.execute(f"select {selects} from pedidos where {r['filtro']}").fetchone()
        linhas.append((r["nome"], valores))

    md = ["# Valores esperados", "",
          "Gerado por `scripts/validar_metricas.py` a partir de `metricas/metricas.yml`. Não edite à mão.", "",
          "Cada painel (Power BI, Tableau, Metabase, Looker Studio) tem que mostrar estes números nos mesmos recortes.", "",
          "| Métrica | " + " | ".join(nome for nome, _ in linhas) + " |",
          "|---|" + "---:|" * len(linhas)]
    for i, m in enumerate(metricas):
        md.append(f"| {m['rotulo']} | " + " | ".join(formatar(v[i], m["formato"]) for _, v in linhas) + " |")
    md += ["", "## Filtros de cada recorte", ""]
    md += [f"- **{r['nome']}:** `{r['filtro']}`" for r in recortes]

    destino = RAIZ / "metricas" / "valores_esperados.md"
    destino.write_text("\n".join(md) + "\n")
    print(f"{len(metricas)} métricas × {len(recortes)} recortes -> {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
