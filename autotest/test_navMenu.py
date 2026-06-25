from playwright.sync_api import sync_playwright

def test_navigation_links():
    """Проверяет кнопки навигации на сайте chulakov.team"""
    
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.chromium.launch(
            headless=False,  # Видимый режим
            slow_mo=300      # Замедляем действия
        )
        page = browser.new_page()
        
        print("🚀 Открываем сайт...")
        page.goto("https://chulakov.team/", timeout=60000)
        
        # Ждем загрузки основного контента
        page.wait_for_timeout(3000)
        
        # Список кнопок с их href
        buttons = [
            {"text": "Вакансии", "href": "/vacancies"},
            {"text": "Мероприятия", "href": "/events"},
            {"text": "Начало карьеры", "href": "/student"},
            {"text": "Офис", "href": "/office"}
        ]
        
        results = {}
        
        for button in buttons:
            print(f"\n🔍 Проверяем кнопку: '{button['text']}'")
            
            try:
                # Находим ссылку по href
                link = page.locator(f"a[href='{button['href']}']").first
                
                # Проверяем, что кнопка существует и видима
                if not link.is_visible(timeout=3000):
                    print(f"   ⚠️ Кнопка не видна, пробуем найти по тексту...")
                    link = page.locator(f"span[data-title='{button['text']}']").locator("..").first
                    if not link.is_visible(timeout=3000):
                        results[button['text']] = "❌ Не найдена"
                        continue
                
                href = link.get_attribute("href")
                print(f"   Href: {href}")
                
                # Проверяем статус страницы до клика
                full_url = f"https://chulakov.team{href}"
                response = page.request.get(full_url)
                print(f"   Статус до клика: {response.status} {'✅' if response.status == 200 else '❌'}")
                
                if response.status != 200:
                    results[button['text']] = f"❌ Ошибка {response.status}"
                    continue
                
                # Кликаем по кнопке
                print(f"   🖱️ Кликаем...")
                link.click()
                
                # Вместо wait_for_load_state используем просто ожидание
                page.wait_for_timeout(2000)
                
                # Проверяем текущий URL
                current_url = page.url
                print(f"   Текущий URL: {current_url}")
                
                # Проверяем, что URL содержит нужный путь
                if button['href'] in current_url:
                    print(f"   ✅ Переход на {button['text']} выполнен")
                    
                    # Проверяем статус текущей страницы
                    try:
                        current_response = page.request.get(current_url)
                        if current_response.status == 200:
                            print(f"   ✅ Страница загружена (код {current_response.status})")
                            results[button['text']] = "✅ Успешно"
                        else:
                            print(f"   ⚠️ Код ответа: {current_response.status}")
                            results[button['text']] = f"⚠️ Код {current_response.status}"
                    except:
                        print(f"   ⚠️ Не удалось проверить статус")
                        results[button['text']] = "⚠️ Статус не проверен"
                else:
                    print(f"   ⚠️ URL не совпадает")
                    results[button['text']] = "⚠️ URL отличается"
                
                # Возвращаемся на главную
                print(f"   🔙 Возвращаемся...")
                page.goto("https://chulakov.team/", timeout=30000)
                page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"   ❌ Ошибка: {str(e)[:80]}")
                results[button['text']] = f"❌ Ошибка"
                # Пытаемся вернуться на главную
                try:
                    page.goto("https://chulakov.team/", timeout=30000)
                    page.wait_for_timeout(2000)
                except:
                    pass
        
        # Выводим итоговые результаты
        print("\n" + "="*50)
        print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
        print("="*50)
        for button, result in results.items():
            print(f"{button}: {result}")
        
        # Проверяем результат
        all_passed = all("✅" in result for result in results.values())
        if all_passed:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            success = True
        else:
            print("\n⚠️ ЕСТЬ ПРОБЛЕМЫ, проверьте вывод выше")
            success = False
        
        browser.close()
        return success

if __name__ == "__main__":
    print("🚀 Запуск автотеста навигации...")
    success = test_navigation_links()
    exit(0 if success else 1)