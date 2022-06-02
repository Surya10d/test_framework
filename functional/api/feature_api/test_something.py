# coding=utf-8
"""Proof of concept that my framework works feature tests."""

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
from tests.functional import feature_file_path

@scenario(feature_file_path+'myfeature.feature', 'My first test')
def test_my_first_test():
    """My first test."""


@given('I navigate to the zoo website')
def i_navigate_to_the_zoo_website():
    """I navigate to the zoo website."""


@when('I click on the check button')
def i_click_on_the_check_button():
    """I click on the check button."""


@then('I check to see that no animals are available')
def i_check_to_see_that_no_animals_are_available():
    """I check to see that no animals are available."""

