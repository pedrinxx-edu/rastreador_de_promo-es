import sqlite3

conexao = sqlite3.connect("promocoes.db")
cursor = conexao.cursor()
cursor.execute("SELECT * FROM promocoes")
linhas = cursor.fetchall()

print(linhas)