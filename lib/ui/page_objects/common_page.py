import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class CommonPage(object):

    """ This class is the parent class for BasePage, PageSection, and PageIframe
    It provides helper methods for interacting with Page element(s), such as clicking, text inputs, file uploads etc.
    :type logger: logging instance
    """

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def click(self, locator, timeout=None, params=None, key=None):
        """
        Click web element
        :param locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        :param timeout: (optional) num. of seconds to wait for element
        :param params: (optional) locator parameters in dict type
        :param key: (optional) Keys code (ex: Keys.LEFT_SHIFT)
        """
        self._click(locator, timeout, params, key)

    def input_text(self, locator, text, timeout=None, visible=True, with_clear=False, with_enter=False, params=None):
        """
        Enter text
        :param locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        :param text: text to input
        :param timeout: (optional) # of seconds to wait for element
        :param visible: element visibility on page
        :param with_clear: clear the input field
        :param with_enter: press ENTER key after text input
        :param params: (optional) locator parameters in dict type
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator, timeout, params, visible)

        # focus on the element
        self.click(element)

        # clear input field
        if with_clear:
            element.clear()
            self.click(element)

        # input text
        element.send_keys(text)

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.perform()

        # press ENTER
        if with_enter:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()

    def _click(self, locator, timeout=None, params=None, key=None):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        :param timeout: (optional) # of seconds to wait for element
        :param params: (optional) locator parameters in dict type
        :param key: (optional) locator parameters in dict type
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator, timeout, params)

        if key:
            actions = ActionChains(self.driver)
            actions.key_down(key)
            actions.click(element)
            actions.key_up(key)
            actions.perform()
        else:
            element.click()

    def _get_element(self, locator, timeout=None, params=None, visible=False):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        :param timeout:
        :param params:
        :param visible:
        :return: returns WebElement
        """
        try:
            wait = WebDriverWait(driver=self.driver, timeout=timeout or self.timeout)
            expected_condition = EC.visibility_of_element_located if visible else EC.presence_of_element_located
            element = wait.until(expected_condition(locator))
            return element
        except NoSuchElementException as exception:
            self.logger.info(f"\n * ELEMENT NOT FOUND! : {locator}")
            self.logger.info(exception)

    def hover(self, locator):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        """
        element = self._get_element(locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def wait_for_element(self, locator):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.info("\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s" % locator)
            self.driver.quit()

    def is_displayed(self, *locator):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        """
        try:
            return True if WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(*locator)) else False
        except NoSuchElementException as exception:
            self.logger.info("\n * ELEMENT NOT FOUND! : %s" % (locator[0]))
            self.logger.info(exception)
            self.driver.quit()

    def click_cookies_continue(self):
        try:
            elem = self.driver.find_element_by_class_name(self.cookies_element_class)
            elem.click()
        except NoSuchElementException as exception:
            self.logger.info("No cookies element found at " + self.get_url())
            self.logger.info(exception)
            pass

    def move_to_and_click(self, locator):
        """
        :param locator: locator: locator tuple (ex: locator=(By.ID, 'some_id')) or WebElement instance
        """
        self.scroll_element_into_view(locator)
        self.click(locator)

    def get_text(self, locator, params=None, timeout=None, visible=True):
        """
        Get text or value from element based on locator with optional parameters.
        :param locator: element identifier
        :param params: (optional) locator parameters
        :param timeout: (optional) time to wait for text (default: None)
        :param visible: should element be visible before getting text (default: True)
        :return: element text, value or empty string
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator, timeout, params, visible)

        if element and element.text:
            return element.text
        else:
            try:
                return element.get_attribute('value')
            except AttributeError:
                return ""

    def select_from_drop_down_by_index(self, locator, index):
        """
                Select option from drop down widget using value.
                :param locator: locator tuple or WebElement instance
                :param index: int
                :param params: (optional) locator parameters
                :return: None
                """
        from selenium.webdriver.support.ui import Select

        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator)

        Select(element).select_by_index(index)

    def select_from_drop_down_by_value(self, locator, value):
        """
        Select option from drop down widget using value.
        :param locator: locator tuple or WebElement instance
        :param value: string
        :param params: (optional) locator parameters
        :return: None
        """
        from selenium.webdriver.support.ui import Select

        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator)

        Select(element).select_by_value(value)

    def select_from_drop_down_by_text(self, drop_down_locator, option_locator, option_text, params=None):
        """
        Select option from drop down widget using text.
        :param drop_down_locator: locator tuple (if any, params needs to be in place) or WebElement instance
        :param option_locator: locator tuple (if any, params needs to be in place)
        :param option_text: text to base option selection on
        :param params: Dictionary containing dictionary of params
        :return: None
        """
        # Open/activate drop down
        self.click(drop_down_locator, params['drop_down'] if params else None)

        # Get options
        for option in self._get_element(option_locator, params['option'] if params else None):
            if self.get_text(option) == option_text:
                self.click(option)
                break

    def scroll_element_into_view(self, locator):
        """
        Scrolls an element into view.
        :param locator: selector of element or WebElement to scroll into view
        :return: None
        """
        element = locator
        if not isinstance(element, WebElement):
            element = self._get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView( true );", element)

    def wait_for_element_to_be_clickable_and_click(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        self.click(element)

    def click_element(self, locator1, locator):
        element = self.driver.find_element(locator1,locator)
        self.driver.execute_script("arguments[0].click();", element)
