import sqlite3

def init_db():
    conn = sqlite3.connect('faltas.db')
    cursor = conn.cursor()
    
    # Tabela de Alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL
        )
    ''')
    
    # Tabela de Faltas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faltas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            materia TEXT NOT NULL,
            data DATE NOT NULL,
            justificativa TEXT,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao importar
init_db()