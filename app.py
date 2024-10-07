import streamlit as st
import pandas as pd
import pickle

# Função principal
def main():
    # Título do aplicativo
    st.title("Cálculo Métricas Teste")

    # Leitura do arquivo CSV
    try:
        df = pd.read_csv('tabela_metrica_produtos_ruas_bronze.csv')
    except FileNotFoundError:
        st.error("Erro: O arquivo 'tabela_metricas_produtos.csv' não foi encontrado.")
        return
    
    try:
        with open('parametrosPracas.pkl', 'rb') as file:
            params = pickle.load(file)
    except FileNotFoundError:
        st.error("Erro: O arquivo 'parametrosPracas.pkl' não foi encontrado.")
        return

    # Verificação se a coluna 'chave_produto' existe no DataFrame
    if 'chave_produto' not in df.columns:
        st.error("Erro: A coluna 'chave_produto' não foi encontrada no arquivo.")
        return

    # Caixa de seleção múltipla com todas as opções de 'chave_produto', filtrável conforme o usuário digita
    chaves_selecionadas = st.multiselect("Buscar chaves de produto:", df['chave_produto'].unique())

    # Campo de entrada de texto para o período
    periodo = st.text_input("Digite o período:")

    # Caixa de seleção para a cota
    cota = st.selectbox("Selecione a cota:", ['0.5', '1.0', '2.0'])

    # Exibir as chaves selecionadas
    texto_chaves = ', '.join(chaves_selecionadas)
    st.write(f"Chaves selecionadas: {texto_chaves}")

    # Exibir o período
    st.write(f"Período inserido: {periodo}")

    # Exibir a cota selecionada
    st.write(f"Cota selecionada: {cota}")

    lista_chaves = chaves_selecionadas

    lista_pracas = df[df['chave_produto'].isin(lista_chaves)]['praca'].unique()

    texto_pracas = ', '.join(lista_pracas)
    st.write(f"Praças presentes: {texto_pracas}")

# Executa o aplicativo
if __name__ == '__main__':
    main()
