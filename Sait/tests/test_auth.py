import pytest
from pages.auth_page import AuthPage
from pages.profile_page import ProfilePage
from playwright.sync_api import expect
import uuid
import logging
import allure

@allure.epic("Авторизация")
@allure.feature("Регистрация")
class TestAuth:

    @allure.title("Позитивный тест: Полный цикл регистрации -> Редирект -> Логин")
    @allure.description("Тест проверяет полный цикл регистрации нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_new_user(self, page):
        logger.info("Начало теста: Регистрация нового пользователя")
        register_page = ProfilePage(page)
        register_page.navigate("/register")

        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        logging.debug(f"Сгенерирован новый пользователь: {unique_email}")
        register_page.register(
            first_name="Test",
            last_name="User",
            email=unique_email,
            phone="+79990001122",
            password="password123"
        )
        with allure.step("Проверка редиректа на /login"):
            assert "/login" in page.url
        register_page.take_screenshot("after_registration")
        logger.info("Тест завершен успешно")

    @allure.title("Вход существующего пользователя")
    @allure.description("Тест проверяет вход существующего пользователя с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, page):
        logger.info("Начало теста: Вход существующим пользователем")
        login_page = AuthPage(page)
        login_page.navigate("/login")
        login_page.login("test@example.com", "password123")

        with allure.step("Проверка наличия кнопки Добавить новость"):
            add_news_btn = page.get_by_role("link", name="Добавить новость")
            expect(add_news_btn).to_be_visible(timeout=10000)

        login_page.take_screenshot("after_login")
        logger.info("Тест завершен успешно")

    @allure.title("Вход с неверным паролем")
    @allure.description("Тест проверяет, что вход с неверным паролем не выполняется")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self, page):
        logger.info("Начало теста: Вход с неправильным паролем")
        login_page = AuthPage(page)
        login_page.navigate("/login")
        with allure.step("Проверка появления ошибки при попытке входа с неправильным паролем"):
            login_page.login("test@example.com", "password123")
            login_page.should_see_error()
        logger.info("Тест завершен успешно")

    @allure.title("Негативный тест: Регистрация с существующим email")
    @allure.description("Тест проверяет, что регистрация с уже существующим email невозможна")
    @allure.severity(allure.severity_level.NORMAL)

    def test_login_nonexistent_email(self, page):
        logger.info("Начало теста: Вход несуществующим email")
        login_page = AuthPage(page)
        login_page.navigate("/login")
        with allure.step("Проверка появления ошибки при попытке входа с несуществующим email"):
            login_page.login("nonexistent@example.com", "password123")
            login_page.should_see_error()
        logger.info("Тест завершен успешно")