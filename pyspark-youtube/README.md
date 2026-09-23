# ⚡ Otimização de dados com PySpark — YouTube

Projeto prático desenvolvido durante o curso de **Analista de Dados**, com foco em otimização de processamento no PySpark.

## 🎯 Objetivo

Comparar diferentes estratégias para integrar bases de vídeos e comentários e aplicar técnicas para tornar o processamento mais eficiente.

## 🧰 Tecnologias

- Python
- PySpark
- Spark SQL
- Parquet

## 🔎 O que foi praticado

- Leitura de arquivos Parquet
- Criação de tabelas temporárias com `createOrReplaceTempView`
- `JOIN` com Spark SQL
- `repartition` pela chave `Video ID`
- `coalesce` antes da escrita
- Filtro antecipado de chaves nulas
- Seleção somente das colunas necessárias
- `broadcast` para apoiar joins com a menor base
- `explain("formatted")` para analisar planos de execução
- Salvamento do resultado otimizado em Parquet

## 📁 Arquivos

```text
pyspark-youtube/
├── README.md
├── requirements.txt
└── otimizacao.ipynb
```

> Os arquivos Parquet utilizados como entrada fazem parte das etapas anteriores do projeto e podem ser colocados na mesma pasta do notebook para execução local.

## ▶️ Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Abra o notebook no PyCharm, Jupyter ou VS Code e execute as células em ordem.

## 📚 Aprendizados

A principal ideia desta etapa é entender que performance em Big Data não depende somente da consulta final. A distribuição das partições, o volume de dados movimentado, o filtro antecipado, a quantidade de colunas selecionadas e a escolha da estratégia de join também influenciam o processamento.

📌 **Projeto desenvolvido como atividade prática do curso de Analista de Dados.**
