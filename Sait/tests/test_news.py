import pytest
import allure
from pages.auth_page import AuthPage
from pages.news_page import NewsPage


class TestNewsCreation:

    def test_news_list_loads(self, page):
        news_list = NewsPage(page)
        news_list.navigate("/")
        news_list.should_have_news()
        news_list.take_screenshot("news_list")

    def test_search_news(self, page):
        news_list = NewsPage(page)
        news_list.navigate("/")
        news_list.search("Банк")
        news_list.should_have_news(min_count=0)

    def test_pagination(self, page):
        news_list = NewsPage(page)
        news_list.navigate("/")
        news_list.should_have_pagination()

    def test_navigate_to_detail(self, page):
        news_list = NewsPage(page)
        news_list.navigate("/")
        first_card_title = page.locator(".card-title").first.text_content()
        news_list.click_news(first_card_title)
        assert "/news/" in page.url

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_without_title(self, auth_page, news_page):
        logger.info("=== Тест создания новости без заголовка ===")

        news_page.navigate_to("https://archiscope.ru/news")
        news_page.create_news("", "Тестовый текст новости без заголовка")

        with allure.step("Проверка сообщения об ошибке"):
            error_message = news_page.get_error_message()
            assert error_message, "Сообщение об ошибке не отображено"
            assert "заголовок" in error_message.lower() or "title" in error_message.lower(), \
                "Сообщение об ошибке не содержит информацию о заголовке"
            logger.info(f"Получено сообщение об ошибке: {error_message}")

        logger.info("=== Тест создания новости без заголовка завершен ===")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_news_without_text(self, auth_page, news_page):
        logger.info("=== Тест создания новости без текста ===")

        news_page.navigate_to("https://archiscope.ru/news")
        news_page.create_news("Новость без текста", "")

        with allure.step("Проверка сообщения об ошибке"):
            error_message = news_page.get_error_message()
            assert error_message, "Сообщение об ошибке не отображено"
            assert "текст" in error_message.lower() or "text" in error_message.lower(), \
                "Сообщение об ошибке не содержит информацию о тексте"
            logger.info(f"Получено сообщение об ошибке: {error_message}")

        logger.info("=== Тест создания новости без текста завершен ===")

        