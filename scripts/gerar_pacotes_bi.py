"""Gera as medidas de cada ferramenta de BI a partir de metricas/metricas.yml.

  bi/powerbi/medidas.dax                  medidas DAX + tabela calendário + comparação com mês anterior
  bi/tableau/campos_calculados.md         campos calculados para colar no Tableau
  bi/metabase/consultas.sql               perguntas SQL com filtros de campo do painel
  bi/looker-studio/campos_calculados.md   campos calculados da fonte de dados

Uso: python scripts/gerar_pacotes_bi.py
"""
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
AVISO = "Gerado por scripts/gerar_pacotes_bi.py a partir de metricas/metricas.yml. Não edite à mão."
FORMATO_PBI = {"moeda": '"R$ "#,##0.00', "inteiro": "#,##0", "decimal": "0.00", "percentual": "0.0%"}


def powerbi(metricas):
    out = [f"// {AVISO}", "// Cole cada bloco em Nova medida, na tabela _Medidas. Fato: pedidos.", ""]
    for m in metricas:
        out += [f"// {m['rotulo']}: {m['descricao']}  |  formato: {FORMATO_PBI[m['formato']]}", m["powerbi"], ""]
    out += [
        "// ---- Inteligência de tempo (exige a tabela Calendario marcada como tabela de datas) ----",
        "Receita mês anterior = CALCULATE ( [Receita], DATEADD ( Calendario[Data], -1, MONTH ) )",
        "",
        "Var. receita vs mês anterior = DIVIDE ( [Receita] - [Receita mês anterior], [Receita mês anterior] )",
        "",
        "// ---- Tabela calculada: Modelagem > Nova tabela ----",
        "Calendario =",
        "ADDCOLUMNS (",
        "    CALENDAR ( MIN ( pedidos[data_compra] ), MAX ( pedidos[data_compra] ) ),",
        '    "Ano", YEAR ( [Date] ),',
        '    "Mes", MONTH ( [Date] ),',
        '    "Ano-Mês", FORMAT ( [Date], "yyyy-mm" ),',
        '    "Mês", FORMAT ( [Date], "mmm/yy" )',
        ")",
        "// Depois: renomeie a coluna [Date] para Data e marque Calendario como tabela de datas.",
    ]
    return "\n".join(out) + "\n"


def tabela_md(titulo, metricas, campo, intro):
    out = [f"# {titulo}", "", f"_{AVISO}_", "", intro, ""]
    for m in metricas:
        out += [f"### {m['rotulo']}", m["descricao"], "", "```", m[campo], "```", ""]
    return "\n".join(out)


def metabase(metricas):
    out = [f"-- {AVISO}",
           "-- Cada bloco é uma pergunta SQL nativa sobre a tabela pedidos (Postgres).",
           "-- Variáveis: {{estado}} = Filtro de campo -> pedidos.estado; {{periodo}} = Filtro de campo -> pedidos.data_compra;",
           "--            {{categoria}} = Filtro de campo -> pedidos.categoria. Ligue as três aos filtros do painel.",
           "-- Os colchetes [[ ]] tornam cada filtro opcional.", ""]
    filtros = "where true\n  [[and {{estado}}]]\n  [[and {{periodo}}]]\n  [[and {{categoria}}]]"
    for m in metricas:
        out += [f"-- Pergunta: {m['rotulo']} ({m['descricao']})",
                f"select {m['metabase']} as \"{m['rotulo']}\"\nfrom pedidos\n{filtros};", ""]
    out += ["-- Pergunta: Receita e pedidos por mês (gráfico de linha)",
            "select date_trunc('month', data_compra)::date as mes,\n"
            "       sum(valor_total) as receita,\n       count(*) as pedidos\n"
            f"from pedidos\n{filtros}\ngroup by 1\norder by 1;", "",
            "-- Pergunta: Nota média por prazo de entrega",
            "select case when dias_entrega <= 7 then '1. até 7 dias'\n"
            "            when dias_entrega <= 14 then '2. 8 a 14'\n"
            "            when dias_entrega <= 21 then '3. 15 a 21'\n"
            "            when dias_entrega <= 30 then '4. 22 a 30'\n"
            "            else '5. mais de 30' end as faixa_prazo,\n"
            "       avg(nota_avaliacao) as nota_media,\n       count(nota_avaliacao) as pedidos_avaliados\n"
            f"from pedidos\n{filtros}\n  and dias_entrega is not null\ngroup by 1\norder by 1;", ""]
    return "\n".join(out)


def main():
    metricas = yaml.safe_load((RAIZ / "metricas" / "metricas.yml").read_text())["metricas"]
    arquivos = {
        "bi/powerbi/medidas.dax": powerbi(metricas),
        "bi/tableau/campos_calculados.md": tabela_md(
            "Tableau: campos calculados", metricas, "tableau",
            "Em Análise → Criar campo calculado, use o rótulo como nome e cole a fórmula. "
            "São cálculos agregados: não misture com campos de linha na mesma fórmula."),
        "bi/metabase/consultas.sql": metabase(metricas),
        "bi/looker-studio/campos_calculados.md": tabela_md(
            "Looker Studio: campos calculados", metricas, "looker_studio",
            "Crie na fonte de dados (Recurso → Gerenciar fontes de dados → Editar → Adicionar campo), "
            "não no gráfico, para reaproveitar em todo o relatório."),
    }
    for caminho, conteudo in arquivos.items():
        destino = RAIZ / caminho
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(conteudo)
        print(f"{len(metricas)} métricas -> {caminho}")


if __name__ == "__main__":
    main()
