import pandas as pd
from datetime import datetime, timedelta
import google.auth.transport.requests
import google.oauth2.id_token
import google.oauth2.service_account
from tqdm import tqdm
import json
import time
import numpy as np
import requests
import certifi
import urllib3
import streamlit as st
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

url_api_ooh = url_api_ooh
url_api_OnD = url_api_OnD

# Obtenção do ID token
id_token_ooh = get_id_token(service_account_info, url_api_ooh)

# Cabeçalho de autenticação
headers_ooh = {
    'Authorization': f'Bearer {id_token_ooh}',
    'Content-Type': 'application/json'
}

# Dados a serem enviados na requisição POST
json_data_ooh = {
    "map_id": "Mub_Carnaval!",
    # "map_id": '018f9650-989a-7a89-acfe-6e3c849d6a82',
    "start_date": "2024-05-07",
    "end_date": "2024-05-27",
    "map_name": 1,
    "force": 0,
    "csv": 0}

response = requests.post(url_api_ooh, headers=headers_ooh, json=json_data_ooh, verify=False)

st.write(response)