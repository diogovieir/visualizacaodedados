import pandas as pd
import plotly.express as px
import streamlit as st

# Carrega o dataset de vazão
df_vazao = pd.read_csv("data/clean_data/vazao.csv")
df_vazao['timestamp'] = pd.to_datetime(df_vazao['timestamp'])

# Gráfico 1: Variação da Vazão ao Longo da Semana
st.title("Variação da Vazão ao Longo da Semana")
fig_vazao = px.density_heatmap(
    df_vazao,
    x="timestamp",
    y="day_of_week_name",
    z="vazao",
    color_continuous_scale="Viridis",
    title="Variação da Vazão ao Longo da Semana"
)
fig_vazao.update_xaxes(title="Mês e Ano")
fig_vazao.update_yaxes(title="Dia da Semana")
fig_vazao.update_coloraxes(colorbar_title="Vazão (m³/s)")
st.plotly_chart(fig_vazao)

# Dados climatológicos
df_clima = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Temperatura Média (°C)": [26.7, 27, 25.9, 24.3, 21.8, 20.8, 20.1, 20.9, 22.2, 23.7, 24.2, 25.8],
    "Temperatura Mínima (°C)": [23.3, 23.3, 22.7, 21.1, 18.2, 16.8, 16, 16.5, 18.1, 20, 21, 22.4],
    "Temperatura Máxima (°C)": [31.2, 31.7, 30.2, 28.5, 26.2, 25.8, 25.4, 26.5, 27.5, 28.6, 28.5, 30.1],
    "Chuva (mm)": [172, 117, 153, 99, 81, 52, 55, 45, 81, 98, 143, 156],
    "Umidade(%)": [79, 78, 81, 81, 81, 80, 79, 76, 75, 76, 80, 80],
    "Dias Chuvosos (d)": [12, 10, 12, 10, 9, 6, 6, 6, 8, 9, 12, 12],
    "Horas de Sol (h)": [9.8, 10.0, 8.8, 7.9, 7.2, 7.0, 6.9, 7.3, 7.2, 7.4, 7.7, 8.8]
}

mapa_meses = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

# Cria um DataFrame com os dados climatológicos
df_temperatura = pd.DataFrame(df_clima)

# Mock DataFrame df1, substitua pela leitura do seu arquivo
df1 = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=12, freq='M'),
    'vazao': [10, 12, 15, 8, 10, 14, 16, 18, 20, 22, 24, 26]
})

df_vazao = df1

df_vazao['timestamp'] = pd.to_datetime(df_vazao['timestamp'])

# Extraindo o mês da coluna 'timestamp' e criando uma nova coluna 'Mês'
df_vazao['Mês'] = df_vazao['timestamp'].dt.strftime('%B').map(mapa_meses)

# Mesclando os dois conjuntos de dados com base na coluna 'Mês'
merged_df = pd.merge(df_vazao, df_temperatura, left_on='Mês', right_on='Mês', how='inner')

# Gráfico 2: Relação entre Temperatura e Vazão
st.title('Relação entre Temperatura e Vazão')
fig_temperatura = px.scatter(merged_df, x='Temperatura Média (°C)', y='vazao', labels={'vazao': 'Vazão', 'Temperatura Média (°C)': 'Temperatura Média (°C)'})
st.plotly_chart(fig_temperatura)

# Gráfico 3: Variação na Qualidade das Leituras ao Longo da Semana
# (Seção de leitura de dados)
df_2 = df_vazao.copy()
df_2['quality_status'] = ['good' if v > 15 else 'bad' for v in df_2['vazao']]
df_2['quality_value'] = [1 if status == 'good' else 0 for status in df_2['quality_status']]
df_2['is_good'] = df_2['quality_status'] == 'good'
df_2['is_bad'] = df_2['quality_status'] == 'bad'
df_2['day_of_week'] = df_2['timestamp'].dt.dayofweek
df_2['day_of_week_name'] = df_2['timestamp'].dt.day_name()
dias_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
df_2['day_of_week_name_pt'] = df_2['day_of_week_name'].map(dias_semana)

# (Seção de plotagem)
st.title('Variação na Qualidade das Leituras ao Longo da Semana')
fig_qualidade = px.scatter(df_2, x='timestamp', y='vazao', color='is_good', facet_col='day_of_week_name_pt', facet_col_wrap=3,
                 labels={'vazao': 'Vazão', 'is_good': 'Leitura Boa', 'timestamp': 'Timestamp'},
                 title='Variação na Qualidade das Leituras ao Longo da Semana')
fig_qualidade.add_trace(px.scatter(df_2[df_2['is_bad']], x='timestamp', y='vazao', color='is_bad', facet_col='day_of_week_name_pt').data[0])
fig_qualidade.update_layout(showlegend=False)
st.plotly_chart(fig_qualidade)
