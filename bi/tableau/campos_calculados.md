# Tableau: campos calculados

_Gerado por scripts/gerar_pacotes_bi.py a partir de metricas/metricas.yml. Não edite à mão._

Em Análise → Criar campo calculado, use o rótulo como nome e cole a fórmula. São cálculos agregados: não misture com campos de linha na mesma fórmula.

### Receita
Valor dos produtos + frete.

```
SUM([valor_total])
```

### Pedidos
Quantidade de pedidos (uma linha por pedido na fonte).

```
COUNTD([pedido_id])
```

### Ticket médio
Receita ÷ pedidos. É uma razão de somas, não a média de uma coluna.

```
SUM([valor_total]) / COUNTD([pedido_id])
```

### Nota média
Média da avaliação do cliente (1 a 5). Pedidos sem avaliação ficam fora da média.

```
AVG([nota_avaliacao])
```

### Prazo médio de entrega (dias)
Dias entre a compra e a entrega, só para pedidos entregues.

```
AVG([dias_entrega])
```

### Entregas com atraso
Pedidos entregues depois da data prometida ÷ pedidos entregues.

```
SUM(IIF([entrega_atrasada] = 'Sim', 1, 0)) / SUM(IIF([entregue] = 'Sim', 1, 0))
```

### Nota com entrega no prazo
Nota média dos pedidos entregues dentro do prazo.

```
AVG(IF [entrega_atrasada] = 'Não' THEN [nota_avaliacao] END)
```

### Nota com entrega atrasada
Nota média dos pedidos entregues depois do prazo.

```
AVG(IF [entrega_atrasada] = 'Sim' THEN [nota_avaliacao] END)
```

### Frete sobre produtos
Quanto o frete representa sobre o valor dos produtos.

```
SUM([valor_frete]) / SUM([valor_produtos])
```
