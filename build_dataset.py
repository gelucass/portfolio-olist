"""Monta a tabela de pedidos (1 linha por pedido) para o painel no Looker Studio."""
import pandas as pd

RAW = "raw/"

orders = pd.read_csv(RAW + "olist_orders_dataset.csv", parse_dates=[
    "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"])
items = pd.read_csv(RAW + "olist_order_items_dataset.csv")
products = pd.read_csv(RAW + "olist_products_dataset.csv")
customers = pd.read_csv(RAW + "olist_customers_dataset.csv")
reviews = pd.read_csv(RAW + "olist_order_reviews_dataset.csv")

# Itens -> pedido (agrega antes de juntar para não duplicar linhas)
items = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
items["product_category_name"] = items["product_category_name"].fillna("sem_categoria")
item_agg = items.groupby("order_id").agg(
    qtd_itens=("order_item_id", "count"),
    valor_produtos=("price", "sum"),
    valor_frete=("freight_value", "sum"),
)
# Categoria principal do pedido = a de maior valor
main_cat = (items.groupby(["order_id", "product_category_name"])["price"].sum()
            .reset_index().sort_values("price", ascending=False)
            .drop_duplicates("order_id").set_index("order_id")["product_category_name"])
ACENTOS = {"saude": "saúde", "informatica": "informática", "acessorios": "acessórios", "moveis": "móveis",
           "decoracao": "decoração", "domesticas": "domésticas", "relogios": "relógios", "bebes": "bebês",
           "eletronicos": "eletrônicos", "escritorio": "escritório", "eletrodomesticos": "eletrodomésticos",
           "construcao": "construção", "eletroportateis": "eletroportáteis", "tecnicos": "técnicos",
           "climatizacao": "climatização", "servico": "serviço", "calcados": "calçados", "iluminacao": "iluminação",
           "industria": "indústria", "comercio": "comércio", "negocios": "negócios", "seguranca": "segurança",
           "sinalizacao": "sinalização", "impressao": "impressão", "portateis": "portáteis", "cafe": "café",
           "colchao": "colchão", "musica": "música", "musicais": "musicais", "servicos": "serviços",
           "audio": "áudio", "cozinha": "cozinha", "area": "área", "higiene": "higiene"}
item_agg["categoria"] = (main_cat.str.split("_")
                         .map(lambda ws: " ".join(ACENTOS.get(w, w) for w in ws).capitalize()))

# Avaliações: alguns pedidos têm mais de uma -> média
review_agg = reviews.groupby("order_id")["review_score"].mean().rename("nota_avaliacao")

df = (orders
      .merge(customers[["customer_id", "customer_city", "customer_state"]], on="customer_id", how="left")
      .join(item_agg, on="order_id", how="inner")
      .join(review_agg, on="order_id", how="left"))

# Período com volume consistente (a base tem poucos pedidos em 2016 e após ago/2018)
df = df[(df["order_purchase_timestamp"] >= "2017-01-01") & (df["order_purchase_timestamp"] < "2018-09-01")]

status_pt = {"delivered": "Entregue", "shipped": "Enviado", "canceled": "Cancelado", "unavailable": "Indisponível",
             "invoiced": "Faturado", "processing": "Em processamento", "created": "Criado", "approved": "Aprovado"}
entregue = df["order_status"].eq("delivered") & df["order_delivered_customer_date"].notna()

out = pd.DataFrame({
    "pedido_id": df["order_id"],
    "data_compra": df["order_purchase_timestamp"].dt.strftime("%Y-%m-%d"),
    "status": df["order_status"].map(status_pt).fillna(df["order_status"]),
    "estado": df["customer_state"],
    "cidade": df["customer_city"].str.title(),
    "categoria": df["categoria"],
    "qtd_itens": df["qtd_itens"],
    "valor_produtos": df["valor_produtos"].round(2),
    "valor_frete": df["valor_frete"].round(2),
    "valor_total": (df["valor_produtos"] + df["valor_frete"]).round(2),
    "entregue": entregue.map({True: "Sim", False: "Não"}),
    "dias_entrega": (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days.where(entregue),
    "entrega_atrasada": (df["order_delivered_customer_date"].dt.normalize()
                         > df["order_estimated_delivery_date"].dt.normalize()).where(entregue)
                        .map({True: "Sim", False: "Não"}),
    "nota_avaliacao": df["nota_avaliacao"].round(1),
})

out.to_csv("pedidos_olist.csv", index=False)

# Conferências
assert out["pedido_id"].is_unique
print(f"linhas: {len(out):,}  |  período: {out.data_compra.min()} a {out.data_compra.max()}")
print(f"faturamento total: R$ {out.valor_total.sum():,.0f}  |  ticket médio: R$ {out.valor_total.mean():,.2f}")
ent = out[out.entregue == "Sim"]
print(f"entregues: {len(ent):,}  |  atrasados: {(ent.entrega_atrasada == 'Sim').mean():.1%}  |  "
      f"prazo médio: {ent.dias_entrega.mean():.1f} dias  |  nota média: {out.nota_avaliacao.mean():.2f}")
print("top categorias:", out.groupby("categoria").valor_total.sum().nlargest(5).round(0).to_dict())
