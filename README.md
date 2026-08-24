Este repositório reúne os códigos em Python desenvolvidos para um estudo piloto sobre a identificação e análise de Sleeping Beauties (SBs) em artigos científicos da categoria Agronomy da Web of Science (WoS).

Os códigos permitem calcular o Beauty Coefficient (B) e o Awakening Time com base na metodologia de Ke et al. (2015), além de produzir estatísticas descritivas, tabelas e gráficos utilizados na análise dos resultados.

O projeto e seus códigos encontram-se em fase de refinamento e validação para posterior aplicação na pesquisa definitiva.

### Metodologia

A identificação das Sleeping Beauties é realizada a partir do Beauty Coefficient proposto por Ke et al. (2015).

O indicador considera a trajetória anual de citações de cada artigo desde seu ano de publicação até o momento em que atinge seu maior número anual de citações. Também é calculado o Awakening Time, utilizado para identificar o momento de despertar do artigo em sua trajetória de citações.

Referência:

KE, Qing et al. Defining and identifying Sleeping Beauties in science. Proceedings of the National Academy of Sciences, v. 112, n. 24, p. 7426–7431, jun. 2015. DOI: 10.1073/pnas.1424329112.

### Estrutura do repositório

Os principais arquivos utilizados no estudo piloto são:

- `data_piloto_agronomy_corrigido.txt` — conjunto de dados utilizado na aplicação piloto.
- `verificar_base.py` — realiza verificações no conjunto de dados antes da análise.
- `main.py` — prepara os dados e aplica os cálculos do Beauty Coefficient e do Awakening Time.
- `formulas/formula_ke.py` — contém as funções utilizadas nos cálculos baseados em Ke et al. (2015).
- `estatisticas_descritivas.py` — produz as estatísticas descritivas dos indicadores obtidos.
- `graficos_tres_maiores_menores_bc.py` — gera as curvas de citações dos três artigos com maiores e menores valores de Beauty Coefficient.
- `grafico_Artigos_Destaque.py` — gera gráficos dos artigos destacados pelo Awakening Time e pelo maior pico anual de citações.
- `distribuicao_beauty_coefficient.py` — produz a distribuição dos artigos por faixas de Beauty Coefficient.

### Dados

O arquivo de dados utilizado na fase piloto do projeto está incluído neste repositório. Os dados foram obtidos a partir de registros da categoria Agronomy da Web of Science e incluem os metadados e as citações anuais utilizados nos cálculos.

### Bibliotecas utilizadas

Os códigos utilizam principalmente Python, pandas e Matplotlib, além de módulos da biblioteca padrão do Python, como pathlib, math e re.

### Uso de Inteligência Artificial

Ferramentas de inteligência artificial generativa foram utilizadas como apoio no desenvolvimento e na revisão dos scripts em Python, incluindo a organização dos códigos e a elaboração das visualizações.

O pesquisador permanece responsável pelas decisões metodológicas, revisão e validação dos códigos, interpretação dos resultados e conteúdo final da pesquisa.

O uso das ferramentas de IA e os prompts relevantes serão documentados nos procedimentos metodológicos da pesquisa.

### Status

Estudo piloto — códigos em fase de refinamento e validação.
