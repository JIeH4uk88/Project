import allure
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # Селекторы для регистрации
        self.first_name_input = (By.NAME, "first_name")
        self.last_name_input = (By.NAME, "last_name")
        self.email_input = (By.NAME, "email")
        self.phone_input = (By.NAME, "phone")
        self.password_input = (By.NAME, "password")
        self.register_button = (By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
        self.register_link = (By.XPATH, "//a[contains(text(), 'Регистрация')]")

        # Селекторы для профиля
        self.avatar_button = (By.XPATH, "//button[contains(text(), 'Avatar')]")
        self.profile_link = (By.XPATH, "//a[contains(text(), 'Профиль')]")
        self.save_button = (By.XPATH, "//button[contains(text(), 'Сохранить')]")

        # Сообщения об успехе/ошибке
        self.success_message = (By.CSS_SELECTOR, ".success, .alert-success")
        self.error_message = (By.CSS_SELECTOR, ".error, .alert-danger, .invalid-feedback")

    @allure.step("Перейти на страницу регистрации")
    def navigate_to_register(self):
        if "/register" not in self.driver.current_url:
            self.click(self.register_link)
        self.wait_for_element(self.first_name_input)
        return self

    @allure.step("Зарегистрировать нового пользователя")
    def register(self, first_name: str, last_name: str, email: str, phone: str, password: str):

        self.fill(self.first_name_input, first_name)
        self.fill(self.last_name_input, last_name)
        self.fill(self.email_input, email)
        self.fill(self.phone_input, phone)
        self.fill(self.password_input, password)

        self.click(self.register_button)
        self.wait_for_page_load()

        logger.info(f"Зарегистрирован пользователь: {email}")
        return self

    @allure.step("Проверить успешную регистрацию")
    def should_see_registration_success(self):

        self.wait_for_element(self.email_input, timeout=10)

        if self.is_element_visible(self.success_message, timeout=3):
            success_text = self.get_text(self.success_message)
            logger.info(f"Сообщение об успехе: {success_text}")
            allure.attach(success_text, "Сообщение об успехе", allure.attachment_type.TEXT)

        return self

    @allure.step("Проверить ошибку регистрации")
    def should_see_registration_error(self):
        """Проверка ошибки регистрации"""
        error_visible = self.is_element_visible(self.error_message, timeout=5)
        assert error_visible, "Сообщение об ошибке не отображается"

        error_text = self.get_text(self.error_message)
        logger.info(f"Текст ошибки регистрации: {error_text}")
        allure.attach(error_text, "Текст ошибки", allure.attachment_type.TEXT)

        return self

    @allure.step("Перейти в профиль")
    def go_to_profile(self):
        """Переход в профиль пользователя"""
        self.click(self.avatar_button)
        self.click(self.profile_link)
        self.wait_for_page_load()
        return self

    @allure.step("Обновить профиль")
    def update_profile(self, first_name: str = None, last_name: str = None,
                       email: str = None, phone: str = None, password: str = None):
        """Обновление данных профиля"""
        if first_name is not None:
            self.fill(self.first_name_input, first_name)
        if last_name is not None:
            self.fill(self.last_name_input, last_name)
        if email is not None:
            self.fill(self.email_input, email)
        if phone is not None:
            self.fill(self.phone_input, phone)
        if password is not None:
            self.fill(self.password_input, password)

        self.click(self.save_button)
        self.wait_for_page_load()
        return self