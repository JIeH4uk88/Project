import allure
from base_page import BasePage
from playwright.sync_api import Page, expect


class AuthPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.register_link = "a:has-text('Регистрация')"
        self.first_name_input = "input[name='first_name']"
        self.last_name_input = "input[name='last_name']"
        self.email_input = "input[name='email']"
        self.phone_input = "input[name='phone']"
        self.password_input = "input[name='password']"
        self.register_button = "button:has-text('Зарегистрироваться')"

        self.login_link = "a:has-text('Войти')"
        self.login_email_input = "textbox[name='user@example.com']"
        self.login_password_input = "textbox[name='••••••']"
        self.login_button = "button:has-text('Войти')"

    def register(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.fill_form(first_name, last_name, email, phone, password)
        self.submit()
        self.page.wait_for_url("**/login", timeout=10000)

    def fill_email(self, email: str):
        self.page.locator('input[type="email"]').fill(email)

    def fill_password(self, password: str):
        self.page.locator('input[type="password"]').fill(password)

    def submit(self):
        self.page.get_by_role("button", name="Войти").click()
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str):
        self.fill_email(email)
        self.fill_password(password)
        self.submit()
        return self
    def should_see_error(self):
        expect(self.page.locator(".alert-error")).to_be_visible()