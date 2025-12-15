import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- Configuração da Página ---
st.set_page_config(
    page_title="Gráfico de Incidência SRAG",
    page_icon="📈",
    layout="wide"
)

# --- Título da Página ---
st.title("📈 Análise Temporal de Casos SRAG (2023-2024)")
st.caption("Evolução semanal dos casos de Síndrome Respiratória Aguda Grave (SRAG) em Machado, MG, utilizando dados do SIVEP-Gripe.")
st.markdown("---")


# 1. Carregamento e Preparação dos Dados
# -------------------------------------
try:
    # Constrói o caminho absoluto para o arquivo machado_srag_casos.csv
    # Path(__file__).parent.parent resolve para /workspaces/Projeto_Final_Vacina/
    base_path = Path(__file__).parent.parent 
    srag_path = base_path / "dados" / "machado_srag_casos.csv"
    
    df_srag = pd.read_csv(srag_path)

    # Preparação dos Dados para o Gráfico
    df_srag['DT_SIN_PRI'] = pd.to_datetime(df_srag['DT_SIN_PRI'], errors='coerce')
    df_srag.dropna(subset=['DT_SIN_PRI'], inplace=True)
    
    # Agrupamento semanal para o gráfico de linhas
    df_timeline = df_srag.set_index('DT_SIN_PRI').resample('W').size().reset_index(name='Casos')
    df_timeline.rename(columns={'DT_SIN_PRI': 'Data_Semanal'}, inplace=True)
    
except FileNotFoundError:
    st.error(f"ERRO: Arquivo de casos brutos não encontrado em: {srag_path}")
    st.info("Certifique-se de que o arquivo 'machado_srag_casos.csv' foi gerado e está na pasta '/dados'.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao processar dados de Incidência (SRAG): {e}")
    st.stop()


# 2. Gráfico de Linhas (Incidência Temporal)
# ----------------------------------------
st.subheader("Contagem Semanal de Casos SRAG")

fig_inc = px.line(
    df_timeline,
    x='Data_Semanal',
    y='Casos',
    markers=True,
    title='Contagem Semanal de Casos SRAG (2023-2024)',
    labels={'Data_Semanal': 'Data do Início da Semana', 'Casos': 'Novos Casos (SRAG)'}
)

fig_inc.update_traces(line=dict(color='#006400', width=3))
fig_inc.update_layout(xaxis_title="Data", yaxis_title="Número de Casos")

st.plotly_chart(fig_inc, use_container_width=True)


# 3. Tabela de Dados Brutos
# -------------------------
st.markdown("---")
st.subheader("Tabela de Dados Brutos SIVEP-Gripe")
st.caption("Contém informações detalhadas dos casos que compõem o gráfico acima.")

# Selecionar e Renomear colunas
df_tabela_srag = df_srag[[
    'DT_SIN_PRI', 'NU_IDADE_N', 'CS_SEXO', 'CS_GESTANT', 'FATOR_RISC'
]].copy()

df_tabela_srag.columns = [
    'Data Sintomas', 'Idade', 'Sexo', 'Gestante', 'Fatores de Risco (Sim/Não)'
]

# Mapeamento e Limpeza (Melhor visualização na tabela)
df_tabela_srag['Gestante'] = df_tabela_srag['Gestante'].map({1.0: 'Sim', 2.0: 'Não', 5.0: 'Não', 6.0: 'Ignorado'}).fillna('N/A')
df_tabela_srag['Fatores de Risco (Sim/Não)'] = df_tabela_srag['Fatores de Risco (Sim/Não)'].apply(
    lambda x: 'Sim' if x == 1.0 else 'Não'
)

st.dataframe(df_tabela_srag, use_container_width=True)