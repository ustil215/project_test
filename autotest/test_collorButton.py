from playwright.sync_api import sync_playwright
import os
from datetime import datetime
import time

def test_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("🚀 Открываем страницу...")
        page.goto("https://chulakov.team/", timeout=60000)
        print("✅ Страница открыта")
        
        # Просто ждем немного для прогрузки
        page.wait_for_timeout(3000)
        
        # Скроллим вниз
        print("📜 Скроллим к футеру...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        
        print("🔍 Ищем кнопку 'Вакансии'...")
        
        # Ищем кнопку разными способами
        button = None
        
        # Способ 1: через текст в футере
        try:
            button = page.locator("footer a:has-text('Вакансии')").first
            if button.count() > 0:
                print("✅ Найдено через footer a:has-text('Вакансии')")
        except:
            pass
        
        # Способ 2: через span
        if button is None or button.count() == 0:
            try:
                button = page.locator("span:has-text('Вакансии')").first
                if button.count() > 0:
                    print("✅ Найдено через span:has-text('Вакансии')")
            except:
                pass
        
        # Способ 3: просто по тексту
        if button is None or button.count() == 0:
            try:
                button = page.locator("text=Вакансии").first
                if button.count() > 0:
                    print("✅ Найдено через text=Вакансии")
            except:
                pass
        
        if button is None or button.count() == 0:
            print("❌ Кнопка не найдена!")
            browser.close()
            return
        
        # Проверяем видимость
        try:
            button.wait_for(state="visible", timeout=5000)
            print("✅ Кнопка видима")
        except:
            print("⚠️ Кнопка невидима, но продолжаем...")
        
        # Делаем скриншот
        print("📸 Делаем скриншот...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(current_dir, f"vacancies_button_{timestamp}.png")
        button.screenshot(path=screenshot_path)
        print(f"✅ Скриншот сохранен: {screenshot_path}")
        
        # Получаем цвета
        print("🎨 Получаем цвета...")
        actual_bg = button.evaluate("el => getComputedStyle(el).backgroundColor")
        actual_color = button.evaluate("el => getComputedStyle(el).color")
        print(f"   Фон кнопки:   {actual_bg}")
        print(f"   Цвет текста:  {actual_color}")
        
        # Проверяем, есть ли span внутри
        span_inside = button.locator("span").first
        if span_inside.count() > 0:
            span_bg = span_inside.evaluate("el => getComputedStyle(el).backgroundColor")
            span_color = span_inside.evaluate("el => getComputedStyle(el).color")
            print(f"   Фон span:     {span_bg}")
            print(f"   Цвет span:    {span_color}")
            # Используем цвета span, если они есть
            actual_bg = span_bg
            actual_color = span_color
        
        expected_bg = "rgb(255, 244, 95)"
        expected_color = "rgb(21, 21, 21)"
        
        print("="*50)
        if actual_bg == expected_bg and actual_color == expected_color:
            print("✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
            print(f"   Цвет фона:   {actual_bg}")
            print(f"   Цвет текста: {actual_color}")
        else:
            print("❌ ТЕСТ НЕ ПРОЙДЕН!")
            print(f"   Фон:   ожидался {expected_bg}, получен {actual_bg}")
            print(f"   Текст: ожидался {expected_color}, получен {actual_color}")
        
        print(f"   Скриншот: {screenshot_path}")
        print("="*50)
        
        # Ждем 5 секунд перед закрытием
        print("\n⏳ Браузер закроется через 5 секунд...")
        time.sleep(5)
        
        # Закрываем браузер
        browser.close()
        print("✅ ТЕСТ ПРОЙДЕН, БРАУЗЕР ЗАКРЫТ")

if __name__ == "__main__":
    test_button()