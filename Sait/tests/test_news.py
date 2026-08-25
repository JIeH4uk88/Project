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