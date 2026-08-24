from pathlib import Path

import pandas as pd


# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

ARQUIVO = (
    Path("data")
    / "data_piloto_agronomy_corrigido.txt"
)

ANO_FINAL_CITACOES = 2025

COLUNAS_OBRIGATORIAS = [
    "Title",
    "DOI",
    "Publication Year",
    "Total Citations",
]


# --------------------------------------------------
# CARREGAMENTO DA BASE
# --------------------------------------------------

print("Verificando base...\n")

if not ARQUIVO.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: "
        f"{ARQUIVO.resolve()}"
    )

dados = pd.read_csv(
    ARQUIVO,
    sep="\t",
    encoding="utf-16",
    low_memory=False,
)

print(
    f"Arquivo analisado: "
    f"{ARQUIVO.resolve()}"
)

print(
    f"Quantidade de registros: "
    f"{len(dados)}"
)

print(
    f"Número de colunas: "
    f"{len(dados.columns)}"
)


# --------------------------------------------------
# COLUNAS OBRIGATÓRIAS
# --------------------------------------------------

print("\nColunas obrigatórias:")

colunas_ausentes = []

for coluna in COLUNAS_OBRIGATORIAS:

    if coluna in dados.columns:
        print(f"✔ {coluna}")

    else:
        print(f"✘ {coluna}")
        colunas_ausentes.append(coluna)


if colunas_ausentes:
    raise ValueError(
        "A base não possui todas as colunas "
        "necessárias para a análise."
    )


# --------------------------------------------------
# ANO DE PUBLICAÇÃO
# --------------------------------------------------

print("\nVerificando anos de publicação...")

anos_numericos = pd.to_numeric(
    dados["Publication Year"],
    errors="coerce",
)

anos_invalidos = anos_numericos.isna()

quantidade_anos_invalidos = (
    anos_invalidos.sum()
)

print(
    f"Registros sem ano válido: "
    f"{quantidade_anos_invalidos}"
)

if quantidade_anos_invalidos > 0:

    print("\nRegistros com problema no ano:")

    print(
        dados.loc[
            anos_invalidos,
            [
                "Title",
                "Publication Year",
                "DOI",
            ],
        ].to_string(index=False)
    )

else:

    print(
        "Todos os registros possuem "
        "ano de publicação válido."
    )


# --------------------------------------------------
# COLUNAS ANUAIS DE CITAÇÕES
# --------------------------------------------------

print("\nVerificando colunas anuais de citações...")

if quantidade_anos_invalidos == 0:

    primeiro_ano = int(
        anos_numericos.min()
    )

    anos_esperados = [
        str(ano)
        for ano in range(
            primeiro_ano,
            ANO_FINAL_CITACOES + 1,
        )
    ]

    colunas_citacoes_ausentes = [
        ano
        for ano in anos_esperados
        if ano not in dados.columns
    ]

    if colunas_citacoes_ausentes:

        print(
            "Colunas anuais ausentes:"
        )

        print(
            ", ".join(
                colunas_citacoes_ausentes
            )
        )

    else:

        print(
            f"Todas as colunas anuais entre "
            f"{primeiro_ano} e "
            f"{ANO_FINAL_CITACOES} estão presentes."
        )


# --------------------------------------------------
# DOI DUPLICADO
# --------------------------------------------------

print("\nVerificando DOIs duplicados...")

dois = (
    dados["DOI"]
    .fillna("")
    .astype(str)
    .str.strip()
)

dois_validos = dados[
    dois != ""
].copy()

dois_validos["DOI_auditoria"] = (
    dois[dois != ""]
    .str.lower()
)

dois_duplicados = dois_validos[
    dois_validos[
        "DOI_auditoria"
    ].duplicated(
        keep=False
    )
].copy()

print(
    f"DOIs válidos: "
    f"{len(dois_validos)}"
)

print(
    f"Registros com DOI repetido: "
    f"{len(dois_duplicados)}"
)

if not dois_duplicados.empty:

    print("\nRegistros com DOI repetido:")

    print(
        dois_duplicados[
            [
                "Title",
                "Publication Year",
                "DOI",
                "Source Title",
                "Volume",
                "Beginning Page",
                "Ending Page",
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# TÍTULOS DUPLICADOS
# --------------------------------------------------

print("\nVerificando títulos duplicados...")

titulos_normalizados = (
    dados["Title"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

titulos_duplicados = dados[
    titulos_normalizados.duplicated(
        keep=False
    )
].copy()

print(
    f"Registros com título repetido: "
    f"{len(titulos_duplicados)}"
)

if not titulos_duplicados.empty:

    print("\nRegistros com título repetido:")

    print(
        titulos_duplicados[
            [
                "Title",
                "Publication Year",
                "DOI",
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# RESUMO FINAL
# --------------------------------------------------

print("\n----------------------------------")
print("RESUMO DA AUDITORIA")
print("----------------------------------")

print(
    f"Registros: {len(dados)}"
)

print(
    f"Colunas: {len(dados.columns)}"
)

print(
    f"Anos inválidos: "
    f"{quantidade_anos_invalidos}"
)

print(
    f"Registros com DOI repetido: "
    f"{len(dois_duplicados)}"
)

print(
    f"Registros com título repetido: "
    f"{len(titulos_duplicados)}"
)

print("\nFim da verificação.")