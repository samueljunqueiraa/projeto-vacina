# Exemplo de /pages/3_Cobertura_Vacinal.py
import streamlit as st
import pandas as pd
from pathlib import Path

# ... (configuração da página)

# 1. Carregamento e Exibição do Valor
try:
    base_path = Path(__file__).parent.parent 
    vacinal_path = base_path / "dados" / "machado_cobertura_vacinal.csv"
    df_vacinal = pd.read_csv(vacinal_path)
    
    C_VACINAL_MEDIA = df_vacinal['C_Vacinal'].iloc[0]
    
    st.header("💉 Cobertura Vacinal Consolidada")
    st.markdown("A Cobertura Vacinal ($C_{Vacinal}$) representa a média consolidada de 2023 e 2024 para Machado, utilizada como fator de mitigação na heurística de priorização.")
    
    st.metric(
        label="Média Consolidada de Cobertura Vacinal (2023-2024)",
        value=f"{C_VACINAL_MEDIA:.2f}%",
        delta=None # Ou a diferença entre 2024 e 2023, se desejar
    )
    
    st.subheader("Detalhes da Consolidação")
    st.dataframe(df_vacinal)
    
except FileNotFoundError:
    st.error(f"ERRO: Arquivo de Cobertura Vacinal não encontrado em: {vacinal_path}")
    st.stop()
except Exception as e:
    st.error(f"Erro ao processar dados de Cobertura Vacinal: {e}")
    st.stop()