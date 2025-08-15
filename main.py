import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
from database import init_db

# Configuração da página
st.set_page_config(
    page_title="Sistema de Faltas Escolares",
    page_icon="📊",
    layout="wide"
)

# ---- FUNÇÕES ---- #
def cadastrar_aluno(nome, turma):
    conn = sqlite3.connect('faltas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alunos (nome, turma) VALUES (?, ?)', (nome, turma))
    conn.commit()
    conn.close()

def registrar_falta(aluno_id, materia, data):
    conn = sqlite3.connect('faltas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO faltas (aluno_id, materia, data) VALUES (?, ?, ?)
    ''', (aluno_id, materia, data))
    conn.commit()
    conn.close()

def gerar_relatorio_pdf():
    conn = sqlite3.connect('faltas.db')
    df = pd.read_sql('''
        SELECT alunos.nome, alunos.turma, faltas.materia, faltas.data, faltas.justificativa 
        FROM faltas
        JOIN alunos ON faltas.aluno_id = alunos.id
    ''', conn)
    conn.close()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Faltas Escolares", ln=True, align='C')
    
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"Aluno: {row['nome']} | Turma: {row['turma']} | Matéria: {row['materia']} | Data: {row['data']}", ln=True)
    
    pdf.output("relatorio_faltas.pdf")
    return df

# ---- INTERFACE ---- #
st.title("📊 Sistema de Faltas Escolares")

# Abas para organização
tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar Aluno", "Registrar Falta", "Relatórios", "Dashboard"])

with tab1:
    st.header("Cadastrar Novo Aluno")
    nome = st.text_input("Nome do Aluno")
    turma = st.text_input("Turma")
    if st.button("Cadastrar"):
        cadastrar_aluno(nome, turma)
        st.success("Aluno cadastrado com sucesso!")

with tab2:
    st.header("Registrar Falta")
    conn = sqlite3.connect('faltas.db')
    alunos = pd.read_sql('SELECT id, nome, turma FROM alunos', conn)
    conn.close()
    
    aluno_selecionado = st.selectbox("Selecione o Aluno", alunos['nome'])
    materia = st.text_input("Matéria")
    data = st.date_input("Data da Falta")
    
    if st.button("Registrar Falta"):
        aluno_id = alunos.loc[alunos['nome'] == aluno_selecionado, 'id'].values[0]
        registrar_falta(aluno_id, materia, data)
        st.success("Falta registrada com sucesso!")

with tab3:
    st.header("Gerar Relatório")
    if st.button("Gerar PDF"):
        df = gerar_relatorio_pdf()
        st.dataframe(df)
        
        with open("relatorio_faltas.pdf", "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name="relatorio_faltas.pdf",
            mime="application/pdf"
        )

with tab4:
    st.header("Dashboard de Faltas")
    conn = sqlite3.connect('faltas.db')
    faltas = pd.read_sql('''
        SELECT alunos.nome, alunos.turma, faltas.materia, faltas.data
        FROM faltas
        JOIN alunos ON faltas.aluno_id = alunos.id
    ''', conn)
    conn.close()
    
    st.bar_chart(faltas['materia'].value_counts())