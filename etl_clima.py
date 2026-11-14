import os
import time
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Lista de capitais brasileiras
CIDADES = ["Sao Paulo,BR", "Rio de Janeiro,BR", "Brasilia,BR", "Salvador,BR", "Curitiba,BR"]

def extrair_previsao():
    print("Iniciando extração de previsão do tempo (5 dias)...")
    
    # URL da API de Previsão (Forecast)
    url = "https://api.openweathermap.org/data/2.5/forecast"
    
    dados_para_salvar = []

    for cidade in CIDADES:
        print(f"Buscando dados para: {cidade}...")
        
        parametros = {
            "q": cidade,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }

        try:
            # Tratamento de erro: timeout de 10 segundos para não travar
            resposta = requests.get(url, params=parametros, timeout=10)
            
            # Se a API retornar erro (chave inválida, cidade não encontrada, etc)
            if resposta.status_code != 200:
                print(f"Erro na API para {cidade}: {resposta.json().get('message', 'Erro')}")
                continue # Pula para a próxima cidade e não quebra o código

            dados = resposta.json()

            # A previsão retorna uma lista com 40 horários (3 em 3 horas)
            for item in dados['list']:
                linha = {
                    'cidade': dados['city']['name'],
                    'data_previsao': item['dt_txt'], # Data e hora da previsão
                    'temperatura_c': item['main']['temp'],
                    'sensacao_termica_c': item['main']['feels_like'],
                    'umidade_pct': item['main']['humidity'],
                    'descricao_clima': item['weather'][0]['description'],
                    'data_coleta': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                dados_para_salvar.append(linha)
                
            # Pausa de 1 segundo entre cidades para não sobrecarregar a API
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            # Se a internet cair, ele avisa e continua
            print(f"Erro de conexão com a internet para {cidade}: {e}")

    # Transformando a lista em DataFrame
    if dados_para_salvar:
        df = pd.DataFrame(dados_para_salvar)
        print(f"Total de registros extraídos: {len(df)}")
        return df
    else:
        print("Nenhum dado foi extraído.")
        return None

def carregar_no_banco(df):
    if df is not None and not df.empty:
        print("Salvando dados no banco SQLite...")
        # O arquivo clima_banco.db será criado na mesma pasta
        engine = create_engine('sqlite:///clima_banco.db')
        
        # Adiciona os novos dados (se a tabela existir, ele apenas insere mais linhas)
        df.to_sql('previsao_clima', engine, if_exists='append', index=False)
        print("Dados salvos com sucesso no banco!")
    else:
        print("Não há dados para salvar.")

# Fluxo principal do ETL
if __name__ == "__main__":
    df_previsao = extrair_previsao()
    carregar_no_banco(df_previsao)