import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Configuração inicial do Streamlit
st.title("Portal Belas Artes - Notas e Faltas")

# Entrada de usuário e senha
st.sidebar.header("Login")
usuario = st.sidebar.text_input("Usuário:")
senha = st.sidebar.text_input("Senha:", type="password")

if st.sidebar.button("Entrar"):
    # Configuração do Selenium
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Acessar o portal
        url = 'https://portal.belasartes.br/FrameHTML/Web/App/Edu/PortalEducacional/login/'
        driver.get(url)
        st.info('Acessando o site...')
        time.sleep(5)

        # Preenchendo os campos de login
        driver.find_element(By.XPATH, '//*[@id="User"]').send_keys(usuario)
        driver.find_element(By.XPATH, '//*[@id="Pass"]').send_keys(senha)
        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/form/div[4]/input').click()
        time.sleep(10)

        st.success('Login bem-sucedido!')

        # Acessar notas
        driver.find_element(By.XPATH, '//*[@id="sidebar-min"]/ul/li[6]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="EDU_PORTAL_ACADEMICO_CENTRALALUNO"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="EDU_PORTAL_ACADEMICO_CENTRALALUNO_NOTAS"]').click()
        time.sleep(6)

        st.info('Carregando as notas...')
        texto = driver.find_elements(By.CLASS_NAME, 'gridRow')
        aa = [txt.text for txt in texto if txt.text]

        # Processar notas
        data = [item.strip().split('\n') for item in aa]
        blocos = []
        bloco_atual = []

        for item in data:
            if item == ['CENTRO UNIVERSITARIO BELAS ARTES DE SAO PAULO']:
                if bloco_atual:
                    blocos.append(bloco_atual)
                bloco_atual = [item[0]]
            else:
                bloco_atual.append(item[0])

        if bloco_atual:
            blocos.append(bloco_atual)

        df = pd.DataFrame(blocos, columns=['Instituição', 'Código', 'Materia', 'Status', 'Nota', 'Frequência', 'Avaliações'])
        df = df[['Materia', 'Nota']]
        df['Nota'] = df['Nota'].apply(lambda x: x.replace('Ver avaliações', '0'))
        df['Nota'] = df['Nota'].apply(lambda x: float(x.replace(',', '.')) if x.replace(',', '.').replace('.', '').isdigit() else x)

        # Calculando "Quanto Falta"
        grade_requirements = {
            0.0: 0.0, 0.5: 9.5, 1.0: 9.0, 1.5: 9.0, 2.0: 8.5,
            2.5: 8.0, 3.0: 8.0, 3.5: 7.5, 4.0: 7.0, 4.5: 7.0,
            5.0: 6.5, 5.5: 6.0, 6.0: 6.0, 6.5: 5.5, 7.0: 5.0,
            7.5: 5.0, 8.0: 4.5, 8.5: 4.0, 9.0: 4.0, 9.5: 3.5,
            10.0: 3.0, 8.2: 4.5
        }
        df['Quanto Falta'] = [grade_requirements.get(grade, '0') for grade in df['Nota']]

        # Acessar faltas
        driver.find_element(By.XPATH, '//*[@id="sidebar-min"]/ul/li[6]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="EDU_PORTAL_ACADEMICO_CENTRALALUNO"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="EDU_PORTAL_ACADEMICO_CENTRALALUNO_FALTAS"]').click()
        time.sleep(6)

        st.info('Carregando as faltas...')
        aab = [txt.text for txt in driver.find_elements(By.CLASS_NAME, 'gridRow') if txt.text]

        # Processar faltas
        rows = []
        temp_row = []

        for item in aab:
            temp_row.append(item)
            if item == "Ver faltas":
                rows.append(temp_row)
                temp_row = []

        formatted_rows = []
        for row in rows:
            if len(row) == 4:
                formatted_rows.append([row[0], row[1], row[2], 0, 0, 0, 0, 0, 0, 0, row[3]])
            else:
                formatted_rows.append(row[:10])

        columns = ['Instituicao', 'Materia', 'Curso', 'Total_Faltas', 'Faltas_Agosto', 'Faltas_Setembro', 
                   'Faltas_Outubro', 'Faltas_Novembro', 'Total_Faltas_Possiveis', 'Ver faltas', 'Ver faltas']
        df2 = pd.DataFrame(formatted_rows, columns=columns)
        df2 = df2[['Materia', 'Total_Faltas', 'Total_Faltas_Possiveis']]

        # Merge notas e faltas
        df_final = df.merge(df2, on='Materia')

        # Exibir tabelas
        st.subheader("Notas")
        st.dataframe(df)

        st.subheader("Faltas")
        st.dataframe(df2)

        st.subheader("Resumo Final")
        st.dataframe(df_final)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()
