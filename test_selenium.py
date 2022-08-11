import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrom_driver_path = "C:/Users/debor/Downloads/chromedriver_win32/chromedriver.exe"


def function(text: str = None, email: str = None, password: str = None) -> bool:
    """
    function that get text, email and password, checking the error type
    :param text: str ERROR TYPE
    :param email: str
    :param password: str
    :return: bool
    """
    if not isinstance(email, str):
        raise TypeError("email must be a string!")
    if not isinstance(password, str):
        raise TypeError("password must be a string!")
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "passwd").send_keys(password)
    driver.find_element(By.CLASS_NAME, "icon-lock").click()
    alert = driver.find_element(By.CLASS_NAME, "alert")
    return text in alert.text


my_email = 'd2@gmail.com'
my_password = 'D123456'
my_account = 'deborah fellous'


def test_empty_email():
    """
    test that check that no email has been entered
    """
    mylogger.info("test no email")
    assert function("An email address required", " ", "12345")


def test_invalid_email():
    """
        test that check that an invalid email was entered
    """
    mylogger.info("test fake email")
    assert function("Invalid email address", "od2@gmail", "12345")


def test_invalid_password():
    """
    test that check that an invalid password was entered
    """
    mylogger.info("test invalid password")
    assert function("Invalid password", "d2@gmail.com", "1234")


def test_unregistered_authentication():
    """
    test that check that an invalid authentication try to login
    """
    mylogger.info("test fake authentication")
    assert function("Authentication failed", "d2@gmail.com", "123456")


def test_empty_password():
    """
    test that check that no password has been entered
    """
    mylogger.info("test no password")
    assert function("Password is required", "d2@gmail.com", "  ")


def test_valid_authentication():
    """
    test that check valid authentication
    """
    mylogger.info("test valid authentication")
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()
    driver.find_element(By.ID, "email").send_keys(my_email)
    driver.find_element(By.ID, "passwd").send_keys(my_password)
    driver.find_element(By.CLASS_NAME, "icon-lock").click()
    name_account = driver.find_element(By.CLASS_NAME, "header_user_info")
    time.sleep(3)
    assert name_account.text == my_account


def test_forgot_password():
    mylogger.info("test for click on forgot password button")
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//a[text()="Forgot your password?"]').click()
    time.sleep(2)
    assert driver.current_url == "http://automationpractice.com/index.php?controller=password"
    driver.close()


def test_buy_dress():
    """
    test that login, search summer categorie, find the cheapest item and buy it
    :return:
    """
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()

    # login to the website
    mylogger.info("test login to the website")
    driver.find_element(By.ID, "email").send_keys(my_email)
    driver.find_element(By.ID, "passwd").send_keys(my_password)
    driver.find_element(By.CLASS_NAME, "icon-lock").click()
    name_account = driver.find_element(By.CLASS_NAME, "header_user_info")
    time.sleep(3)
    assert name_account.text == my_account

    # search "summer"
    mylogger.info("test search 'summer'")
    driver.find_element(By.ID, "search_query_top").send_keys("summer")
    driver.find_element(By.NAME, "submit_search").click()
    time.sleep(1)
    search_result_header = driver.find_element(By.CSS_SELECTOR, "#center_column>h1")
    time.sleep(3)
    assert 'SEARCH  "SUMMER"' in search_result_header.text

    # from the item select the cheapest Item
    product_containers = driver.find_elements(By.CLASS_NAME, "product-container")
    min_price = 1000
    min_product_container = product_containers
    for product_container in product_containers:
        right_block = product_container.find_element(By.CLASS_NAME, "right-block")
        content_price = right_block.find_element(By.CLASS_NAME, "content_price")
        price = content_price.find_element(By.CLASS_NAME, "price").text
        price_num = float(price[1:len(price)])
        if min_price > price_num:
            min_price = price_num
            min_product_container = product_container
    right_block = min_product_container.find_element(By.CLASS_NAME, "right-block")
    product_name = right_block.find_element(By.CLASS_NAME, "product-name")
    product_name.click()
    time.sleep(3)

    # complete the preaches to the end
    mylogger.info("test complete the preaches to the end")
    driver.find_element(By.CSS_SELECTOR, "button.exclusive").click()
    time.sleep(2)

    # 1  button_container = driver.find_element(By.CLASS_NAME, "button-container")
    # button_container.find_element(By.CLASS_NAME, "btn").click()

    # 2 button_container.find_element(By.CSS_SELECTOR, "a[title='Proceed to checkout']").click()

    driver.find_element(By.CSS_SELECTOR,
                        'a[href="http://automationpractice.com/index.php?controller=order"]').click()

    # driver.find_element(By.CSS_SELECTOR, "a.button-medium").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,
                        'a[href="http://automationpractice.com/index.php?controller=order&step=1"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[name=processAddress]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[type=checkbox]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[name=processCarrier]').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "bankwire").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.button-medium").click()
    time.sleep(2)
    comp = driver.find_element(By.CLASS_NAME, "cheque-indent").find_element(By.CLASS_NAME, "dark")
    assert "Your order on My Store is complete." in comp.text
    driver.close()
