import streamlit as st
import pandas as pd

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

    # Verificação se a coluna 'chave_produto' existe no DataFrame
    if 'chave_produto' not in df.columns:
        st.error("Erro: A coluna 'chave_produto' não foi encontrada no arquivo.")
        return

    # Campo para inserção de texto (busca)
    st.write("Digite a chave do produto:")
    
    # Caixa de texto para pesquisa
    chave_input = st.text_input("Buscar chave do produto:")

    # Filtrar as opções conforme o texto é digitado
    if chave_input:
        # Mostrar somente as chaves que contêm o texto inserido
        opcoes_filtradas = df[df['chave_produto'].str.contains(chave_input, case=False, na=False)]
        
        if not opcoes_filtradas.empty:
            # Exibir as chaves filtradas
            st.write("Opções encontradas:")
            st.dataframe(opcoes_filtradas[['chave_produto']])
        else:
            st.write("Nenhuma chave encontrada.")
    else:
        st.write("Insira uma chave_produto para calcular a métrica.")

# Executa o aplicativo
if __name__ == '__main__':
    main()
