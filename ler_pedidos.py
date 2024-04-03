import streamlit as st
import fitz  # PyMuPDF
import re

def extract_product_names_from_pdf(uploaded_file):
    """
    Extrai os nomes dos produtos de um arquivo PDF carregado, removendo números e itens não desejados.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    # Melhorando a regex para identificar melhor os produtos
    product_lines = re.findall(r'\d+\s+-\s+([^\d\n]+)', text)
    # Remove números do início dos nomes e itens claramente não relacionados a produtos
    processed_products = [re.sub(r'^\d+\s+-\s+', '', line).strip() for line in product_lines if "EM FRENTE MAÇONARIA" not in line]
    return processed_products

def main():
    st.title('Extrator de Borderô')
    uploaded_files = st.file_uploader("Faça o upload dos arquivos PDF aqui", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        all_products = []
        for uploaded_file in uploaded_files:
            with st.spinner(f'Processando {uploaded_file.name}...'):
                products = extract_product_names_from_pdf(uploaded_file)
                all_products.extend(products)
        # Removendo duplicatas e ordenando a lista
        unique_products = sorted(set(all_products))
        
        st.success('Processamento concluído!')
        
        # Usando uma caixa de texto para facilitar a cópia dos produtos
        products_text = "\n".join(unique_products)
        st.text_area("Produtos/Serviços extraídos:", products_text, height=300)

if __name__ == "__main__":
    main()
