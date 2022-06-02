from selenium.webdriver.common.by import By
from lib.ui.page_objects.base_page import BasePage


class ContactConfirm(BasePage):

    URL = "http://www.thetestroom.com/webapp/"

    contact_link = (By.ID, "contact_link")
    name_field = (By.NAME, "name_field")
    address_field = (By.NAME, "address_field")
    postcode_field = (By.NAME, "postcode_field")
    email_field = (By.NAME, "email_field")
    submit_message = (By.ID, "submit_message")

    def load(self, driver):
        super(ContactConfirm, self).load()

    def click_contact_btn(self):
        self.click(self.contact_link)

    def enter_name_field(self, input_data):
        self.input_text(self.name_field, input_data)

    def enter_address_field(self, input_data):
        self.input_text(self.address_field, input_data)

    def enter_postcode_field(self, input_data):
        self.input_text(self.postcode_field, input_data)

    def enter_email_field(self, input_data):
        self.input_text(self.email_field, input_data)

    def click_submit_message(self):
        self.click(self.submit_message)
