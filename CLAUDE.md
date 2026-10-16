# Portfólio Olist — instruções para o Claude

Pipeline de dados do dataset público da Olist: Parquet → dbt + DuckDB → painel web (GitHub Pages) e
métricas e roteiros para montar o mesmo painel em Power BI, Tableau, Metabase e Looker Studio.

## Estrutura
- `data/raw/` Parquet de origem (versionado). `olist_dbt/` projeto dbt (staging → intermediate → marts).
- `metricas/metricas.yml` **fonte única dos KPIs**, com a tradução para cada ferramenta de BI.
- `metricas/valores_esperados.md` gabarito gerado; nunca editar à mão.
- `bi/<ferramenta>/` pacote de cada ferramenta (gerado por `scripts/gerar_pacotes_bi.py` + roteiro).
- `site/index.html` painel web; `scripts/exportar.py` gera `_site/` e `exports/pedidos_olist.csv`.

## Comandos
```bash
cd olist_dbt && ../.venv/bin/dbt build --profiles-dir . && cd ..   # modelos + testes
.venv/bin/python scripts/exportar.py                              # painel, docs e CSV
.venv/bin/python scripts/validar_metricas.py                      # valores esperados
.venv/bin/python scripts/gerar_pacotes_bi.py                      # medidas de cada BI
```

## Regras
- Nomes de modelos, colunas e textos em português. Código e comentários seguem o estilo do arquivo vizinho.
- Toda mudança em modelo dbt passa por `dbt build` antes do commit; nenhum teste pode falhar.
- KPI novo ou alterado: use a skill `traduzir-metricas-bi`. Nunca defina uma métrica direto numa ferramenta.
- Modelo dbt novo: use a skill `modelo-dbt`. Peça ao agent `revisor-dbt` uma revisão antes do commit.
- Números de uma ferramenta que não batem: use o agent `auditor-bi`.
- Dados confidenciais (ex.: trabalho de cliente): skill `dados-confidenciais`. O hook em `.claude/hooks/` bloqueia o acesso aos caminhos e comandos listados em `.claude/governanca.json`.
