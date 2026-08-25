import allure
from playwright.sync_api import Page, expect
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page, base_url: str= "https://archiscope.ru") -> None:
        self.page = page
        self.base_url = base_url

    def navigate_to(self, path: str = "/"):
        url = self.base_url + path
        logger.info(f"Переход на страницу {url}")
        with allure.step(f"Переход на страницу: {url}"):
            self.page.goto(f"{url}")
            self.page.wait_for_load_state("networkidle")

        logger.info(f"Страница загружена: {url}")
        return self

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, name: str = None):
        screenshot_path = f"screenshots/{name}.png"
        Path("artifacts/screenshots").mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=screenshot_path, full_page=True)
        allure.attach.file(screenshot_path, name=f"Screenshot {name}", attachment_type=allure.attachment_type.PNG)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return self

    def should_see_text(self, text: str):
        expect(self.page.get_by_text(text)).to_be_visible()
        return self

    def should_see_button(self, name: str):
        expect(self.page.get_by_role("button", name=name)).to_be_visible()
        return self