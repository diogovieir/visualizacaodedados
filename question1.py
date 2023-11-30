import pandas as pd
import plotly.express as px
import streamlit as st

# Gráfico para a questão 1
df = pd.read_csv("data/clean_data/vazao.csv")
# Cria uma cópia do DataFrame
df_1 = df.copy()
# Converte a coluna 'timestamp' para o tipo datetime
df_1['timestamp'] = pd.to_datetime(df_1['timestamp'])
# Extrai o dia da semana da coluna 'timestamp' e cria uma nova coluna 'day_of_week'
df_1['day_of_week_name'] = df_1['timestamp'].dt.day_name()
# Cria o gráfico de calendar heatmap
fig = px.density_heatmap(
    df_1,
    x="day_of_week_name",
    y="timestamp",
    z="vazao",
    color_continuous_scale="Viridis",
    title="Variação da Vazão ao Longo da Semana"
)
# Personaliza o layout
fig.update_xaxes(title="Dia da Semana")
fig.update_yaxes(title="Mês e Ano")
fig.update_coloraxes(colorbar_title="Vazão (m³/s)")
# Mostra o gráfico no Streamlit
st.plotly_chart(fig)
