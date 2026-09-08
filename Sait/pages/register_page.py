import allure
from playwright.sync_api import Page, expect
import logging
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = "input[name='name']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.password_confirmation_input = "input[name='password_confirmation']"
        self.register_button = "button[type='submit']"
        self.success_message = ".alert-success"

    def register(self, name: str, email: str, password: str, password_confirmation: str = None):
        if password_confirmation is None:
            password_confirmation = password

        logger.info(f"Регистрация пользователя: {email}")
        self.wait_for_element(self.name_input)
        self.page.fill(self.name_input, name)
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.fill(self.password_confirmation_input, password_confirmation)
        self.page.click(self.register_button)
        logger.info("Форма регистрации отправлена")

    def is_registration_successful(self) -> bool:
        return self.is_element_visible(self.success_message)

    def get_success_message(self) -> str:
        self.wait_for_element(self.success_message)
        message = self.page.text_content(self.success_message)
        logger.info(f"Сообщение об успехе: {message}")
        return message