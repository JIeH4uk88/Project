import pytest
import allure
from pages.auth_page import AuthPage
from pages.profile_page import ProfilePage
import uuid
import logging

logger = logging.getLogger(__name__)


@allure.epic("Авторизация")
@allure.feature("Регистрация")
class TestAuth:

    @allure.title("Позитивный тест: Полный цикл регистрации -> Редирект -> Логин")
    @allure.description("Тест проверяет полный цикл регистрации нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_register_new_user(self, driver, base_url):
        logger.info("Начало теста: Регистрация нового пользователя")

        with allure.step("Перейти на страницу регистрации"):
            register_page = ProfilePage(driver)
            register_page.navigate_to(base_url + "/register")
            register_page.take_screenshot("registration_page")

        with allure.step("Заполнить форму регистрации"):
            unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
            logger.debug(f"Сгенерирован новый пользователь: {unique_email}")

            register_page.register(
                first_name="Test",
                last_name="User",
                email=unique_email,
                phone="+79990001122",
                password="password123"
            )
            register_page.take_screenshot("after_registration_submit")

        with allure.step("Проверка редиректа на /login"):
            register_page.wait_for_page_load()
            current_url = register_page.get_current_url()
            assert "/login" in current_url, f"Ожидался редирект на /login, получен: {current_url}"
            logger.info(f"Редирект выполнен на: {current_url}")

        with allure.step("Проверить, что на странице входа есть поле email"):
            auth_page = AuthPage(driver)
            auth_page.wait_for_element(auth_page.email_input, timeout=10)
            auth_page.take_screenshot("login_page_after_redirect")

        logger.info("Тест завершен успешно")

    @allure.title("Позитивный тест: Вход существующего пользователя")
    @allure.description("Тест проверяет вход существующего пользователя с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_login_success(self, driver, base_url, existing_user_1):
        logger.info("Начало теста: Вход существующим пользователем")

        with allure.step("Перейти на страницу входа"):
            login_page = AuthPage(driver)
            login_page.navigate_to(base_url + "/login")
            login_page.take_screenshot("login_page")

        with allure.step("Выполнить вход с валидными данными"):
            login_page.login(
                existing_user_1["email"],
                existing_user_1["password"]
            )

        with allure.step("Проверка наличия кнопки Добавить новость"):
            login_page.wait_for_element(login_page.add_news_link, timeout=10)
            add_news_visible = login_page.is_element_visible(login_page.add_news_link)
            assert add_news_visible, "Кнопка 'Добавить новость' не отображается после входа"
            login_page.take_screenshot("after_login")

        logger.info("Тест завершен успешно")

    @allure.title("Негативный тест: Вход с неверным паролем")
    @allure.description("Тест проверяет, что вход с неверным паролем не выполняется")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_wrong_password(self, driver, base_url, existing_user_1):
        logger.info("Начало теста: Вход с неправильным паролем")

        with allure.step("Перейти на страницу входа"):
            login_page = AuthPage(driver)
            login_page.navigate_to(base_url + "/login")
            login_page.take_screenshot("login_page")

        with allure.step("Попытка входа с неправильным паролем"):
            login_page.login(
                existing_user_1["email"],
                "wrong_password_123"
            )

        with allure.step("Проверка появления ошибки"):
            login_page.should_see_error()
            login_page.take_screenshot("login_wrong_password")

        with allure.step("Проверить, что вход не выполнен (нет кнопки добавления новости)"):
            add_news_visible = login_page.is_element_visible(login_page.add_news_link, timeout=2)
            assert not add_news_visible, "Кнопка добавления новости отображается, хотя вход должен был провалиться"

        logger.info("Тест завершен успешно")

    @allure.title("Негативный тест: Регистрация с существующим email")
    @allure.description("Тест проверяет, что регистрация с уже существующим email невозможна")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_register_existing_email(self, driver, base_url, existing_user_1):
        logger.info("Начало теста: Регистрация с существующим email")

        with allure.step("Перейти на страницу регистрации"):
            register_page = ProfilePage(driver)
            register_page.navigate_to(base_url + "/register")
            register_page.take_screenshot("register_page")

        with allure.step("Попытка регистрации с существующим email"):
            register_page.register(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="+79990001122",
                password="password123"
            )
            register_page.take_screenshot("after_register_existing_email")

        with allure.step("Проверка появления ошибки"):
            register_page.should_see_registration_error()
            register_page.take_screenshot("register_existing_email_error")

        with allure.step("Проверить, что редирект не произошел (страница регистрации видна)"):
            current_url = register_page.get_current_url()
            assert "/register" in current_url or "register" in current_url, \
                f"Ожидалась страница регистрации, получен: {current_url}"

        logger.info("Тест завершен успешно")

    @allure.title("Негативный тест: Вход с несуществующим email")
    @allure.description("Тест проверяет, что вход с несуществующим email невозможен")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_login_nonexistent_email(self, driver, base_url):
        logger.info("Начало теста: Вход с несуществующим email")

        with allure.step("Перейти на страницу входа"):
            login_page = AuthPage(driver)
            login_page.navigate_to(base_url + "/login")
            login_page.take_screenshot("login_page")

        with allure.step("Попытка входа с несуществующим email"):
            login_page.login(
                "nonexistent@example.com",
                "password123"
            )

        with allure.step("Проверка появления ошибки"):
            login_page.should_see_error()
            login_page.take_screenshot("login_nonexistent_email")

        with allure.step("Проверить, что вход не выполнен"):
            add_news_visible = login_page.is_element_visible(login_page.add_news_link, timeout=2)
            assert not add_news_visible, "Кнопка добавления новости отображается, хотя вход должен был провалиться"

        logger.info("Тест завершен успешно")