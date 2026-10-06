from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    aba = browser.new_page()
    aba.goto("https://www.amazon.com.br")
    barra_de_pesquisa = aba.locator("#twotabsearchtextbox")
    barra_de_pesquisa.fill("Notebook")
    barra_de_pesquisa.press("Enter")
    time.sleep(5)
    lista_de_caixas = aba.locator('[data-component-type="s-search-result"]').all()

    for caixa in lista_de_caixas:
        titulo = caixa.locator("h2.a-size-base-plus").first.inner_text()
        try:    
            preco_antigo = caixa.locator('[data-a-strike="true"]').first.inner_text(timeout = 1000).split('\n')[0]
            preco_atual = caixa.locator("span.a-price").first.inner_text(timeout = 1000).split("\n")[0]
            print(f"Promoção! {titulo} | De: {preco_antigo} | Por: {preco_atual}")
        except Exception:
            pass