import math


def calcular_beauty_coefficient(citacoes):
    """
    Calcula o Beauty Coefficient de Ke et al. (2015).

    A lista deve começar no ano de publicação do artigo. t=0 corresponde ao ano de publicação, t=1 ao ano seguinte, e assim por diante.
    C0 é o número de citações no ano de publicação do artigo. 
    """

    citacoes_pico = max(citacoes)
    tempo_pico = citacoes.index(citacoes_pico)
    c0 = citacoes[0]

    if tempo_pico == 0:
        return 0.0, tempo_pico, citacoes_pico

    beauty_coefficient = 0.0

    for t in range(tempo_pico + 1):
        ct = citacoes[t]

        linha_referencia = (
            ((citacoes_pico - c0) / tempo_pico) * t
            + c0
        )

        parcela = (
            linha_referencia - ct
        ) / max(1, ct)

        beauty_coefficient += parcela

    return (
        beauty_coefficient,
        tempo_pico,
        citacoes_pico,
    )


def calcular_awakening_time(citacoes):
    """
    Calcula o awakening time de Ke et al. (2015).
    """

    citacoes_pico = max(citacoes)
    tempo_pico = citacoes.index(citacoes_pico)
    c0 = citacoes[0]

    if tempo_pico == 0:
        return 0, 0.0

    denominador = math.sqrt(
        (citacoes_pico - c0) ** 2
        + tempo_pico ** 2
    )

    distancias = []

    for t in range(tempo_pico + 1):
        ct = citacoes[t]

        numerador = abs(
            (citacoes_pico - c0) * t
            - tempo_pico * ct
            + tempo_pico * c0
        )

        distancia = numerador / denominador
        distancias.append(distancia)

    awakening_time = distancias.index(
        max(distancias)
    )

    distancia_maxima = max(distancias)

    return awakening_time, distancia_maxima