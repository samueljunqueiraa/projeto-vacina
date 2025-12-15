# -----------------------------------------------------------------------
# 1. IMPORTS NECESSÁRIOS (DEVE FICAR NO TOPO!)
# -----------------------------------------------------------------------
import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import streamlit_folium as st_folium

# -----------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (A navegação é criada automaticamente)

# -----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Priorização de Surto - Machado/MG",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------
# 3. APRESENTAÇÃO DO PROJETO E FÓRMULA HEURÍSTICA
# -----------------------------------------------------------------------

st.title("Dashboard de Priorização de Risco de Surto - Machado/MG")
st.markdown("### 🎯 Heurística de Priorização em Saúde Pública")

st.markdown("""
O problema consiste em determinar quais **Setores Censitários** devem ser priorizados nas campanhas de vacinação (foco em doenças imunopreveníveis, como a **Influenza/SRAG**), de modo a maximizar a cobertura vacinal e reduzir a propagação de surtos.

Este projeto propõe uma **Heurística de Priorização** para auxiliar gestores de saúde a alocar recursos de forma estratégica em áreas de maior vulnerabilidade demográfica e de menor proteção vacinal.
""")

st.markdown("---")

st.header("1. Objetivo Principal")

st.markdown("""
O objetivo central é fornecer uma **ferramenta de apoio à decisão** que mapeia e classifica os Setores Censitários de Machado (MG) por ordem de **risco de surto**. Essa classificação serve como base para o planejamento e execução de campanhas de vacinação mais eficazes e direcionadas.
""")

st.header("2. Fórmula da Heurística")

st.markdown(r"""
A Pontuação de Prioridade ($P_s$) é o resultado da ponderação de três fatores essenciais: a Demografia de Risco no local, a Vulnerabilidade Vacinal do município, e a Incidência Média da doença.

$$\mathbf{P_s = I \times D_{Pop_s} \times (1 - C_{Vac})}$$
""")


st.header("3. Variáveis e Fontes de Dados")

st.markdown("A heurística utiliza dados de fontes públicas e confiáveis, conforme detalhado abaixo:")

st.subheader("3.1. Variáveis por Setor Censitário ($\mathbf{D_{Pop_s}}$ e $\mathbf{P_s}$)")
st.markdown("""
* **$D_{Pop_s}$ (Demografia / População de Risco):**
    * **O que é:** Representa a população residente no Setor Censitário que se enquadra nos grupos de maior risco para complicações da doença (crianças, idosos, portadores de comorbidades).
    * **Fonte:** Instituto Brasileiro de Geografia e Estatística (IBGE) - **Censo 2022** (dados desagregados por Setor Censitário).
    * **Representação:** É a principal **variável por setor** que impulsiona a pontuação no ranking.

* **$P_s$ (Pontuação de Prioridade):**
    * **O que é:** O valor final da fórmula. Quanto maior a pontuação, maior a prioridade do Setor Censitário no Ranking.
""")

st.subheader("3.2. Variáveis Constantes (Aplicáveis a todo o Município)")
st.markdown("""
* **$I$ (Incidência Média da Doença):**
    * **O que é:** A média da taxa de incidência da doença (SRAG/Influenza) em Machado em um período recente.
    * **Fonte:** Sistema de Informação de Vigilância Epidemiológica da Gripe (**SIVEP-Gripe**) - Dados Epidemiológicos de SRAG.
    * **Representação:** Constante utilizada para modular a pontuação com base no risco epidemiológico atual da cidade.

* **$(1 - C_{Vac})$ (Vulnerabilidade Vacinal):**
    * **O que é:** A vulnerabilidade do município à doença, calculada como $1 - \text{Cobertura Vacinal}$ ($C_{Vac}$). Uma cobertura baixa resulta em alta vulnerabilidade.
    * **Fonte:** Sistema de Informação do Programa Nacional de Imunizações (**INFOMS**) - Cobertura Vacinal da Influenza.
    * **Representação:** Constante utilizada para ponderar o risco demográfico pela proteção geral da população.
""")

st.markdown("---")

# -----------------------------------------------------------------------
# 4. INÍCIO DO CÓDIGO FUNCIONAL (CARREGAMENTO DOS DADOS)
# -----------------------------------------------------------------------

# 2. Carregar os Dados (GeoJSON)
# Carrega o GeoJSON (agora ele já tem a geometria e os dados de prioridade)
try:
    gdf_machado = gpd.read_file("dados/machado_prioridade.geojson")
except Exception as e:
    st.error(f"Erro ao carregar o GeoJSON: Verifique se o arquivo está em 'dados/machado_prioridade.geojson'. Detalhe: {e}")
    st.stop()


# 3. Exibir Conteúdo Funcional (Ranking e Mapa)
# ... A lógica do ranking e mapa virá aqui ...

# ... Adicione o código do ranking de volta aqui, dentro de uma estrutura que separe o conteúdo...