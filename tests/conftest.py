import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Тестовые данные
TEST_USER_1 = {
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Тест",
    "last_name": "Пользователь",
    "phone": "+79991234567"
}

TEST_USER_2 = {
    "email": "test2@example.com",
    "password": "password321",
    "first_name": "Тест2",
    "last_name": "Пользователь2",
    "phone": "+79991234568"
}


@pytest.fixture(scope="function")
def driver():
    logger.info("Создание WebDriver")

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)  # Неявное ожидание 5 секунд

    yield driver

    logger.info("Закрытие WebDriver")
    driver.quit()


@pytest.fixture(scope="function")
def existing_user_1():
    return TEST_USER_1


@pytest.fixture(scope="function")
def existing_user_2():
    return TEST_USER_2


@pytest.fixture(scope="function")
def base_url():
    """Базовый URL приложения"""
    return "https://archiscope.ru"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = "screenshots/failures"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{item.name}_{timestamp}.png"

            try:
                driver.save_screenshot(screenshot_path)
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure screenshot: {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )

                html_content = driver.page_source
                allure.attach(
                    html_content,
                    name=f"Page HTML: {item.name}",
                    attachment_type=allure.attachment_type.HTML
                )
                logger.info(f"Скриншот сохранен: {screenshot_path}")
            except Exception as e:
                logger.error(f"Не удалось сохранить скриншот: {e}")