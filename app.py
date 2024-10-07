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

    # Exibir um campo de seleção múltipla (com filtro) para as chaves do produto
    st.write("Selecione ou digite as chaves de produto:")

    # Caixa de seleção múltipla com todas as opções de 'chave_produto', filtrável conforme o usuário digita
    chaves_selecionadas = st.multiselect("Buscar chaves de produto:", df['chave_produto'].unique())

    # Exibir as chaves selecionadas
    if chaves_selecionadas:
        st.write("Chaves selecionadas:")
        st.write(chaves_selecionadas)
    else:
        st.write("Nenhuma chave selecionada.")

    # Salvar as chaves selecionadas em uma lista
    lista_chaves = chaves_selecionadas

# Executa o aplicativo
if __name__ == '__main__':
    main()
