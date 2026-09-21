from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ==========================================================
# 1. CONFIGURAÇÃO E LEITURA DOS DADOS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "dados.csv"


df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

# Garantia de tipos numéricos para os gráficos.
colunas_numericas = [
    "Nota",
    "N_Avaliações",
    "Desconto",
    "Preço",
    "Qtd_Vendidos_Cod",
]
for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df = df.dropna(subset=["Preço", "Nota", "N_Avaliações", "Desconto", "Qtd_Vendidos_Cod"])

# Remove uma coluna de índice criada na exportação, caso exista.
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# ==========================================================
# 2. FUNÇÕES DOS GRÁFICOS
# ==========================================================

def apply_layout(fig, title, x_title=None, y_title=None):
    fig.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        template="plotly_white",
        margin=dict(l=55, r=30, t=75, b=55),
        hovermode="closest",
        font=dict(family="Arial", size=13),
    )
    if x_title:
        fig.update_xaxes(title=x_title, showgrid=True, gridcolor="#E9EEF5")
    if y_title:
        fig.update_yaxes(title=y_title, showgrid=True, gridcolor="#E9EEF5")
    return fig


def empty_figure(message="Nenhum dado disponível para os filtros selecionados."):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def filter_data(genero, temporada):
    data = df.copy()
    if genero != "Todos":
        data = data[data["Gênero"] == genero]
    if temporada != "Todos":
        data = data[data["Temporada"] == temporada]
    return data


def histograma(data):
    fig = px.histogram(
        data,
        x="Preço",
        nbins=20,
        labels={"Preço": "Preço (R$)", "count": "Quantidade de produtos"},
    )
    fig.add_vline(
        x=data["Preço"].mean(),
        line_dash="dash",
        annotation_text=f"Média: R$ {data['Preço'].mean():.2f}",
        annotation_position="top right",
    )
    return apply_layout(fig, "Distribuição dos Preços dos Produtos", "Preço (R$)", "Quantidade de Produtos")


def dispersao(data):
    fig = px.scatter(
        data,
        x="Preço",
        y="N_Avaliações",
        hover_data=["Título", "Marca", "Nota"],
        labels={"Preço": "Preço (R$)", "N_Avaliações": "Número de avaliações"},
    )
    return apply_layout(fig, "Relação entre Preço e Número de Avaliações", "Preço (R$)", "Número de Avaliações")


def mapa_calor(data):
    cols = ["Nota", "N_Avaliações", "Desconto", "Preço", "Qtd_Vendidos_Cod"]
    corr = data[cols].corr()
    labels = {
        "Nota": "Nota",
        "N_Avaliações": "Avaliações",
        "Desconto": "Desconto",
        "Preço": "Preço",
        "Qtd_Vendidos_Cod": "Vendas (cod.)",
    }
    corr.index = [labels.get(x, x) for x in corr.index]
    corr.columns = [labels.get(x, x) for x in corr.columns]

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
    )
    return apply_layout(fig, "Mapa de Calor das Correlações", None, None)


def barras(data):
    top = data["Marca"].value_counts().head(10).sort_values(ascending=True)
    barra_df = top.rename_axis("Marca").reset_index(name="Quantidade")
    fig = px.bar(
        barra_df,
        x="Quantidade",
        y="Marca",
        orientation="h",
        text="Quantidade",
        labels={"Quantidade": "Quantidade de Produtos", "Marca": "Marca"},
    )
    fig.update_traces(textposition="outside")
    return apply_layout(fig, "10 Marcas com Maior Quantidade de Produtos", "Quantidade de Produtos", "Marca")


def pizza(data):
    contagem = data["Gênero"].value_counts().reset_index()
    contagem.columns = ["Gênero", "Quantidade"]
    fig = px.pie(
        contagem,
        names="Gênero",
        values="Quantidade",
        hole=0.35,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return apply_layout(fig, "Distribuição dos Produtos por Gênero")


def densidade(data):
    # Estimativa de densidade suavizada usando apenas NumPy.
    valores = data["Preço"].dropna().to_numpy(dtype=float)
    if len(valores) < 3 or np.std(valores) == 0:
        return empty_figure("Dados insuficientes para calcular a densidade.")

    x = np.linspace(valores.min(), valores.max(), 300)
    desvio = np.std(valores, ddof=1)
    largura = 1.06 * desvio * (len(valores) ** (-1 / 5))
    largura = max(largura, (valores.max() - valores.min()) / 100)

    z = (x[:, None] - valores[None, :]) / largura
    y = np.exp(-0.5 * z**2).sum(axis=1) / (len(valores) * largura * np.sqrt(2 * np.pi))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            name="Densidade",
            hovertemplate="Preço: R$ %{x:.2f}<br>Densidade: %{y:.4f}<extra></extra>",
        )
    )
    fig.add_vline(
        x=data["Preço"].mean(),
        line_dash="dash",
        annotation_text=f"Média: R$ {data['Preço'].mean():.2f}",
        annotation_position="top right",
    )
    return apply_layout(fig, "Densidade dos Preços dos Produtos", "Preço (R$)", "Densidade")


def regressao(data):
    x = data["N_Avaliações"].to_numpy()
    y = data["Qtd_Vendidos_Cod"].to_numpy()

    if len(data) < 2 or np.all(x == x[0]):
        return empty_figure("Dados insuficientes para calcular a regressão.")

    coef = np.polyfit(x, y, 1)
    modelo = np.poly1d(coef)
    y_prev = modelo(x)

    ss_res = np.sum((y - y_prev) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

    ordem = np.argsort(x)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Produtos",
            hovertemplate="Avaliações: %{x}<br>Vendas (cod.): %{y}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x[ordem],
            y=y_prev[ordem],
            mode="lines",
            name=f"Regressão (R² = {r2:.2f})",
        )
    )

    fig = apply_layout(
        fig,
        f"Regressão: Avaliações × Vendas (R² = {r2:.2f})",
        "Número de Avaliações",
        "Quantidade de Vendas (cod.)",
    )
    return fig


# ==========================================================
# 3. APLICAÇÃO DASH
# ==========================================================
app = Dash(__name__)
app.title = "Dashboard Ecommerce"

opcoes_genero = [{"label": "Todos", "value": "Todos"}] + [
    {"label": valor, "value": valor}
    for valor in sorted(df["Gênero"].dropna().unique())
]
opcoes_temporada = [{"label": "Todos", "value": "Todos"}] + [
    {"label": valor, "value": valor}
    for valor in sorted(df["Temporada"].dropna().unique())
]


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Dashboard de E-commerce", className="titulo"),
                html.P(
                    "Análise exploratória de produtos, preços, avaliações, descontos e vendas.",
                    className="subtitulo",
                ),
            ],
            className="cabecalho",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Gênero", className="label-filtro"),
                        dcc.Dropdown(
                            id="filtro-genero",
                            options=opcoes_genero,
                            value="Todos",
                            clearable=False,
                        ),
                    ],
                    className="filtro",
                ),
                html.Div(
                    [
                        html.Label("Temporada", className="label-filtro"),
                        dcc.Dropdown(
                            id="filtro-temporada",
                            options=opcoes_temporada,
                            value="Todos",
                            clearable=False,
                        ),
                    ],
                    className="filtro",
                ),
            ],
            className="filtros",
        ),
        html.Div(
            [
                html.Div([html.Div("Produtos analisados", className="kpi-label"), html.Div(id="kpi-produtos", className="kpi-value")], className="kpi-card"),
                html.Div([html.Div("Preço médio", className="kpi-label"), html.Div(id="kpi-preco", className="kpi-value")], className="kpi-card"),
                html.Div([html.Div("Nota média", className="kpi-label"), html.Div(id="kpi-nota", className="kpi-value")], className="kpi-card"),
                html.Div([html.Div("Avaliações médias", className="kpi-label"), html.Div(id="kpi-avaliacoes", className="kpi-value")], className="kpi-card"),
            ],
            className="kpis",
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id="grafico-histograma"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-dispersao"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-calor"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-barras"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-pizza"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-densidade"), className="grafico-card"),
                html.Div(dcc.Graph(id="grafico-regressao"), className="grafico-card grafico-largo"),
            ],
            className="grade-graficos",
        ),
        html.Footer(
            "Projeto de análise de dados — Dashboard desenvolvido com Dash, Plotly e Pandas.",
            className="rodape",
        ),
    ],
    className="pagina",
)


@app.callback(
    Output("kpi-produtos", "children"),
    Output("kpi-preco", "children"),
    Output("kpi-nota", "children"),
    Output("kpi-avaliacoes", "children"),
    Output("grafico-histograma", "figure"),
    Output("grafico-dispersao", "figure"),
    Output("grafico-calor", "figure"),
    Output("grafico-barras", "figure"),
    Output("grafico-pizza", "figure"),
    Output("grafico-densidade", "figure"),
    Output("grafico-regressao", "figure"),
    Input("filtro-genero", "value"),
    Input("filtro-temporada", "value"),
)
def atualizar_dashboard(genero, temporada):
    data = filter_data(genero, temporada)

    if data.empty:
        mensagem = "Sem dados"
        vazio = empty_figure()
        return mensagem, mensagem, mensagem, mensagem, vazio, vazio, vazio, vazio, vazio, vazio, vazio

    return (
        f"{len(data):,}".replace(",", "."),
        f"R$ {data['Preço'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        f"{data['Nota'].mean():.2f}",
        f"{data['N_Avaliações'].mean():,.0f}".replace(",", "."),
        histograma(data),
        dispersao(data),
        mapa_calor(data),
        barras(data),
        pizza(data),
        densidade(data),
        regressao(data),
    )


if __name__ == "__main__":
    app.run(debug=True, port=8050)
