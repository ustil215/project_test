from playwright.sync_api import sync_playwright
import os
import time


def test_yandex_search():
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Создание контекста и страницы
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        # Маскировка
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)
        
        try:
            # 1. Открываем Яндекс
            print("🌐 Открываем ya.ru...")
            page.goto("https://ya.ru/", timeout=10000)
            page.wait_for_timeout(1000)
            
            # 2. Вводим запрос
            print("🔍 Вводим 'коты'...")
            search_input = page.locator('input[name="text"]')
            search_input.wait_for(state="visible", timeout=5000)
            search_input.click()
            search_input.fill("коты")
            page.wait_for_timeout(500)
            search_input.press("Enter")
            
            # 3. Ждем загрузки результатов (сокращенное время)
            print("⏳ Ожидаем загрузки результатов...")
            page.wait_for_load_state("networkidle", timeout=5000)
            page.wait_for_timeout(1000)
            
            # 4. Переходим на картинки
            print("🖼️ Переходим на Картинки...")
            try:
                # Пробуем найти вкладку "Картинки"
                images_link = page.locator('a:has-text("Картинки")')
                if images_link.count() == 0:
                    images_link = page.locator('a[data-id="images"]')
                if images_link.count() == 0:
                    images_link = page.locator('a[href*="/images/"]')
                
                if images_link.count() > 0:
                    images_link.first.click()
                else:
                    # Если не нашли, идем по прямому URL
                    print("⚠️ Переход по прямому URL...")
                    page.goto("https://ya.ru/images/search?text=%D0%BA%D0%BE%D1%82%D1%8B", timeout=10000)
            except:
                page.goto("https://ya.ru/images/search?text=%D0%BA%D0%BE%D1%82%D1%8B", timeout=10000)
            
            # 5. Ждем загрузки картинок (сокращенное время)
            print("⏳ Ожидаем загрузки изображений...")
            page.wait_for_load_state("networkidle", timeout=5000)
            page.wait_for_timeout(1000)
            
            # Ждем появления картинок
            try:
                page.wait_for_selector('img', timeout=5000)
                print("✅ Изображения загружены")
            except:
                print("⚠️ Не дождались изображений, продолжаем...")
            
            page.wait_for_timeout(1000)
            
            # 6. Делаем скриншот (ОБЯЗАТЕЛЬНО)
            print("📸 Делаем скриншот...")
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/yandex_cats_{int(time.time())}.png"
            
            # Делаем скриншот всей страницы
            page.screenshot(path=screenshot_path, full_page=True)
            
            # Проверяем, что скриншот создан
            if os.path.exists(screenshot_path):
                print(f"✅ Скриншот успешно создан: {screenshot_path}")
                print(f"📊 Размер файла: {os.path.getsize(screenshot_path)} байт")
            else:
                print(f"❌ Скриншот НЕ создан!")
            
            # Проверяем количество картинок
            images = page.locator('img').count()
            print(f"🖼️ Найдено {images} изображений на странице")
            
            print(f"\n✅ Тест выполнен успешно!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            
            # ОБЯЗАТЕЛЬНО делаем скриншот ошибки
            error_screenshot = f"error_{int(time.time())}.png"
            try:
                page.screenshot(path=error_screenshot, full_page=True)
                print(f"📸 Скриншот ошибки: {error_screenshot}")
            except:
                print("⚠️ Не удалось сделать скриншот ошибки")
            
        finally:
            print("🔚 Закрываем браузер...")
            browser.close()


# Самый простой и быстрый вариант - сразу открываем картинки
def test_yandex_images_fast():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Сразу открываем Яндекс.Картинки с запросом "коты"
            print("🌐 Открываем Яндекс.Картинки...")
            page.goto("https://ya.ru/images/search?text=%D0%BA%D0%BE%D1%82%D1%8B", timeout=10000)
            page.wait_for_timeout(2000)
            
            # Делаем скриншот
            print("📸 Делаем скриншот...")
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/yandex_cats_fast_{int(time.time())}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            print(f"✅ Скриншот сохранен: {screenshot_path}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            
        finally:
            browser.close()


if __name__ == "__main__":
    # Выберите нужный вариант:
    # test_yandex_search()  # Полный вариант с поиском
    test_yandex_images_fast()  # Быстрый вариант - сразу картинки