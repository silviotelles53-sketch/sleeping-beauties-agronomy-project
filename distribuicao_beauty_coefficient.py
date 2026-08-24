from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# CAMINHOS
# --------------------------------------------------

ARQUIVO_RESULTADOS = (
    Path("resultados")
    / "resultados_formula_ke.csv"
)

PASTA_GRAFICOS = (
    Path("graficos")
    / "distribuicao_bc"
)

ARQUIVO_FAIXAS = (
    Path("resultados")
    / "distribuicao_faixas_bc.csv"
)


# --------------------------------------------------
# CARREGAR OS RESULTADOS
# --------------------------------------------------

if not ARQUIVO_RESULTADOS.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: "
        f"{ARQUIVO_RESULTADOS.resolve()}"
    )

dados = pd.read_csv(
    ARQUIVO_RESULTADOS
)

dados["Beauty Coefficient"] = pd.to_numeric(
    dados["Beauty Coefficient"],
    errors="coerce",
)

dados = dados.dropna(
    subset=["Beauty Coefficient"]
).copy()

PASTA_GRAFICOS.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# ESTATÍSTICAS GERAIS
# --------------------------------------------------

bc = dados["Beauty Coefficient"]

media = bc.mean()
mediana = bc.median()
minimo = bc.min()
maximo = bc.max()

q1 = bc.quantile(0.25)
q3 = bc.quantile(0.75)

intervalo_interquartil = q3 - q1

limite_inferior = (
    q1 - 1.5 * intervalo_interquartil
)

limite_superior = (
    q3 + 1.5 * intervalo_interquartil
)

quantidade_outliers = (
    (bc < limite_inferior)
    | (bc > limite_superior)
).sum()


print(
    "Calculando a distribuição "
    "do Beauty Coefficient..."
)


# --------------------------------------------------
# CLASSIFICAR OS ARTIGOS POR FAIXA DE BC
# --------------------------------------------------

def classificar_bc(valor):

    if valor < 0:
        return "BC < 0"

    if valor < 5:
        return "0 ≤ BC < 5"

    if valor < 10:
        return "5 ≤ BC < 10"

    if valor < 20:
        return "10 ≤ BC < 20"

    if valor < 50:
        return "20 ≤ BC < 50"

    return "BC ≥ 50"


dados["Faixa de BC"] = (
    dados["Beauty Coefficient"]
    .apply(classificar_bc)
)


ordem_faixas = [
    "BC < 0",
    "0 ≤ BC < 5",
    "5 ≤ BC < 10",
    "10 ≤ BC < 20",
    "20 ≤ BC < 50",
    "BC ≥ 50",
]


# --------------------------------------------------
# CALCULAR FREQUÊNCIAS
# --------------------------------------------------

quantidades = (
    dados["Faixa de BC"]
    .value_counts()
    .reindex(
        ordem_faixas,
        fill_value=0,
    )
)


medias_por_faixa = (
    dados.groupby(
        "Faixa de BC",
        observed=False,
    )["Beauty Coefficient"]
    .mean()
    .reindex(
        ordem_faixas
    )
)


tabela_faixas = pd.DataFrame({
    "Faixa de BC": ordem_faixas,
    "Quantidade de artigos": quantidades.values,
    "Percentual": (
        quantidades.values
        / len(dados)
        * 100
    ),
    "BC médio da faixa": medias_por_faixa.values,
})


tabela_faixas["Percentual"] = (
    tabela_faixas["Percentual"]
    .round(2)
)

tabela_faixas["BC médio da faixa"] = (
    tabela_faixas["BC médio da faixa"]
    .round(2)
)


# --------------------------------------------------
# SALVAR TABELA DAS FAIXAS
# --------------------------------------------------

tabela_faixas.to_csv(
    ARQUIVO_FAIXAS,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# GERAR GRÁFICO DAS FAIXAS DE BC
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(11, 7)
)

barras = ax.barh(
    tabela_faixas["Faixa de BC"],
    tabela_faixas[
        "Quantidade de artigos"
    ],
)

ax.invert_yaxis()

ax.set_xlabel(
    "Quantidade de artigos"
)

ax.set_ylabel(
    "Faixa de Beauty Coefficient"
)

ax.set_title(
    "Distribuição dos artigos por faixa "
    "de Beauty Coefficient"
)


maior_quantidade = (
    tabela_faixas[
        "Quantidade de artigos"
    ].max()
)

ax.set_xlim(
    0,
    maior_quantidade * 1.25,
)


# --------------------------------------------------
# ADICIONAR QUANTIDADE E PERCENTUAL
# --------------------------------------------------

for barra, quantidade, percentual in zip(
    barras,
    tabela_faixas[
        "Quantidade de artigos"
    ],
    tabela_faixas[
        "Percentual"
    ],
):

    quantidade_formatada = (
        f"{quantidade:,}"
        .replace(",", ".")
    )

    percentual_formatado = (
        f"{percentual:.2f}"
        .replace(".", ",")
    )

    texto = (
        f"{quantidade_formatada} artigos "
        f"({percentual_formatado}%)"
    )

    ax.text(
        barra.get_width()
        + maior_quantidade * 0.015,
        barra.get_y()
        + barra.get_height() / 2,
        texto,
        va="center",
        fontsize=10,
    )


ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3,
)

fig.tight_layout()


# --------------------------------------------------
# SALVAR GRÁFICO
# --------------------------------------------------

arquivo_grafico = (
    PASTA_GRAFICOS
    / "distribuicao_faixas_bc.png"
)

fig.savefig(
    arquivo_grafico,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)


# --------------------------------------------------
# MOSTRAR RESULTADOS NO TERMINAL
# --------------------------------------------------

tabela_terminal = (
    tabela_faixas.copy()
)

tabela_terminal["Percentual"] = (
    tabela_terminal["Percentual"]
    .map(
        lambda valor:
        f"{valor:.2f}%"
        .replace(".", ",")
    )
)

tabela_terminal[
    "BC médio da faixa"
] = (
    tabela_terminal[
        "BC médio da faixa"
    ]
    .map(
        lambda valor:
        f"{valor:.2f}"
        .replace(".", ",")
    )
)


print(
    "\nDistribuição por faixas "
    "de Beauty Coefficient:"
)

print(
    tabela_terminal.to_string(
        index=False
    )
)


print("\nResumo geral:")

print(
    f"Média do BC: "
    f"{media:.2f}"
    .replace(".", ",")
)

print(
    f"Mediana do BC: "
    f"{mediana:.2f}"
    .replace(".", ",")
)

print(
    f"Quantidade de valores extremos: "
    f"{quantidade_outliers}"
)


print(
    f"\nTabela salva em:\n"
    f"{ARQUIVO_FAIXAS.resolve()}"
)

print(
    f"\nGráfico salvo em:\n"
    f"{arquivo_grafico.resolve()}"
)

print("\nAnálise concluída.")