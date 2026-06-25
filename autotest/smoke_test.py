from playwright.sync_api import sync_playwright
import time

def test_site_opens():
    with sync_playwright() as p:
        # Запускаем браузер с открытым окном (headless=False)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("🚀 Открываю браузер и перехожу на сайт...")
        
        # Переходим на сайт
        response = page.goto("https://chulakov.team/")
        
        # Проверяем статус ответа
        assert response.status == 200, f"Ожидался статус 200, получен {response.status}"
        
        print(f"✅ Сайт успешно открылся! Статус: {response.status}")
        
        # Держим браузер открытым 5 секунд, чтобы вы могли увидеть сайт
        print("⏳ Браузер закроется через 5 секунд...")
        time.sleep(5)
        
        browser.close()
        print("✅ Браузер закрыт. Тест завершён!")

if __name__ == "__main__":
    test_site_opens()