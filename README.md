# 📊 Dashboard de E-commerce

Dashboard interativo desenvolvido em **Python** como continuação de um projeto de análise exploratória de dados do curso de **Analista de Dados**.

O projeto transforma as análises realizadas no notebook em uma aplicação web interativa, permitindo explorar os dados de forma visual, dinâmica e sem a necessidade de executar o código Python diretamente.

## 🎯 Objetivo

Apresentar informações relevantes sobre produtos de e-commerce por meio de indicadores e visualizações interativas, facilitando a análise de:

- preços;
- avaliações;
- descontos;
- marcas;
- gêneros;
- vendas.

## 🛠️ Tecnologias utilizadas

- **Python** — desenvolvimento da aplicação
- **Pandas** — leitura e tratamento dos dados
- **Plotly** — criação dos gráficos interativos
- **Dash** — construção do dashboard web
- **NumPy** — apoio aos cálculos das visualizações

## 📈 Visualizações

O dashboard reúne as visualizações desenvolvidas no módulo anterior:

| Visualização | Objetivo |
|---|---|
| 📊 Histograma | Analisar a distribuição dos preços |
| 🔵 Dispersão | Observar a relação entre preço e número de avaliações |
| 🔥 Mapa de calor | Identificar correlações entre variáveis numéricas |
| 📈 Barras | Comparar as marcas com maior quantidade de produtos |
| 🥧 Pizza | Visualizar a distribuição dos produtos por gênero |
| 📉 Densidade | Analisar a distribuição suavizada dos preços |
| 📐 Regressão | Observar a relação entre avaliações e vendas codificadas |

### Indicadores

O dashboard também apresenta:

- quantidade de produtos analisados;
- preço médio;
- nota média;
- média de avaliações.

### Filtros

A aplicação permite filtrar os resultados por:

- **Gênero**
- **Temporada**

Os indicadores e gráficos são atualizados de acordo com os filtros selecionados.

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/eduardosilvafonseca18-netizen/projeto_ecommerce.git
```

Entre na pasta:

```bash
cd projeto_ecommerce
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install pandas dash plotly numpy
```

### 4. Execute o dashboard

```bash
python app.py
```

Abra no navegador o endereço exibido no terminal, normalmente:

```text
http://127.0.0.1:8050/
```

## 📂 Estrutura do projeto

```text
projeto_ecommerce/
│
├── .gitignore
├── app.py
├── dados.csv
│
└── assets/
    └── style.css
```

## 🔎 Funcionamento

Ao iniciar a aplicação, o arquivo `dados.csv` é carregado em um DataFrame. Os dados são tratados e utilizados para alimentar os indicadores e gráficos do dashboard.

A interação com os filtros de **gênero** e **temporada** atualiza os resultados exibidos na tela, permitindo uma exploração mais dinâmica da base.

## 📚 Aprendizados

Este projeto reúne conhecimentos de:

- análise exploratória de dados;
- tratamento e organização de dados com Pandas;
- visualização de dados;
- criação de gráficos interativos com Plotly;
- desenvolvimento de dashboards com Dash;
- transformação de uma análise em notebook em uma aplicação web.

## 🚀 Próximos passos

O projeto pode ser evoluído com novas perguntas de negócio, indicadores, filtros e visualizações, ampliando as possibilidades de análise dos dados.

---

📌 **Projeto desenvolvido como atividade prática do curso de Analista de Dados.**
