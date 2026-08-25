from base_page import BasePage, expect
import logging

logger = logging.getLogger(__name__)


class NewsPage(BasePage):

    def get_news_cards(self):
        return self.page.locator(".card")

    def get_news_count(self) -> int:
        return self.get_news_cards().count()

    def click_news(self, title: str):
        self.page.get_by_text(title, exact=False).first.click()

    def search(self, query: str):
        search_input = self.page.get_by_placeholder("Поиск...")
        search_input.fill(query)
        search_input.press("Enter")
        self.page.wait_for_timeout(500)

    def go_to_page(self, page_num: int):
        self.page.get_by_role("button", name=str(page_num)).click()

    def should_have_pagination(self):
        expect(self.page.locator(".join").last).to_be_visible()

    def get_all_tags(self):
        return self.page.locator(".badge-outline").all_text_contents()

    def should_have_news(self, min_count: int = 1):
        expect(self.get_news_cards().first).to_be_visible()
        assert self.get_news_count() >= min_count
