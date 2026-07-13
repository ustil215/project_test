from playwright.sync_api import sync_playwright


def test_ochen_burger_menu():
    """Открывает бургер-меню (три точки) на сайте ochen.team и выводит в консоль
    названия всех пунктов меню (span) вместе со ссылками, куда они ведут"""

    with sync_playwright() as p:
        # Запускаем именно Google Chrome, а не bundled Chromium
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=300
        )
        page = browser.new_page(viewport={"width": 1440, "height": 840})

        print("🚀 Открываем сайт...")
        page.goto("https://ochen.team/", timeout=60000)
        page.wait_for_timeout(3000)

        # Проверяем, что оказались на главной странице
        assert page.url.rstrip("/") == "https://ochen.team", \
            f"Ожидали главную страницу, но получили {page.url}"
        print(f"✅ Главная страница открыта: {page.url}")

        # Ищем бургер-меню (три точки) в хедере и кликаем по нему
        print("🔍 Ищем бургер-меню в хедере...")
        burger_button = page.locator('header button[aria-label="открыть меню"]')
        assert burger_button.is_visible(timeout=5000), "Бургер-меню не найдено в хедере"

        print("🖱️ Открываем бургер-меню...")
        burger_button.click()
        page.wait_for_timeout(2000)

        # Ищем контейнер открывшегося меню
        menu_container = page.locator('div[class*="SGMyaq__Root"]')
        assert menu_container.count() > 0, "Контейнер бургер-меню не найден после клика"
        assert menu_container.first.is_visible(), "Бургер-меню не отобразилось после клика"
        print("✅ Бургер-меню открыто")

        # Собираем все li внутри контейнера меню
        menu_items = menu_container.first.locator("li").all()
        assert len(menu_items) > 0, "В бургер-меню не найдено ни одного пункта (li)"
        print(f"📋 Найдено {len(menu_items)} пунктов меню")

        # Собираем название (span) и ссылку (href) по каждому пункту
        results = []
        for li in menu_items:
            span = li.locator("span[data-title]").first
            link = li.locator("a").first

            title = span.get_attribute("data-title") if span.count() > 0 else None
            href = link.get_attribute("href") if link.count() > 0 else None

            if title is None:
                title = (li.text_content() or "").strip()

            results.append((title, href))

        # Выводим итоговый результат в консоль
        print("\n" + "=" * 50)
        print("📊 ПУНКТЫ БУРГЕР-МЕНЮ:")
        print("=" * 50)
        for title, href in results:
            print(f"{title} - {href}")

        # Каждый пункт меню должен иметь и название, и ссылку
        for title, href in results:
            assert title, f"У пункта меню отсутствует название: {title!r} - {href!r}"
            assert href, f"У пункта меню '{title}' отсутствует ссылка"

        browser.close()


if __name__ == "__main__":
    test_ochen_burger_menu()
    print("\n🎉 Тест выполнен успешно!")
