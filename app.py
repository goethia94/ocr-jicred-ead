import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import tempfile
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="OCR JiCred EAD", layout="wide")
st.title("📄 Processador de Relatórios EAD - JiCred")

st.markdown("""Este aplicativo realiza a leitura de PDFs ou imagens (.jpg/.png) com os relatórios de aproveitamento EAD da JiCred,
extraindo os nomes, notas e status de conclusão com base na seguinte regra:

- Nota **≥ 7.00** → **Concluído**
- Nota **< 7.00** → **Não Concluído**
""")

uploaded_files = st.file_uploader("Envie o PDF ou imagens do relatório", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

def process_image(img):
    text = pytesseract.image_to_string(img, lang="eng")
    linhas = text.split('\n')
    dados = []
    for linha in linhas:
        if "Colaboradores JiCred" in linha:
            partes = linha.split("Colaboradores JiCred")
            nome = partes[0].strip()
            nota = None
            tokens = partes[1].split()
            for token in tokens:
                try:
                    nota_float = float(token.replace(',', '.'))
                    nota = nota_float
                    break
                except:
                    continue
            conclusao = ""
            for token in tokens:
                if "/" in token and len(token) >= 8:
                    conclusao = token
            if nota is not None:
                status = "Concluído" if nota >= 7.0 else "Não Concluído"
                dados.append((nome, round(nota, 2), status, conclusao))
    return dados

if uploaded_files:
    dados_por_nota = []
    with st.spinner("Processando arquivos..."):
        for file in uploaded_files:
            if file.name.lower().endswith(".pdf"):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                for page in doc:
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    dados_por_nota.extend(process_image(img))
            else:
                img = Image.open(file)
                dados_por_nota.extend(process_image(img))

    df_resultado = pd.DataFrame(dados_por_nota, columns=["Nome", "Nota", "Status", "Data Conclusão"])
    st.success(f"Processamento concluído! {len(df_resultado)} registros encontrados.")
    st.dataframe(df_resultado, use_container_width=True)

    st.download_button(
        label="📄 Baixar planilha Excel",
        data=df_resultado.to_excel(index=False),
        file_name="Relatorio_EAD_JiCred.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
