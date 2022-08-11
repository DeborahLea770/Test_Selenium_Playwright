import re
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

my_email = 'd2@gmail.com'
my_password = 'D123456'
my_account = 'deborah fellous'


def function(text: str = None, email: str = None, password: str = None) -> bool:
    if not isinstance(email, str):
        raise TypeError("email must be a string!")
    if not isinstance(password, str):
        raise TypeError("password must be a string!")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://automationpractice.com/index.php")
        page.locator("a.login").click()
        time.sleep(1)
        page.locator("input#email").fill(email)
        page.locator("input#passwd").fill(password)
        page.locator("#SubmitLogin").click()
        time.sleep(2)
        return text in page.locator('body').inner_html()


def test_empty_email():
    """
    test that check that no email has been entered
    """
    mylogger.info("test for empty email")
    assert function("An email address required", " ", "12345")


def test_invalid_email():
    """
        test that check that an invalid email was entered
    """
    mylogger.info("test for fake email")
    assert function("Invalid email address", "od2@gmail", "12345")


def test_invalid_password():
    """
    test that check that an invalid password was entered
    """
    mylogger.info("test for invalid password")
    assert function("Invalid password", "d2@gmail.com", "1234")


def test_unregistered_authentication():
    """
    test that check that an invalid authentication try to login
    """
    mylogger.info("test for fake authentication")
    assert function("Authentication failed", "d2@gmail.com", "123456")


def test_empty_password():
    """
    test that check that no password has been entered
    """
    mylogger.info("test for empty password")
    assert function("Password is required", "d2@gmail.com", "  ")


def test_valid_authentication():
    """
        test that check valid authentication
        """
    mylogger.info("test for valid authentication")
    assert function("Welcome to your account", "d2@gmail.com", "123456")


def test_forgot_password():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://automationpractice.com/index.php")
        page.locator("a.login").click()
        time.sleep(2)
        page.locator('text=Forgot your password?').click()
        time.sleep(2)
        assert page.url == "http://automationpractice.com/index.php?controller=password"


def test_buy_dress():
    """
        test that login, search summer categorie, find the cheapest item and buy it
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://automationpractice.com/index.php")
        page.locator("a.login").click()
        time.sleep(1)
        page.locator("input#email").fill(my_email)
        page.locator("input#passwd").fill(my_password)
        page.locator("#SubmitLogin").click()
        time.sleep(1)
        assert "Welcome to your account" in page.locator("body").inner_html()
        page.locator('#search_query_top').fill('summer')
        page.locator('button.button-search').click()
        header = page.locator("h1.page-heading:has-text('SUMMER')")
        assert "summer" in header.inner_html()
        products = page.locator('ul.product_list li')
        prices = page.locator('ul.product_list li .product-price')
        time.sleep(1)
        prices_list = []
        for price in prices.all_inner_texts():
            prices_list.append(re.sub('[^\d\.]', "", price))
        cheapest = products.locator(f".product-container:has-text('${(min(prices_list))}')")
        cheapest.hover()
        page.wait_for_timeout(3000)
        cheapest.locator("text='Add to cart'").click()
        page.locator("text='Proceed to checkout'").click()
        time.sleep(1)
        page.locator("#center_column >> text='Proceed to checkout'").click()
        page.locator("button >> text='Proceed to checkout'").click()
        page.locator("input#cgv").click()
        page.locator("button >> text='Proceed to checkout'").click()
        total_price = page.locator("#total_product").inner_text()
        assert min(prices_list) == re.sub('[^\d\.]', "", total_price)
        page.locator("text='Pay by bank wire'").click()
        page.locator("button >> text='I confirm my order'").click()
        time.sleep(1)
        assert "Your order on My Store is complete" in page.locator('body').inner_html()
