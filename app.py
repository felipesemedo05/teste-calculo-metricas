import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from tqdm import tqdm
import google.auth.transport.requests
import google.oauth2.id_token
import google.oauth2.service_account
import urllib3

# Desabilitar avisos de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_id_token(service_account_info, audience):
    """
    Obtém um ID token usando a conta de serviço para autenticação com uma Cloud Function.

    Args:
    - service_account_info (str): Conteúdo JSON da chave da conta de serviço.
    - audience (str): O público-alvo, geralmente a URL da Cloud Function.

    Returns:
    - str: O ID token.
    """
    try:
        # Carregar credenciais da conta de serviço diretamente do conteúdo JSON
        #service_account_info = json.loads(service_account_info)
        credentials = google.oauth2.service_account.IDTokenCredentials.from_service_account_info(service_account_info, target_audience=audience)
        print("Service account credentials loaded successfully.")
        
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)
        print("ID token refreshed successfully.")
        
        return credentials.token
    except (google.auth.exceptions.GoogleAuthError, json.JSONDecodeError) as e:
        print(f"Error fetching ID token: {e}")
        return None

# Configuração do Streamlit
st.title("Aplicativo de Integração com API")

# Entrada de dados para as credenciais do serviço
st.sidebar.header("Configurações de Credenciais")

url_api_ooh = st.secrets['url_api_ooh']
url_api_OnD = st.secrets['url_api_OnD']

# Definindo as informações da conta de serviço
service_account_info = {
    "type": st.secrets['type'],
    "project_id": st.secrets['project_id'],
    "private_key_id": st.secrets['private_key_id'],
    "private_key": st.secrets['private_key'],
    "client_email": st.secrets['client_email'],
    "client_id": st.secrets['client_id'],
    "auth_uri": st.secrets['auth_uri'],
    "token_uri": st.secrets['token_uri'],
    "auth_provider_x509_cert_url": st.secrets['auth_provider_x509_cert_url'],
    "client_x509_cert_url": st.secrets['client_x509_cert_url'],
    "universe_domain": st.secrets['universe_domain']
}


# Inputs para a requisição da API
st.sidebar.header("Configurações da Requisição")
map_name = st.sidebar.text_input("Nome do Mapa")
start_date = st.sidebar.date_input("Data de Início", datetime(2024, 5, 7))
end_date = st.sidebar.date_input("Data de Fim", datetime(2024, 5, 27))
force = st.sidebar.number_input("Force", min_value=0, value=0)
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
        "map_id": map_name,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "map_name": 1,
        "force": force,
        "csv": csv
    }

    # Enviando a requisição
    response = requests.post(url_api_ooh, headers=headers_ooh, json=json_data_ooh, verify=False)
    return response

# Botão para enviar a requisição
if st.button("Enviar Requisição"):
    response = send_request()
    st.write('🟢')
    if response.status_code == 200:
        st.success("Requisição enviada com sucesso!")
        st.json(response.json())
    else:
        st.error(f"Erro {response.status_code}: {response.text}")
