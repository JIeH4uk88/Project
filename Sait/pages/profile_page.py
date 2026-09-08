import allure
from base_page import BasePage
from playwright.sync_api import Page, expect


class ProfilePage(BasePage):

    def fill_form(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.page.locator('input[name="first_name"]').fill(first_name)
        self.page.locator('input[name="last_name"]').fill(last_name)
        self.page.locator('input[name="email"]').fill(email)
        self.page.locator('input[name="phone"]').fill(phone)
        self.page.locator('input[name="password"]').fill(password)

    def go_to_profile(self):
        logger.info("Переход в профиль")
        self.wait_for_element(self.profile_link)
        self.page.click(self.profile_link)
        self.page.wait_for_load_state("networkidle")

    def update_name(self, new_name: str):
        logger.info(f"Обновление имени на: {new_name}")
        self.wait_for_element(self.name_input)
        self.page.fill(self.name_input, new_name)

    def update_email(self, new_email: str):
        logger.info(f"Обновление email на: {new_email}")
        self.wait_for_element(self.email_input)
        self.page.fill(self.email_input, new_email)

    def save_profile(self):
        logger.info("Сохранение профиля")
        self.page.click(self.save_profile_button)
        self.page.wait_for_load_state("networkidle")

    def submit(self):
        self.page.get_by_role("button", name="Зарегистрироваться").click()
        self.page.wait_for_load_state("networkidle")

    def register(self, first_name: str, last_name: str, email: str, phone: str, password: str):
        self.fill_form(first_name, last_name, email, phone, password)
        self.submit()
        self.page.wait_for_url("**/login", timeout=10000)

    def should_see_error(self):
        expect(self.page.locator(".alert-error")).to_be_visible()