# Dashboard Comercial 2026

Aplicação web em Python com Streamlit e Plotly para acompanhar faturamento a partir de um arquivo Excel atualizado periodicamente.

## Requisitos
- Python 3.10 ou superior
- Excel `.xlsx`, `.xlsm` ou `.xls`
- Bibliotecas listadas em `requirements.txt`

## Como executar no Windows
1. Extraia o ZIP para uma pasta.
2. Abra o Prompt de Comando nessa pasta.
3. Instale as dependências:

   ```bash
   py -m pip install -r requirements.txt
   ```

4. Inicie a aplicação:

   ```bash
   py -m streamlit run app.py
   ```

5. O navegador abrirá a página. Carregue a versão atualizada do Excel na barra lateral.

## Estrutura de dados recomendada
O formato mais confiável é uma tabela única, com uma linha por produto/fabricante/mês:

| Ano | Produto | Fabricante | Mês | Faturamento |
|---|---|---|---|---:|
| 2026 | Butter Toffe | ARCOR | Janeiro | 75917.65 |

O app também tenta ler planilhas organizadas em blocos com a linha de cabeçalho `FABRICANTE` e colunas de meses. Como o arquivo original ainda não foi fornecido, é importante validar os dados extraídos antes de usar os totais em decisões gerenciais.

## Funcionalidades
- Filtros por produto/bloco, fabricante e mês
- Indicadores de faturamento filtrado, mês mais recente nos filtros, produto líder e fabricante líder
- Evolução mensal
- Ranking por produto e fabricante
- Comparativo mensal empilhado
- Exportação dos dados filtrados em CSV e Excel

## Atenção sobre totais
Se a planilha tiver um bloco consolidado (`2026 - TOTAL`) e blocos detalhados por produto, não selecione ambos juntos sem confirmar a regra de negócio: isso pode duplicar valores. O app sinaliza essa situação.
