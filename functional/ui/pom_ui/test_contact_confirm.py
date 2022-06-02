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

    @pytest.fixture()
    def background(self, driver):
        self.contact_confirm = ContactConfirm(driver)
        self.contact_confirm.load(driver)
        self.driver = driver

    @pytest.mark.usefixtures("background")
    def test_contact_confirm(self):
        self.contact_confirm.click_contact_btn()
        self.contact_confirm.enter_name_field("Chris")
        self.contact_confirm.enter_address_field("Galaxy")
        self.contact_confirm.enter_postcode_field("P2D F3F")
        self.contact_confirm.enter_email_field("light@star.com")
        self.contact_confirm.click_submit_message()
        assert self.contact_confirm.get_title() == "Contact Confirmation"
