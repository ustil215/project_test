import pytest
from playwright.sync_api import Page, expect
import os
from datetime import datetime

def test_footer_vacancies_button_colors(page: Page):
    # 1. Открываем страницу
    page.goto("https://chulakov.team/")
    
    # 2. Находим кнопку "Вакансии" в футере
    button = page.locator("footer a:has-text('Вакансии')")
    
    # 3. Убеждаемся, что кнопка видима
    expect(button).to_be_visible()
    
    # 4. Скроллим до кнопки
    button.scroll_into_view_if_needed()
    
    # 5. Получаем реальные цвета ДО проверок
    actual_bg = button.evaluate("el => getComputedStyle(el).backgroundColor")
    actual_color = button.evaluate("el => getComputedStyle(el).color")
    
    # 6. Делаем скриншот кнопки ВСЕГДА (до или после проверок)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(current_dir, f"vacancies_button_{timestamp}.png")
    button.screenshot(path=screenshot_path)
    
    # 7. Проверяем цвета с перехватом ошибок
    expected_bg = "rgb(255, 244, 94)"
    expected_color = "rgb(21, 21, 22)"
    
    try:
        # Проверяем фон
        assert actual_bg == expected_bg, f"Цвет фона не совпадает! Ожидаемый: {expected_bg}, Реальный: {actual_bg}"
        
        # Проверяем текст
        assert actual_color == expected_color, f"Цвет текста не совпадает! Ожидаемый: {expected_color}, Реальный: {actual_color}"
        
        # Если все проверки прошли
        print("✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print(f"   Цвет фона: {actual_bg} (совпадает)")
        print(f"   Цвет текста: {actual_color} (совпадает)")
        print(f"   Скриншот сохранен: {screenshot_path}")
        
    except AssertionError as e:
        # Если какая-то проверка не прошла
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        print(f"   Ошибка: {str(e)}")
        print(f"   Скриншот сохранен: {screenshot_path}")
        
        # Перевыбрасываем исключение, чтобы тест упал
        raise
    
    # Дополнительный вариант: использовать встроенные ожидания Playwright с try/except
    # (закомментировано, но оставлено для справки)
    """
    try:
        expect(button).to_have_css("background-color", expected_bg)
        expect(button).to_have_css("color", expected_color)
        print("✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
    except AssertionError as e:
        print("❌ ТЕСТ НЕ ПРОЙДЕН!")
        print(f"   Ошибка: {str(e)}")
        raise
    """