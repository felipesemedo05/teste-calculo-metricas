import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import google.auth.transport.requests
import google.oauth2.id_token
import google.oauth2.service_account
import urllib3

# Desabilitar avisos de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Função para obter o token de autenticação do Google
def get_id_token(service_account_info, url):
    credentials = google.oauth2.service_account.Credentials.from_service_account_info(
        service_account_info
    )
    auth_request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_request, url)
    return id_token

# Configuração do Streamlit
st.title("Aplicativo de Integração com API")

# Entrada de dados para as credenciais do serviço
st.sidebar.header("Configurações de Credenciais")

# # Coletando dados de entrada do usuário no Streamlit
# project_id = st.sidebar.text_input("ID do Projeto")
# private_key_id = st.sidebar.text_input("ID da Chave Privada")
# private_key = st.sidebar.text_area("Chave Privada")
# client_email = st.sidebar.text_input("Email do Cliente")
# client_id = st.sidebar.text_input("ID do Cliente")
# auth_uri = st.sidebar.text_input("URI de Autenticação")
# token_uri = st.sidebar.text_input("URI do Token")
# auth_provider_x509_cert_url = st.sidebar.text_input("URL do Certificado do Provedor de Autenticação")
# client_x509_cert_url = st.sidebar.text_input("URL do Certificado do Cliente")
# universe_domain = st.sidebar.text_input("Domínio do Universo")
# url_api_ooh = st.sidebar.text_input("URL da API OOH")
# url_api_OnD = st.sidebar.text_input("URL da API OnD")

# Definindo as informações da conta de serviço
service_account_info = {
    "type": type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}

# Inputs para a requisição da API
st.sidebar.header("Configurações da Requisição")
map_id = st.sidebar.text_input("ID do Mapa", "Mub_Carnaval!")
start_date = st.sidebar.date_input("Data de Início", datetime(2024, 5, 7))
end_date = st.sidebar.date_input("Data de Fim", datetime(2024, 5, 27))
map_name = st.sidebar.number_input("Nome do Mapa", min_value=0, value=1)
force = st.sidebar.number_input("Força", min_value=0, value=0)
csv = st.sidebar.number_input("CSV", min_value=0, value=0)

# Função para fazer a requisição
def send_request():
    # Obtenção do ID token
    id_token_ooh = get_id_token(service_account_info, url_api_ooh)

    # Cabeçalho de autenticação
    headers_ooh = {
        'Authorization': f'Bearer {id_token_ooh}',
        'Content-Type': 'application/json'
    }

    # Dados a serem enviados na requisição POST
    json_data_ooh = {
        "map_id": map_id,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "map_name": map_name,
        "force": force,
        "csv": csv
    }

    # Enviando a requisição
    response = requests.post(url_api_ooh, headers=headers_ooh, json=json_data_ooh, verify=False)
    return response

# Botão para enviar a requisição
if st.button("Enviar Requisição"):
    response = send_request()
    if response.status_code == 200:
        st.success("Requisição enviada com sucesso!")
        st.json(response.json())
    else:
        st.error(f"Erro {response.status_code}: {response.text}")
