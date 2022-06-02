# import pytest
# from selenium.webdriver import Chrome, ChromeOptions
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# @pytest.fixture(autouse=True, scope='module')
# def setup(request):
#     chrome_options = ChromeOptions()
#     driver = Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
#
#     def fin():
#         driver.quit()
#         request.addfinalizer(fin)
