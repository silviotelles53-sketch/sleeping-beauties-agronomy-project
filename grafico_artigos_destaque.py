from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator


# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

ARQUIVO_DADOS = Path("data") / "data_piloto_agronomy_corrigido.txt"

ARQUIVO_RESULTADOS = (
    Path("resultados")
    / "resultados_formula_ke.csv"
)

PASTA_SAIDA = (
    Path("graficos")
    / "artigos_destaque"
)

ANO_FINAL_CITACOES = 2025


# Trechos dos títulos usados para localizar os artigos
ARTIGOS_DESTAQUE = {
    "maior_pico_citacoes": (
        "Nutrient availability and leaching in an "
        "archaeological Anthrosol"
    ),
    "maior_awakening_time": (
        "Some factors affecting fat-content in cacao beans"
    ),
}


# --------------------------------------------------
# FUNÇÕES
# --------------------------------------------------

def limpar_nome_arquivo(texto):
    """Remove caracteres inválidos do nome do arquivo."""

    texto = re.sub(
        r'[<>:"/\\|?*]',
        "",
        str(texto),
    )

    return texto.strip()[:90]


def localizar_resultado(resultados, trecho_titulo):
    """Localiza o artigo na tabela de resultados."""

    encontrados = resultados[
        resultados["Title"]
        .astype(str)
        .str.contains(
            trecho_titulo,
            case=False,
            regex=False,
            na=False,
        )
    ]

    if encontrados.empty:
        raise ValueError(
            "Artigo não encontrado nos resultados:\n"
            f"{trecho_titulo}"
        )

    return encontrados.iloc[0]


def localizar_artigo_original(dados, resultado):
    """
    Localiza o artigo na base original.

    Usa DOI quando disponível. Caso contrário,
    utiliza título e ano de publicação.
    """

    doi = resultado["DOI"]

    if pd.notna(doi) and str(doi).strip():
        encontrados = dados[
            dados["DOI"].astype(str).str.strip()
            == str(doi).strip()
        ]

        if not encontrados.empty:
            return encontrados.iloc[0]

    encontrados = dados[
        (
            dados["Title"].astype(str).str.strip()
            == str(resultado["Title"]).strip()
        )
        & (
            dados["Publication Year"]
            == int(resultado["Publication Year"])
        )
    ]

    if encontrados.empty:
        raise ValueError(
            "Artigo não encontrado na base original:\n"
            f"{resultado['Title']}"
        )

    return encontrados.iloc[0]


def obter_curva_citacoes(artigo):
    """Obtém as citações anuais da publicação até 2025."""

    ano_publicacao = int(
        artigo["Publication Year"]
    )

    anos = list(
        range(
            ano_publicacao,
            ANO_FINAL_CITACOES + 1,
        )
    )

    citacoes = []

    for ano in anos:
        valor = pd.to_numeric(
            artigo[str(ano)],
            errors="coerce",
        )

        if pd.isna(valor):
            valor = 0

        citacoes.append(int(valor))

    return anos, citacoes


def criar_grafico(resultado, artigo, identificador):
    """Cria o gráfico individual do artigo."""

    anos, citacoes = obter_curva_citacoes(
        artigo
    )

    ano_publicacao = int(
        resultado["Publication Year"]
    )

    ano_despertar = int(
        resultado["Ano do despertar"]
    )

    ano_pico = int(
        resultado["Ano do pico"]
    )

    awakening_time = int(
        resultado["Awakening time"]
    )

    citacoes_pico = int(
        resultado["Citacoes no pico"]
    )

    beauty_coefficient = float(
        resultado["Beauty Coefficient"]
    )

    plt.figure(figsize=(12, 7))

    plt.plot(
        anos,
        citacoes,
        marker="o",
        linewidth=1.8,
        label="Citações anuais",
    )

    plt.axvline(
        ano_despertar,
        linestyle="--",
        linewidth=1.5,
        label=(
            f"Despertar: {ano_despertar} "
            f"({awakening_time} anos)"
        ),
    )

    plt.axvline(
        ano_pico,
        linestyle=":",
        linewidth=1.8,
        label=(
            f"Pico: {ano_pico} "
            f"({citacoes_pico} citações)"
        ),
    )

    plt.scatter(
        ano_pico,
        citacoes_pico,
        zorder=3,
    )

    plt.xlabel("Ano")
    plt.ylabel("Número de citações")

    plt.title(
        f"{resultado['Title']}\n"
        f"Ano de publicação: {ano_publicacao} | "
        f"Beauty Coefficient: {beauty_coefficient:.2f}"
    )

    # Mantém os valores do eixo X como anos inteiros
    plt.gca().xaxis.set_major_locator(
        MaxNLocator(
            integer=True,
            nbins=12,
        )
    )

    plt.grid(
        alpha=0.3,
        linestyle="--",
    )

    plt.legend()
    plt.tight_layout()

    nome_titulo = limpar_nome_arquivo(
        resultado["Title"]
    )

    arquivo_saida = (
        PASTA_SAIDA
        / f"{identificador}_{nome_titulo}.png"
    )

    plt.savefig(
        arquivo_saida,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Gráfico criado: {arquivo_saida}")


# --------------------------------------------------
# CARREGAR OS ARQUIVOS
# --------------------------------------------------

print("Carregando os dados...")

if not ARQUIVO_DADOS.exists():
    raise FileNotFoundError(
        f"Base não encontrada: "
        f"{ARQUIVO_DADOS.resolve()}"
    )

if not ARQUIVO_RESULTADOS.exists():
    raise FileNotFoundError(
        f"Resultados não encontrados: "
        f"{ARQUIVO_RESULTADOS.resolve()}"
    )

dados = pd.read_csv(
    ARQUIVO_DADOS,
    sep="\t",
    encoding="utf-16",
    low_memory=False,
)

resultados = pd.read_csv(
    ARQUIVO_RESULTADOS,
)

dados["Publication Year"] = pd.to_numeric(
    dados["Publication Year"],
    errors="coerce",
)

PASTA_SAIDA.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# GERAR OS DOIS GRÁFICOS
# --------------------------------------------------

for identificador, trecho_titulo in ARTIGOS_DESTAQUE.items():

    resultado = localizar_resultado(
        resultados,
        trecho_titulo,
    )

    artigo = localizar_artigo_original(
        dados,
        resultado,
    )

    criar_grafico(
        resultado,
        artigo,
        identificador,
    )


print("\nOs dois gráficos foram concluídos.")
print(f"Arquivos salvos em: {PASTA_SAIDA.resolve()}")