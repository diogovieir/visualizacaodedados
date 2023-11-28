import pandas as pd

def clean_data(path):
    df = pd.read_csv(path, sep=';')

    #Alterando a pontuação do valor de vazão
    df['value'] = df['value'].astype(str).str.replace(',', '.').astype(float)

    # Selecionando somente a quality=good e removendo a coluna quality, pois temos todos os valores iguais
    df['quality'] = df['quality'].str.strip().str.lower()

    df = df.rename(columns={'value': 'vazao'})

    #Alterando a coluna timestamp para timestramp e extraindo o dia da semana
    df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
    df['day_of_week'] = df['timestamp'].dt.dayofweek


    # Mapeia o número do dia da semana para o nome do dia da semana em português
    dias_da_semana = {2:'Segunda-feira', 3:'Terça-feira', 4:'Quarta-feira', 5:'Quinta-feira', 6:'Sexta-feira', 0:'Sábado', 1:'Domingo'}
    df['day_of_week_name'] = df['day_of_week'].map(dias_da_semana)

    # Salva o novo df limpo
    df.to_csv('/home/guia/Documents/diogo/visualizacaoDados/trab_final/data/clean_data/vazao.csv', index=False)

if __name__ == '__main__':
    path = '/home/guia/Documents/diogo/visualizacaoDados/trab_final/data/vazao4_2.csv'
    clean_data(path)