import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.short_wait = WebDriverWait(driver, 5)
        self.timeout = 30

    def _get_locator(self, selector):
        if isinstance(selector, tuple):
            return selector

        if isinstance(selector, str):
            if selector.startswith("//") or selector.startswith("("):
                return ("xpath", selector)
            elif selector.startswith("css="):
                return ("css selector", selector[4:])
            elif selector.startswith("text="):
                return ("xpath", f"//*[contains(text(), '{selector[5:]}')]")
            elif selector.startswith("id="):
                return ("id", selector[3:])
            elif selector.startswith("class="):
                return ("class name", selector[6:])
            else:
                return ("css selector", selector)

        raise ValueError(f"Неподдерживаемый тип селектора: {type(selector)}")

    def find_element(self, selector, timeout=None) -> WebElement:
        timeout = timeout or self.timeout
        by, value = self._get_locator(selector)

        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Найден элемент: {selector}")
            return element
        except TimeoutException:
            raise AssertionError(f"Элемент не найден за {timeout} секунд: {selector}")

    def find_elements(self, selector, timeout=None) -> list:
        timeout = timeout or self.timeout
        by, value = self._get_locator(selector)

        wait = WebDriverWait(self.driver, timeout)
        try:
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return elements
        except TimeoutException:
            return []

    @allure.step("Кликнуть на элемент: {selector}")
    def click(self, selector, timeout=None):
        timeout = timeout or self.timeout
        by, value = self._get_locator(selector)

        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            logger.info(f"Клик на: {selector}")
            return self
        except TimeoutException:
            raise AssertionError(f"Элемент не кликабелен: {selector}")

    @allure.step("Заполнить поле: {value}")
    def fill(self, selector, value, timeout=None):
        timeout = timeout or self.timeout
        element = self.find_element(selector, timeout)
        element.clear()
        element.send_keys(value)
        logger.info(f"Заполнено поле {selector}: {value}")
        return self

    @allure.step("Получить текст элемента")
    def get_text(self, selector, timeout=None) -> str:
        element = self.find_element(selector, timeout)
        return element.text

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, selector, timeout=5) -> bool:
        try:
            by, value = self._get_locator(selector)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидать видимости элемента")
    def wait_for_element(self, selector, timeout=None):
        """Ожидание видимости элемента"""
        timeout = timeout or self.timeout
        by, value = self._get_locator(selector)

        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of_element_located((by, value)))
        return self

    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_load(self, timeout=None):
        """Ожидание загрузки страницы"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return self

    @allure.step("Навигация на URL: {url}")
    def navigate_to(self, url):
        if url.startswith("http"):
            full_url = url
        else:
            base_url = "https://archiscope.ru"
            full_url = f"{base_url}{url}" if url.startswith("/") else f"{base_url}/{url}"

        self.driver.get(full_url)
        self.wait_for_page_load()
        logger.info(f"Переход на: {full_url}")
        return self

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name=None):
        if name is None:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = f"{screenshot_dir}/{name}.png"
        self.driver.save_screenshot(screenshot_path)

        allure.attach.file(
            screenshot_path,
            name=f"Screenshot: {name}",
            attachment_type=allure.attachment_type.PNG
        )

        logger.info(f"Скриншот сохранен: {screenshot_path}")
        return self

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:

        return self.driver.current_url