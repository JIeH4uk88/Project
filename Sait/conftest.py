import pytest
from playwright.sync_api import Browser, BrowserContext
import allure
import logging
from pathlib import Path


BASE_URL = "https://archiscope.ru"

logger = logging.getLogger(__name__)

ARTIFACTS_DIR = Path("artifacts")
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"

for directory in [ARTIFACTS_DIR, TRACES_DIR, SCREENSHOTS_DIR, VIDEOS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser, request):
    test_name = request.node.name

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",
        record_video_dir=str(VIDEOS_DIR)
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context._test_name = test_name
    context._test_failed = False

    yield context

    if context._test_failed:
        trace_path = TRACES_DIR / f"{test_name}.zip"
        context.tracing.stop(path=str(trace_path))

        # Прикрепление trace
        allure.attach.file(
            str(trace_path),
            name="Playwright Trace",
            attachment_type="application/zip"
        )
    else:
        context.tracing.stop()

    # Видео
    video_path = VIDEOS_DIR / f"{test_name}.webm"
    if context._test_failed:
        allure.attach.file(
            str(video_path),
            name="Video",
            attachment_type="video/webm"
        )
    elif video_path.exists():
        video_path.unlink()

    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    page = context.new_page()
    page.set_default_timeout(15000)

    yield page

    if request.node.rep_call.failed:
        context._test_failed = True

        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        # Прикрепление скриншота
        allure.attach.file(
            str(screenshot_path),
            name="Screenshot",
            attachment_type="image/png"
        )

    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function", autouse=True)
def allure_setup(request):
    test_name = request.node.name.replace("test_", "").replace("_", " ").title()
    allure.dynamic.title(test_name)
    if request.node.obj.__doc__:
        allure.dynamic.description(request.node.obj.__doc__)

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture(scope="function")
def profile_page(page: Page) -> ProfilePage:
    return ProfilePage(page)