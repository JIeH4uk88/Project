import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class AuthPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.email_input = (By.NAME, "email")
        self.password_input = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[contains(text(), 'Войти')]")
        self.error_message = (By.CSS_SELECTOR, ".error, .alert-danger, .invalid-feedback")
        self.add_news_link = (By.XPATH, "//a[contains(text(), 'Добавить новость')]")

        self.login_link = (By.XPATH, "//a[contains(text(), 'Войти')]")

    @allure.step("Перейти на страницу входа")
    def navigate_to_login(self):
        if "/login" not in self.driver.current_url:
            self.click(self.login_link)
        self.wait_for_element(self.email_input)
        return self

    @allure.step("Выполнить вход: {email}")
    def login(self, email: str, password: str):
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        self.wait_for_page_load()
        return self

    @allure.step("Проверить наличие ошибки")
    def should_see_error(self):
        error_visible = self.is_element_visible(self.error_message, timeout=5)
        assert error_visible, "Сообщение об ошибке не отображается"

        add_news_visible = self.is_element_visible(self.add_news_link, timeout=2)
        assert not add_news_visible, "Кнопка добавления новости отображается, хотя вход должен был провалиться"

        error_text = self.get_text(self.error_message)
        logger.info(f"Текст ошибки: {error_text}")
        allure.attach(error_text, "Текст ошибки", allure.attachment_type.TEXT)

        return self

    @allure.step("Проверить успешный вход")
    def should_see_success(self):
        """Проверка успешного входа"""
        add_news_visible = self.is_element_visible(self.add_news_link, timeout=10)
        assert add_news_visible, "Кнопка 'Добавить новость' не отображается после входа"
        return self