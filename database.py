import sqlite3

conexao = sqlite3.connect("cardapio.db")
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cardapio (
        idPrato INTEGER PRIMARY KEY,
        nome_prato TEXT,
        descricao_prato TEXT,
        categoria_prato TEXT,
        preco_prato REAL,
        disponibilidade_prato BOOLEAN,
        serve_prato TEXT,
        caminhoImagem TEXT
    )
''') 

conexao.commit()
conexao.close()