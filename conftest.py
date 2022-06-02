import logging
import os
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = None

def pytest_configure(config):
    global logger

    try:
        level = config.getoption('log-level'),
    except ValueError as e:
        level = logging.DEBUG

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

def setup_module(module):
    print("\n")
    logger.info("Running setup for MODULE [%s]" %module.__name__)

def teardown_module(module):
    print("\n")
    logger.info("Running teardown for MODULE [%s]" %module.__name__)
    pass


# Initializing webdriver and url with environment variables. Default browser is set to chrome and URL is taken from the
# test suite
@pytest.fixture(scope="session")
def driver():
    global driver
    global url

    browser = os.environ['browser'] if "browser" in os.environ else "chrome"
    if browser == "firefox":
        driver = Firefox(GeckoDriverManager().install())
    else:
        driver = Chrome(ChromeDriverManager().install())
    print("Env browser: " + browser)

    if "url" in os.environ:
        url = os.environ['url']
        driver.get(url)
        print("Env URL: " + url)

    driver.maximize_window()

    yield driver
    driver.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    # For tests inside ui_tests, when the test fails, automatically take a screenshot and display it in the html report
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    location = getattr(report, 'location', [])

    if "ui_tests" in location[0] and (report.when == 'call' or report.when == "setup"):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot():
    return driver.get_screenshot_as_base64()
