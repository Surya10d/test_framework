import os
from uritemplate import expand
from .common_page import CommonPage


class BasePage(CommonPage):

    def __init__(self, driver, timeout=10):
        """
        :param driver: WebDriver instance
        :param timeout: time to wait for locating element
        """
        super().__init__(timeout=timeout)
        self._driver = driver
        self.url = str(self.URL or '')

    @property
    def driver(self):
        return self._driver

    def load(self, **kwargs):
        """
        :param kwargs: keyword/value arguments
        """
        uri = expand(uri=self.url, **kwargs)
        self.driver.get(uri)

    def navigate_to(self, url):
        """
        :param url: string: Driver navigates to the specified URL
        """
        self.driver.get(url)

    def get_title(self):
        """
        :return: returns driver window title text
        """
        return self.driver.title

    def get_url(self):
        """
        :return: get current driver url
        """
        return self.driver.current_url


