import sqlite3

conexao = sqlite3.connect("promocoes.db")
cursor = conexao.cursor()
cursor.execute("SELECT asin, titulo, preco_antigo, preco_atual, round((preco_antigo - preco_atual) / preco_antigo * 100, 1) AS desconto FROM promocoes WHERE enviado = 0 ORDER BY desconto DESC LIMIT 10")
linhas = cursor.fetchall()

for linha in linhas:
    print(linha)