[README (2).md](https://github.com/user-attachments/files/32489543/README.2.md)
# Dashboard de E-commerce

Dashboard interativo desenvolvido como continuação do projeto de análise exploratória de dados do curso de Analista de Dados.

## Objetivo

Transformar as análises do notebook anterior em uma aplicação web interativa, permitindo que o usuário visualize os dados sem precisar interagir diretamente com o Python.

## Tecnologias

- Python
- Pandas
- Plotly
- Dash
- SciPy

## Visualizações

O dashboard apresenta:

- Histograma da distribuição de preços
- Gráfico de dispersão entre preço e número de avaliações
- Mapa de calor das correlações
- Gráfico de barras das principais marcas
- Gráfico de pizza por gênero
- Curva de densidade dos preços
- Regressão entre avaliações e quantidade de vendas codificada

Também foram adicionados filtros por gênero e temporada e indicadores com quantidade de produtos, preço médio, nota média e média de avaliações.

## Como executar

1. Abra a pasta do projeto no PyCharm.
2. Certifique-se de que `ecommerce_estatistica.csv` está na mesma pasta de `app.py`.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute `app.py`.
5. Abra no navegador o endereço exibido pelo terminal, normalmente:

```text
http://127.0.0.1:8050/
```
