# 🥊 UFC Data Analytics: Engenharia de Dados e Evolução Tática do Octógono

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-%234E79A7.svg?style=for-the-badge&logo=analytics&logoColor=white)

Este repositório sedia um projeto completo de Ciência de Dados e Análise Exploratória de Dados (EDA) aplicado ao histórico de lutas e atletas do **UFC (Ultimate Fighting Championship)**. 

Através do cruzamento de dados biométricos, métricas de performance minuto a minuto e desfechos de combates, este estudo reconstrói a história da organização. O objetivo é provar matematicamente como a transição regulatória, os contratos de mídia e a ciência esportiva transformaram um show caótico de "briga de estilos" nos anos 90 em um esporte altamente estratégico, previsível e bilionário de alta performance.

---

## 🎯 Objetivos Estratégicos do Projeto

* **Mapeamento de Tendências Temporais:** Avaliar como as alterações nas regras unificadas impactaram o ritmo e a duração média das lutas.
* **Validação de Hipóteses e Mitos do Esporte:** Testar estatisticamente se vantagens físicas natas (como alcance/envergadura e base canhota) superam fatores de carreira (como experiência e idade).
* **Análise Multivariada de Performance:** Identificar correlações entre volume de golpes significativos lançados, eficiência de quedas (*takedowns*) e o método de vitória.

---

## 🕒 O Framework Analítico: As 5 Eras Institucionais

Para garantir o rigor estatístico das análises, os dados históricos foram segmentados e contextualizados em **5 Eras Macroeconômicas e Regulatórias**:

1.  **No-Rules Era (1993 – 1997):** Período do "vale-tudo" original. Torneios sem divisões de peso, sem luvas obrigatórias, sem juízes laterais e sem limite de tempo. Foco absoluto no choque bruto de modalidades.
2.  **Dark Ages Era (1997 – 2000):** Fase de forte boicote político e banimento dos grandes canais de Pay-Per-View. Para evitar a falência, o UFC adota rounds e categorias de peso iniciais buscando regulamentação.
3.  **Zuffa Boom Era (2001 – 2010):** A compra da franquia pela Zuffa LLC (Dana White e irmãos Fertitta). Instituição das *Regras Unificadas do MMA*, explosão de vendas de PPV e lançamento do reality show *The Ultimate Fighter* (TUF).
4.  **Fox & USADA Era (2011 – 2018):** Fase de massificação midiática na TV aberta dos EUA. Introdução de uniformização corporativa exclusiva (Reebok) e implementação do programa de testes antidoping ultra-rigoroso da USADA.
5.  **Modern / ESPN Era (2019 – Presente):** Consolidação global via streaming com o grupo Disney/ESPN. Consolidação de eventos semanais, surgimento de centros de performance próprios (UFC PI) e atletas operando sob máxima preparação científica.

---

## 🏗️ Pipeline e Engenharia de Dados

O projeto conta com uma arquitetura de dados estruturada sequencialmente em scripts independentes para garantir modularidade e reprodutibilidade:

```text
[Dados Brutos] ──> [pipeline_dados.py] ──> [merge_dados.py] ──> [Datasets Finais] ──> [Geração de Gráficos]

PROJETO_UFC/
│
├── data/                                 # Datasets em diferentes estágios de processamento
│   ├── ufc_fighters_final.csv            # Perfil biométrico limpo dos atletas
│   ├── ufc_fights_merged_full.csv        # Tabela unificada (Lutas + Atletas) para análise
│   ├── ufc_fights_processed.csv          # Histórico de combates estruturado
│   ├── ufc_gold_dataset_final.csv        # Base consolidada de alta fidelidade
│   └── ufc_stats_per_min.csv             # Estatísticas de performance normalizadas por tempo
│
├── graphs/                               # Diretório de saída das visualizações (PNG)
│   ├── analise_stance.png                # Gráfico duplo de aproveitamento de bases
│   ├── box_plot_tempo_medio_por_eras.png # Boxplot de duração das lutas
│   ├── Evolucao_Categorias.png           # Linhas temporais de atividade de categorias
│   ├── Grafico_dispersao_era_sig_min_... # Scatter plot de golpes significativos vs quedas
│   ├── Grafico_Evolucao_Resultado_Era.png# Gráfico de barras de métodos de vitória por era
│   ├── heatmap_correlaçao.png            # Matriz de correlação de Pearson das variáveis
│   ├── idade_vs_experiencia_dark.png     # Gráfico duplo em Dark Mode (Transparente para Slides)
│   ├── idade_vs_experiencia.png          # Versão padrão do gráfico duplo de longevidade
│   └── mito_envergadura.png              # Gráfico de barras com a taxa de vitória do alcance
│
├── scripts/                              # Módulos em Python dedicados
│   ├── analise_stance.py                 # Processa e plota dados de postura tática
│   ├── box_plot.py                       # Gera a distribuição de tempo por eras
│   ├── idade_experiencia.py              # Script principal do conflito biológico de atletas
│   ├── merge_dados.py                    # Realiza o JOIN relacional das bases de dados
│   ├── methods_plot.py                   # Abstração de funções estéticas do Matplotlib
│   ├── mito_envergadura.py               # Calcula e isola a taxa de vitória por alcance
│   ├── pipeline_dados.py                 # Pipeline de ETL e limpeza de strings
│   ├── scatter_plot.py                   # Plota dispersões de performance por minuto
│   ├── stats.py                          # Cálculos de correlação e geração do Heatmap
│   └── weight_class_analysis.py          # Processa a evolução das divisões de peso
│
└── README.md                             # Documentação oficial do projeto

```bash
pip install pandas matplotlib seaborn numpy

# 1. Executar a pipeline de limpeza e unificação dos dados
python scripts/pipeline_dados.py
python scripts/merge_dados.py

# 2. Gerar as análises estatísticas e plots visuais
python scripts/box_plot.py
python scripts/mito_envergadura.py
python scripts/idade_experiencia.py
python scripts/analise_stance.py