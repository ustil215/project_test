import pytest
from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)  # headless=True для фонового режима
        page = browser.new_page()
        
        # 1. Открыть Google
        page.goto('https://www.google.com/')
        
        # 2. Принять куки (если есть баннер)
        accept_button = page.locator('button:has-text("Accept all"), button:has-text("Принять все")')
        if accept_button.is_visible():
            accept_button.click()
        
        # 3. Ввести в поиск "тесты для playwright"
        search_input = page.locator('textarea[name="q"], input[name="q"]')
        search_input.fill('тесты для playwright')
        search_input.press('Enter')
        
        # 4. Дождаться результатов и кликнуть по первой ссылке
        first_result = page.locator('#search a').nth(0)
        first_result.wait_for(state='visible')
        first_result_url = first_result.get_attribute('href')
        first_result.click()
        
        # 5. Проверка, что переход выполнен
        page.wait_for_load_state('networkidle')
        assert page.url != 'https://www.google.com/'
        
        print(f'Перешли по ссылке: {first_result_url}')
        
        # Закрыть браузер
        browser.close()