from playwright.sync_api import sync_playwright
import time
import sqlite3

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    aba = browser.new_page()
    aba.goto("https://www.amazon.com.br")
    barra_de_pesquisa = aba.locator("#twotabsearchtextbox")
    barra_de_pesquisa.fill("Notebook")
    barra_de_pesquisa.press("Enter")
    time.sleep(5)
    lista_de_caixas = aba.locator('[data-component-type="s-search-result"]').all()
    conexao = sqlite3.connect("promocoes.db")
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS promocoes (titulo TEXT, preco_antigo REAL, preco_atual REAL, asin TEXT UNIQUE, enviado INTEGER DEFAULT 0)")
    conexao.commit()

    for caixa in lista_de_caixas:
        titulo = caixa.locator("h2.a-size-base-plus").first.inner_text()
        asin = caixa.get_attribute("data-asin")
        try:    
            preco_antigo = caixa.locator('[data-a-strike="true"]').first.inner_text(timeout = 1000).split('\n')[0]
            preco_antigo = preco_antigo.replace("R$", "").replace("\xa0", "").replace(".", "").replace(",", ".")
            preco_antigo = float(preco_antigo)
            preco_atual = caixa.locator("span.a-price").first.inner_text(timeout = 1000).split("\n")[0]
            preco_atual = preco_atual.replace("R$", "").replace("\xa0", "").replace(".", "").replace(",", ".")            
            preco_atual = float(preco_atual)
            print(f"Promoção! {titulo} | De: {preco_antigo} | Por: {preco_atual}")
            cursor.execute("INSERT OR IGNORE INTO promocoes (titulo, preco_antigo, preco_atual, asin) VALUES (?, ?, ?, ?)", (titulo, preco_antigo, preco_atual, asin))
            conexao.commit()
        except Exception:
            pass