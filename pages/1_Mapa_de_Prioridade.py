import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static
from pathlib import Path

# --- Configuração da Página ---
st.set_page_config(
    page_title="Mapa de Prioridade",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Mapa de Priorização de Setores Censitários - Machado, MG")
st.markdown("Este mapa de calor exibe a **Pontuação de Prioridade ($P_s$)** de cada setor censitário para a campanha de vacinação. Setores com **cores mais escuras (Vermelho)** indicam **Maior Prioridade/Risco**.")
st.markdown("---")


# 1. Carregamento e Preparação dos Dados
# -------------------------------------
try:
    # CONSTRUÇÃO DO CAMINHO ABSOLUTO (À PROVA DE FALHAS):
    # base_path deve apontar para /workspaces/Projeto_Final_Vacina/
    base_path = Path(__file__).parent.parent 
    # geojson_path deve apontar para /workspaces/Projeto_Final_Vacina/dados/machado_prioridade.geojson
    geojson_path = base_path / "dados" / "machado_prioridade.geojson"

    
    gdf_machado = gpd.read_file(geojson_path)
    
    # Verificação de Carregamento (AJUDA DE DEBUG)
    if gdf_machado.empty:
        st.error("ERRO: O GeoJSON foi carregado, mas está vazio.")
        st.stop()

    # Garante que a coluna de pontuação seja numérica e que o CD_SETOR seja string
    gdf_machado['Pontuacao_Prioridade'] = pd.to_numeric(
        gdf_machado['Pontuacao_Prioridade'], errors='coerce'
    )
    gdf_machado['CD_SETOR'] = gdf_machado['CD_SETOR'].astype(str)
    
    # Remove linhas com valores NaN na pontuação, se houver
    gdf_machado.dropna(subset=['Pontuacao_Prioridade'], inplace=True)

except FileNotFoundError:
    st.error(f"ERRO DE ARQUIVO: O arquivo 'machado_prioridade.geojson' não foi encontrado no caminho: {geojson_path}")
    st.info("Verifique se o arquivo está na pasta '/dados' dentro do diretório principal.")
    st.stop()
except Exception as e:
    # Este é o bloco que provavelmente está sendo executado se o arquivo for encontrado, mas estiver corrompido
    st.error(f"Ocorreu um erro ao processar o GeoJSON (Verifique o Conteúdo): {e}")
    st.stop()


# 2. Definição da Coluna de Plotagem e Escala de Cores
# ----------------------------------------------------
# (O código de plotagem aqui é o mesmo, garantindo que ele só execute se o try for bem-sucedido)
column_to_plot = 'Pontuacao_Prioridade'

min_score = gdf_machado[column_to_plot].min()
max_score = gdf_machado[column_to_plot].max()

# Ajuste seguro para evitar erro de bins em dados com pouca variação
if min_score == max_score:
    bins = [min_score, max_score]
else:
    bins = list(gdf_machado[column_to_plot].quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0]))

colormap = folium.LinearColormap(['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'], 
                                 vmin=min_score, vmax=max_score)
colormap.caption = 'Pontuação de Prioridade (Maior Risco)'


# 3. Criação do Mapa Base (Folium)
# --------------------------------
center_lat = gdf_machado.geometry.centroid.y.mean()
center_lon = gdf_machado.geometry.centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=13, 
    tiles="cartodbpositron"
)

# 4. Adicionar a Camada GeoJSON com Mapa de Calor (Choropleth)
# -----------------------------------------------------------
folium.Choropleth(
    geo_data=gdf_machado,
    name='Mapa de Prioridade',
    data=gdf_machado,
    columns=['CD_SETOR', column_to_plot],
    key_on='feature.properties.CD_SETOR',
    fill_color='Reds',
    fill_opacity=0.8,
    line_opacity=0.5,
    legend_name='Pontuação de Prioridade (P_s)',
    bins=bins,
    highlight=True,
    style_function=lambda x: {
        'weight': 0.5, 
        'color': 'black',
        'fillOpacity': 0.8
    }
).add_to(m)

# 5. Adicionar Interatividade (Tooltip)
# -------------------------------------
style_function = lambda x: {
    'fillColor': colormap(x['properties']['Pontuacao_Prioridade']),
    'color': 'black',
    'weight': 0.1,
    'fillOpacity': 0.7
}

highlight_function = lambda x: {
    'fillColor': '#ffffff',
    'color': '#000000',
    'fillOpacity': 0.5,
    'weight': 0.8
}

tooltip = folium.features.GeoJsonTooltip(
    fields=['CD_SETOR', 'Ranking', 'D_Pop_Risco', 'Pontuacao_Prioridade'],
    aliases=['Setor Censitário:', 'Ranking (1=Mais Alto):', 'População de Risco (D_Pop_Risco):', 'Pontuação de Prioridade (P_s):'],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid grey;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800
)

folium.GeoJson(
    gdf_machado,
    style_function=style_function,
    tooltip=tooltip,
    highlight_function=highlight_function
).add_to(m)


# 6. Adicionar a Legenda
# ----------------------
colormap.add_to(m)

# 7. Exibir o Mapa no Streamlit
# -----------------------------
folium_static(m)

st.markdown("---")
st.info("""
**Detalhes das Colunas:**
* **CD_SETOR:** Código do Setor Censitário (IBGE).
* **Pontuação de Prioridade ($P_s$):** O valor calculado pela heurística (maior = mais risco).
* **Ranking:** Posição de prioridade (1 = Setor de maior prioridade).
* **D_Pop_Risco:** População de Risco no Setor (Demografia).
""")