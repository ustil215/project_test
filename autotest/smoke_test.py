from playwright.sync_api import Page, expect

def test_chulakov_website_loads(page: Page):
    # Переходим на сайт
    page.goto("https://chulakov.team/")
    page.wait_for_load_state("networkidle")
    
    # Проверяем статус ответа
    response = page.wait_for_response(
        lambda response: response.url == "https://chulakov.team/" and response.status == 200
    )
    assert response.status == 200
    
    # Проверяем контент
    h1_element = page.locator("h1")
    expect(h1_element).to_contain_text("Быть в топе рейтингов")
    
    awards_block = page.locator("text=153 наград")
    expect(awards_block).to_be_visible()

# Добавляем этот блок для запуска через python3
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Откроет браузер
        page = browser.new_page()
        test_chulakov_website_loads(page)
        print("✅ Тест успешно выполнен!")
        browser.close()