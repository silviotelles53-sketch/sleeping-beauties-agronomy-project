from pathlib import Path

import pandas as pd


# --------------------------------------------------
# CAMINHOS
# --------------------------------------------------

ARQUIVO_RESULTADOS = (
    Path("resultados")
    / "resultados_formula_ke.csv"
)

ARQUIVO_SAIDA = (
    Path("resultados")
    / "estatisticas_descritivas_formula_ke.csv"
)


# --------------------------------------------------
# CARREGAR RESULTADOS
# --------------------------------------------------

if not ARQUIVO_RESULTADOS.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {ARQUIVO_RESULTADOS.resolve()}"
    )

dados = pd.read_csv(ARQUIVO_RESULTADOS)

print("Calculando estatísticas descritivas...")


# --------------------------------------------------
# IDENTIFICAR ARTIGOS IMPORTANTES
# --------------------------------------------------

artigo_maior_bc = dados.loc[
    dados["Beauty Coefficient"].idxmax()
]

artigo_menor_bc = dados.loc[
    dados["Beauty Coefficient"].idxmin()
]

artigo_maior_despertar = dados.loc[
    dados["Awakening time"].idxmax()
]

artigo_maior_pico = dados.loc[
    dados["Citacoes no pico"].idxmax()
]


# --------------------------------------------------
# CONTAGENS DO BEAUTY COEFFICIENT
# --------------------------------------------------

bc_negativos = (
    dados["Beauty Coefficient"] < 0
).sum()

bc_iguais_zero = (
    dados["Beauty Coefficient"] == 0
).sum()

bc_positivos = (
    dados["Beauty Coefficient"] > 0
).sum()


# --------------------------------------------------
# CRIAR TABELA DESCRITIVA
# --------------------------------------------------

indicadores = [
    ("Quantidade de artigos", len(dados)),

    (
        "Média do Beauty Coefficient",
        dados["Beauty Coefficient"].mean(),
    ),
    (
        "Mediana do Beauty Coefficient",
        dados["Beauty Coefficient"].median(),
    ),
    (
        "Desvio-padrão do Beauty Coefficient",
        dados["Beauty Coefficient"].std(),
    ),
    (
        "Menor Beauty Coefficient",
        artigo_menor_bc["Beauty Coefficient"],
    ),
    (
        "Artigo com menor Beauty Coefficient",
        artigo_menor_bc["Title"],
    ),
    (
        "Maior Beauty Coefficient",
        artigo_maior_bc["Beauty Coefficient"],
    ),
    (
        "Artigo com maior Beauty Coefficient",
        artigo_maior_bc["Title"],
    ),

    ("Artigos com BC negativo", bc_negativos),
    ("Artigos com BC igual a zero", bc_iguais_zero),
    ("Artigos com BC positivo", bc_positivos),

    (
        "Média do tempo até o pico",
        dados["Tempo ate o pico"].mean(),
    ),
    (
        "Mediana do tempo até o pico",
        dados["Tempo ate o pico"].median(),
    ),
    (
        "Maior tempo até o pico",
        dados["Tempo ate o pico"].max(),
    ),

    (
        "Média do Awakening Time",
        dados["Awakening time"].mean(),
    ),
    (
        "Mediana do Awakening Time",
        dados["Awakening time"].median(),
    ),
    (
        "Maior Awakening Time",
        artigo_maior_despertar["Awakening time"],
    ),
    (
        "Artigo com maior Awakening Time",
        artigo_maior_despertar["Title"],
    ),

    (
        "Média de citações no pico",
        dados["Citacoes no pico"].mean(),
    ),
    (
        "Mediana de citações no pico",
        dados["Citacoes no pico"].median(),
    ),
    (
        "Maior número de citações no pico",
        artigo_maior_pico["Citacoes no pico"],
    ),
    (
        "Artigo com maior número de citações no pico",
        artigo_maior_pico["Title"],
    ),

    (
        "Ano de publicação mais antigo",
        dados["Publication Year"].min(),
    ),
    (
        "Ano de publicação mais recente",
        dados["Publication Year"].max(),
    ),
]


# Incluir citações totais somente se essa coluna existir
if "Total Citations" in dados.columns:
    indicadores.extend([
        (
            "Média de citações totais",
            dados["Total Citations"].mean(),
        ),
        (
            "Mediana de citações totais",
            dados["Total Citations"].median(),
        ),
        (
            "Maior número de citações totais",
            dados["Total Citations"].max(),
        ),
    ])


tabela_descritiva = pd.DataFrame(
    indicadores,
    columns=["Indicador", "Valor"],
)


# --------------------------------------------------
# SALVAR E MOSTRAR
# --------------------------------------------------

tabela_descritiva.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig",
)

print("\nEstatísticas descritivas:")
print(
    tabela_descritiva.to_string(index=False)
)

print(
    f"\nTabela salva em:\n{ARQUIVO_SAIDA.resolve()}"
)
