import asyncio
from playwright.async_api import async_playwright

async def get_menu_items():
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🔄 Открываем сайт...")
        await page.goto("https://chulakov.team/")
        await page.wait_for_timeout(3000)
        
        print("🔄 Открываем бургер-меню...")
        await page.click('button[aria-label="открыть меню"]')
        await page.wait_for_timeout(2000)
        
        print("\n📋 Ищем контейнер меню...")
        
        # Ищем контейнер меню по классу
        menu_container = page.locator('div[class*="index-module__SGMyaq__Root"]')
        
        # Проверяем, найден ли контейнер
        if await menu_container.count() == 0:
            print("❌ Контейнер меню не найден!")
            print("🔍 Ищем все div с похожими классами...")
            
            # Отладочный вывод
            all_divs = await page.locator('div').all()
            for div in all_divs:
                class_name = await div.get_attribute('class') or ''
                if 'SGMyaq' in class_name or 'Root' in class_name:
                    print(f"  Найден div с классом: {class_name}")
            
            await browser.close()
            return
        
        print("✅ Контейнер меню найден!")
        
        # Ищем все элементы li внутри контейнера
        menu_items = await menu_container.locator('li').all()
        
        print(f"📋 Найдено {len(menu_items)} элементов li")
        
        # Собираем информацию о каждом пункте меню
        items = []
        
        for li in menu_items:
            # Ищем ссылку внутри li
            link = li.locator('a').first
            if await link.count() > 0:
                # Ищем span внутри ссылки (название пункта)
                span = link.locator('span').first
                if await span.count() > 0:
                    text = await span.text_content()
                else:
                    text = await link.text_content()
                
                # Получаем ссылку
                href = await link.get_attribute('href')
                
                # Очищаем текст
                if text:
                    text = text.strip()
                
                # Форматируем ссылку
                if href:
                    if href.startswith('/'):
                        href = f"https://chulakov.team{href}"
                    elif not href.startswith('http'):
                        href = f"https://chulakov.team/{href}"
                else:
                    href = "#"
                
                if text and text not in ['', ' ', '\n', '\t']:
                    items.append((text, href))
        
        # Выводим результат
        print("\n" + "=" * 70)
        if items:
            print(f"✅ Найдено {len(items)} пунктов меню:\n")
            for i, (text, href) in enumerate(items, 1):
                print(f"{i:2}. {text:<35} → {href}")
        else:
            print("❌ Не удалось найти пункты меню!")
            
            # Отладка: показываем содержимое контейнера
            print("\n🔍 Отладка: содержимое контейнера")
            html = await menu_container.inner_html()
            print(f"HTML контейнера:\n{html[:500]}...")
        
        print("\n" + "=" * 70)
        print(f"📊 Всего элементов: {len(items)}")
        
        # Делаем скриншот
        await page.screenshot(path="menu_result.png")
        print("📸 Скриншот сохранен: menu_result.png")
        
        await page.wait_for_timeout(5000)
        await browser.close()

# Запускаем
if __name__ == "__main__":
    asyncio.run(get_menu_items())