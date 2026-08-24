from pathlib import Path

import pandas as pd

from formulas.formula_ke import (
    calcular_awakening_time,
    calcular_beauty_coefficient,
)


# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

ARQUIVO_DADOS = (
    Path("data")
    / "data_piloto_agronomy_corrigido.txt"
)

ANO_FINAL_CITACOES = 2025

# True: mantém somente artigos até o ano definido.
# False: utiliza todos os artigos presentes na base.
USAR_FILTRO_ANO = False
ANO_MAXIMO_PUBLICACAO = 2010


# --------------------------------------------------
# REGISTRO DUPLICADO CONFIRMADO
# --------------------------------------------------

TITULO_DUPLICADO = (
    "RATES AND HYDRAULICS OF INTERRILL EROSION "
    "UNDER DIFFERENT SLOPE AND MULCH"
)

ANO_DUPLICADO = 2009


# --------------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------------

print("Iniciando análise...")

if not ARQUIVO_DADOS.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: "
        f"{ARQUIVO_DADOS.resolve()}"
    )

dados = pd.read_csv(
    ARQUIVO_DADOS,
    sep="\t",
    encoding="utf-16",
    low_memory=False,
)

print(
    f"Registros carregados da base: "
    f"{len(dados)}"
)


# --------------------------------------------------
# PREPARAÇÃO DO ANO DE PUBLICAÇÃO
# --------------------------------------------------

dados["Publication Year"] = pd.to_numeric(
    dados["Publication Year"],
    errors="coerce",
)

quantidade_sem_ano = (
    dados["Publication Year"]
    .isna()
    .sum()
)

if quantidade_sem_ano > 0:
    print("\nRegistros sem ano de publicação:")

    print(
        dados.loc[
            dados["Publication Year"].isna(),
            ["Title", "DOI"],
        ].to_string(index=False)
    )

    raise ValueError(
        "Existem registros sem ano de publicação. "
        "Execute a auditoria da base antes da análise."
    )

dados["Publication Year"] = (
    dados["Publication Year"]
    .astype(int)
)


# --------------------------------------------------
# REMOVER DUPLICATA CONFIRMADA
# --------------------------------------------------

duplicados_confirmados = dados[
    (
        dados["Title"]
        .astype(str)
        .str.strip()
        .str.upper()
        == TITULO_DUPLICADO
    )
    & (
        dados["Publication Year"]
        == ANO_DUPLICADO
    )
].index

if len(duplicados_confirmados) == 2:
    # Mantém o primeiro registro e remove o segundo.
    dados = dados.drop(
        index=duplicados_confirmados[1]
    )

    print(
        "Duplicata confirmada removida: "
        f"{TITULO_DUPLICADO}"
    )

elif len(duplicados_confirmados) > 2:
    raise ValueError(
        "Foram encontrados mais de dois registros "
        "do artigo duplicado conhecido."
    )


# --------------------------------------------------
# FILTRO OPCIONAL POR ANO DE PUBLICAÇÃO
# --------------------------------------------------

if USAR_FILTRO_ANO:
    dados = dados[
        dados["Publication Year"]
        <= ANO_MAXIMO_PUBLICACAO
    ].copy()

    print(
        "Filtro por ano ativado: "
        f"publicações até "
        f"{ANO_MAXIMO_PUBLICACAO}."
    )

else:
    print(
        "Filtro por ano de publicação desativado."
    )


# --------------------------------------------------
# PREPARAÇÃO DAS COLUNAS DE CITAÇÕES
# --------------------------------------------------

ano_inicial_base = int(
    dados["Publication Year"].min()
)

anos_necessarios = [
    str(ano)
    for ano in range(
        ano_inicial_base,
        ANO_FINAL_CITACOES + 1,
    )
]

colunas_ausentes = [
    ano
    for ano in anos_necessarios
    if ano not in dados.columns
]

if colunas_ausentes:
    raise ValueError(
        "Colunas anuais de citações ausentes: "
        + ", ".join(colunas_ausentes)
    )

dados[anos_necessarios] = (
    dados[anos_necessarios]
    .apply(
        pd.to_numeric,
        errors="coerce",
    )
    .fillna(0)
)


# --------------------------------------------------
# PREPARAR OUTROS CAMPOS NUMÉRICOS
# --------------------------------------------------

for coluna in [
    "Total Citations",
    "Average per Year",
]:
    if coluna in dados.columns:
        dados[coluna] = pd.to_numeric(
            dados[coluna],
            errors="coerce",
        )


# --------------------------------------------------
# OBTER CITAÇÕES DO ARTIGO
# --------------------------------------------------

def obter_citacoes_do_artigo(artigo):
    """
    Retorna a série anual de citações entre
    o ano de publicação do artigo e 2025.

    O primeiro valor corresponde ao próprio
    ano de publicação:

    citacoes[0] = c0
    """

    ano_publicacao = int(
        artigo["Publication Year"]
    )

    anos = [
        str(ano)
        for ano in range(
            ano_publicacao,
            ANO_FINAL_CITACOES + 1,
        )
    ]

    citacoes = [
        int(artigo[ano])
        for ano in anos
    ]

    return anos, citacoes


# --------------------------------------------------
# APLICAR A METODOLOGIA DE KE ET AL. (2015)
# --------------------------------------------------

resultados = []

for _, artigo in dados.iterrows():

    anos, citacoes = (
        obter_citacoes_do_artigo(artigo)
    )

    beauty_coefficient, tempo_pico, citacoes_pico = (
        calcular_beauty_coefficient(
            citacoes
        )
    )

    awakening_time, distancia_maxima = (
        calcular_awakening_time(
            citacoes
        )
    )

    ano_publicacao = int(
        artigo["Publication Year"]
    )

    ano_pico = int(
        anos[tempo_pico]
    )

    ano_despertar = int(
        anos[awakening_time]
    )

    resultado = {
        "Title": artigo["Title"],
        "DOI": artigo["DOI"],
        "Publication Year": ano_publicacao,
        "Beauty Coefficient": beauty_coefficient,
        "Tempo ate o pico": tempo_pico,
        "Ano do pico": ano_pico,
        "Citacoes no pico": citacoes_pico,
        "Awakening time": awakening_time,
        "Ano do despertar": ano_despertar,
        "Distancia maxima": distancia_maxima,
    }

    # Mantém esses metadados se existirem na base.
    if "Total Citations" in dados.columns:
        resultado["Total Citations"] = (
            artigo["Total Citations"]
        )

    if "Average per Year" in dados.columns:
        resultado["Average per Year"] = (
            artigo["Average per Year"]
        )

    resultados.append(resultado)


# --------------------------------------------------
# CRIAR TABELA DE RESULTADOS
# --------------------------------------------------

tabela_resultados = pd.DataFrame(
    resultados
)

tabela_resultados = (
    tabela_resultados
    .sort_values(
        "Beauty Coefficient",
        ascending=False,
    )
    .reset_index(drop=True)
)


# --------------------------------------------------
# SALVAR RESULTADOS
# --------------------------------------------------

pasta_resultados = Path("resultados")

pasta_resultados.mkdir(
    parents=True,
    exist_ok=True,
)

arquivo_saida = (
    pasta_resultados
    / "resultados_formula_ke.csv"
)

tabela_resultados.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig",
)


# --------------------------------------------------
# RESUMO
# --------------------------------------------------

print("\nAnálise concluída.")

print(
    f"Artigos efetivamente analisados: "
    f"{len(tabela_resultados)}"
)

print(
    f"Resultado salvo em:\n"
    f"{arquivo_saida.resolve()}"
)