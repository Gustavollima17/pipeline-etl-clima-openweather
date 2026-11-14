# 🌦️ Pipeline ETL de Previsão Climática (OpenWeather)

Pipeline ETL automatizado que consome dados meteorológicos da API do OpenWeatherMap para 5 capitais brasileiras, realiza o tratamento com Python e Pandas, armazena em um banco de dados SQLite e alimenta um dashboard interativo no Power BI.

## 🏗️ Arquitetura do Projeto
1. *Extração (etl_clima.py):* Consumo da API OpenWeatherMap via biblioteca requests.
2. *Transformação:* Limpeza, padronização de tipos numéricos e tratamento de datas com pandas.
3. *Carregamento:* Persistência estruturada no banco de dados relacional SQLite.
4. *Automação (rodar_etl.bat):* Execução agendada diariamente sem intervenção manual.
5. *Visualização (dashboard_clima.pbix):* Painel analítico interativo no Power BI.

## 🛠️ Tecnologias Utilizadas
* *Python 3* (requests, pandas, sqlite3, python-dotenv)
* *SQLite*
* *Power BI*
* *Windows Batch (.bat)*

## 🚀 Como Executar o Projeto
1. Clone este repositório:
   bash
   git clone https://github.com
   
2. Instale as dependências:
   bash
   pip install -r requirements.txt
   
3. Crie um arquivo .env na raiz do projeto com a sua chave da API do OpenWeatherMap:
   env
   OPENWEATHER_API_KEY=sua_chave_aqui
   
4. Execute o pipeline:
   bash
   python etl_clima.py
   

## 📊 Dashboard
<img width="885" height="499" alt="dashboard_imagem" src="https://github.com/user-attachments/assets/e449638b-7403-4f45-80a5-ef3cc5d03a02" />

