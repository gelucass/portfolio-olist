---
name: dados-confidenciais
description: Modo de trabalho para projetos com dados confidenciais (cliente, empresa, dados pessoais) em que o Claude escreve código sem nunca ver os dados reais. Use quando o usuário disser que os dados são sigilosos, de cliente ou de produção, ou antes de trabalhar num repositório com .claude/governanca.json.
---

# Trabalhar sem ver dados confidenciais

Princípio: **o Claude só vê o que passa por ele.** Se os dados reais nunca entram na conversa, não
há como vazarem por ela. O Claude escreve o código; o código roda no ambiente da empresa.

## O que o Claude pode receber
- Estrutura: nomes de tabelas e colunas, tipos, chaves, descrição do negócio.
- Contagens agregadas que o usuário decidir compartilhar (ex.: "a tabela tem ~2 milhões de linhas").
- Dados sintéticos gerados a partir da estrutura (passo 2).

## O que o Claude não faz
- Não roda consultas em banco de produção nem lê extrações de dados reais.
- Não pede ao usuário que cole resultados, amostras ou prints com valores reais.
- Não publica artifacts, gists ou repositórios com conteúdo do cliente, nem com nomes de tabelas
  ou regras de negócio que o usuário não liberou.

## Fluxo
1. **Peça só a estrutura** (DDL, `information_schema` exportado ou descrição das colunas) e grave em
   `schema.yml` no formato de `scripts/gerar_dados_sinteticos.py`.
2. **Gere dados falsos com o mesmo formato:**
   ```bash
   python .claude/skills/dados-confidenciais/scripts/gerar_dados_sinteticos.py schema.yml --linhas 5000
   ```
3. **Desenvolva e teste** modelos, consultas e painéis em cima dos dados sintéticos.
4. **Entregue o código ao usuário**, que roda no ambiente real. Se algo falhar, peça a mensagem de
   erro, nunca o resultado.

## Trava técnica
O hook `.claude/hooks/proteger_dados.py` bloqueia leitura e comandos que batem com os padrões de
`.claude/governanca.json` (pastas de extração, `.env`, clientes de banco de produção). Ele é uma
segunda camada: a garantia principal é a máquina do Claude não ter credenciais de produção.
Antes de começar, confirme com o usuário que `governanca.json` lista as pastas e os comandos do projeto.
