from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)

import pytest

from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from tests.functional import feature_file_path
from lib.ui.page_objects.sample_ui.contact_confirm import ContactConfirm
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class TestContactConfirm:
    # @pytest.fixture(autouse=True, scope='module')
    # def setup(self, driver, request):
    #     chrome_options = ChromeOptions()
    #     driver = Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    #
    #     def fin():
    #         driver.quit()
    #         request.addfinalizer(fin)

    # def test_start(self, driver):
    #     driver.get("https://www.google.co.in")

    # @pytest.fixture(autouse=True, scope="module")
    # def setup(self, request):
    #     chrome_options = ChromeOptions()
    #     self.driver = Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    @scenario(feature_file_path + 'ContactConfirm.feature', 'Check form is validated when there are no errors')
    def test_check_form_is_validated_when_there_are_no_errors(self):
        """Check form is validated when there are no errors."""

    @given('I am on the zoo website')
    def i_am_on_the_zoo_website(self):
        """I am on the zoowebsite."""
        self.contact_confirm = ContactConfirm()
        self.contact_confirm.load(self.driver)

    @when('I click the button of contact link')
    def i_click_the_button_of_contact_link(self):
        """I click the button of contact link."""
        self.contact_confirm.click_contact_btn()

    @when('populate the contact form')
    def populate_the_contact_form(self):
        """populate the contact form."""
        self.contact_confirm.enter_name_field("Chris")
        self.contact_confirm.enter_address_field("Galaxy")
        self.contact_confirm.enter_postcode_field("P2D F3F")
        self.contact_confirm.enter_email_field("light@star.com")
        self.contact_confirm.click_submit_message()

    @then('I close the browser')
    def i_close_the_browser(self):
        """I close the browser."""
        self.driver.close()

    @then('I should be on the contact confirmation page')
    def i_should_be_on_the_contact_confirmation_page(self):
        """I should be on the contact confirmation page."""
        assert self.driver.title == "Contact Confirmation"
