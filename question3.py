import pandas as pd
import plotly.express as px
import streamlit as st

# Carrega o dataset de vazao
df = pd.read_csv("data/clean_data/vazao.csv")
df_2 = df.copy()
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Separa a informação de qualidade
df[['quality_status', 'quality_value']] = df['quality'].str.split(': ', expand=True)

# Mapeia 'good' e 'bad' para valores booleanos
df['is_good'] = df['quality_status'] == 'good'
df['is_bad'] = df['quality_status'] == 'bad'

# Preenche valores NaN de 'vazao' com 0 para leituras ruins
df['vazao'].fillna(0, inplace=True)

# Adiciona coluna de dia da semana
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['day_of_week_name'] = df['timestamp'].dt.day_name()

# Mapeia os nomes dos dias da semana para português
dias_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

df['day_of_week_name_pt'] = df['day_of_week_name'].map(dias_semana)

# Cria DataFrame separado para leituras ruins
bad_data = df[df['is_bad']]

# Classifica ambos os DataFrames pelos timestamps
df.sort_values(by='timestamp', inplace=True)
bad_data.sort_values(by='timestamp', inplace=True)

# Adiciona um título para o Streamlit
st.title('Variação na Qualidade das Leituras ao Longo da Semana')

# Cria o gráfico com Plotly Express
fig = px.scatter(df, x='timestamp', y='vazao', color='is_good', facet_col='day_of_week_name_pt', facet_col_wrap=3,
                 labels={'vazao': 'Vazão', 'is_good': 'Leitura Boa', 'timestamp': 'Timestamp'},
                 title='Variação na Qualidade das Leituras ao Longo da Semana')

# Adiciona trace para leituras ruins
if not bad_data.empty:
    fig.add_trace(px.scatter(bad_data, x='timestamp', y='vazao', color='is_bad', facet_col='day_of_week_name_pt').data[0])

# Atualiza o layout
fig.update_layout(showlegend=False)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig)
