# Looker Studio: campos calculados

_Gerado por scripts/gerar_pacotes_bi.py a partir de metricas/metricas.yml. Não edite à mão._

Crie na fonte de dados (Recurso → Gerenciar fontes de dados → Editar → Adicionar campo), não no gráfico, para reaproveitar em todo o relatório.

### Receita
Valor dos produtos + frete.

```
SUM(valor_total)
```

### Pedidos
Quantidade de pedidos (uma linha por pedido na fonte).

```
COUNT_DISTINCT(pedido_id)
```

### Ticket médio
Receita ÷ pedidos. É uma razão de somas, não a média de uma coluna.

```
SUM(valor_total) / COUNT_DISTINCT(pedido_id)
```

### Nota média
Média da avaliação do cliente (1 a 5). Pedidos sem avaliação ficam fora da média.

```
AVG(nota_avaliacao)
```

### Prazo médio de entrega (dias)
Dias entre a compra e a entrega, só para pedidos entregues.

```
AVG(dias_entrega)
```

### Entregas com atraso
Pedidos entregues depois da data prometida ÷ pedidos entregues.

```
SUM(CASE WHEN entrega_atrasada = "Sim" THEN 1 ELSE 0 END) / SUM(CASE WHEN entregue = "Sim" THEN 1 ELSE 0 END)
```

### Nota com entrega no prazo
Nota média dos pedidos entregues dentro do prazo.

```
AVG(CASE WHEN entrega_atrasada = "Não" THEN nota_avaliacao END)
```

### Nota com entrega atrasada
Nota média dos pedidos entregues depois do prazo.

```
AVG(CASE WHEN entrega_atrasada = "Sim" THEN nota_avaliacao END)
```

### Frete sobre produtos
Quanto o frete representa sobre o valor dos produtos.

```
SUM(valor_frete) / SUM(valor_produtos)
```
