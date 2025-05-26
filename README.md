# JiCred EAD OCR WebApp (versão PyMuPDF)

Este projeto é um WebApp em Python usando Streamlit que permite processar relatórios de cursos EAD da JiCred a partir de PDFs ou imagens.

## Funcionalidades

- Leitura de imagens ou PDFs com múltiplas páginas
- OCR para extrair nome, nota e data de conclusão
- Cálculo automático do status (Concluído ou Não Concluído)
- Exportação para Excel

## Como rodar

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Rode o app:
```bash
streamlit run app.py
```

## Compatibilidade

Essa versão usa `PyMuPDF` (fitz) e funciona diretamente no **Streamlit Cloud** (sem necessidade de Poppler).
