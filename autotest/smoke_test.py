import re
from playwright.sync_api import Page, expect

def test_chulakov_website_loads(page: Page):
    """
    Тест проверяет загрузку сайта Chulakov Team.
    """
    # 1. Переходим на главную страницу
    page.goto("https://chulakov.team/")

    # 2. Ожидаем, пока сеть станет "почти" idle (все основные ресурсы загружены)
    page.wait_for_load_state("networkidle")

    # 3. Проверяем статус ответа (код 200 OK)
    #    Получаем ответ для главной страницы
    response = page.wait_for_response(
        lambda response: response.url == "https://chulakov.team/" and response.status == 200
    )
    assert response.status == 200, f"Ожидался статус 200, получен {response.status}"

    # 4. Проверяем, что в заголовке h1 есть ожидаемый текст
    h1_element = page.locator("h1")
    expect(h1_element).to_contain_text("Быть в топе рейтингов")

    # 5. Дополнительно проверяем, что виден блок с количеством наград
    awards_block = page.locator("text=153 наград")
    expect(awards_block).to_be_visible()