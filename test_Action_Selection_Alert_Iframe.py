import time
import logging
from telnetlib import EC
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrom_driver_path = "C:/Users/debor/Downloads/chromedriver_win32/chromedriver.exe"


def test_drag_drop():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.get('https://demo.guru99.com/test/drag_drop.html')
    driver.maximize_window()
    mylogger.info("test for drag drop")
    block_button = driver.find_element(By.CLASS_NAME, "block13 ")
    shopping_card = driver.find_element(By.ID, "shoppingCart1")
    button_bank = driver.find_element(By.ID, "credit2")
    button_5000 = block_button.find_element(By.CLASS_NAME, "button")
    button_c = driver.find_element(By.ID, "credit1")
    drop2 = shopping_card.find_element(By.CLASS_NAME, "ui-widget-content")
    drop1 = driver.find_element(By.ID, "shoppingCart4")
    drop3 = driver.find_element(By.ID, "shoppingCart3").find_element(By.ID, "loan")
    drop4 = driver.find_element(By.ID, "amt8")
    result_table = driver.find_element(By.CLASS_NAME, "table4_result")
    result_button = result_table.find_element(By.CLASS_NAME, "button")
    action = ActionChains(driver)
    action.drag_and_drop(button_5000, drop1).perform()
    action.drag_and_drop(button_bank, drop2).perform()
    action.drag_and_drop(button_5000, drop4).perform()
    action.drag_and_drop(button_c, drop3).perform()
    result_button.click()
    v_a = (drop1.text[7::], drop2.text, drop4.text, drop3.text)
    e_r = ("5000", "BANK", "5000", "SALES")
    assert v_a == e_r


def test_iframe():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.get('http://automationpractice.com/index.php')
    driver.set_window_size(800, 800)
    mylogger.info("test for ifram")
    wait_driver = WebDriverWait(driver, 15)
    container = driver.find_element(By.CLASS_NAME, "product-container")
    container.find_element(By.CLASS_NAME, 'icon-eye-open').click()
    wait_driver.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "fancybox-iframe")))
    time.sleep(5)
    add_to_card_btn = driver.find_element(By.ID, "add_to_card")
    add_to_card_btn.click()
    time.sleep(5)


def test_alerts():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.get('http://the-internet.herokuapp.com/javascript_alerts')
    driver.maximize_window()
    mylogger.info("test for alerts")
    scripts = ("jsAlert()", "jsConfirm()", "jsPrompt()")
    result = driver.find_element(By.ID, "result")
    result_list = list()
    for script in scripts:
        driver.execute_script(script)
        alert = driver.switch_to.alert
        if 'prompt' in alert.text:
            alert.send_keys("JAVA")
        alert.accept()
        result_list.append(result.text)
        time.sleep(3)

    assert result_list[0] == "You successfully clicked an alert"
    assert result_list[1] == "You clicked: Ok"
    assert result_list[2] == "You entered: JAVA"


def test_selection_register():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.get('https://demo.guru99.com/test/newtours/register.php')
    driver.maximize_window()
    mylogger.info("test for selection register")
    driver.find_element(By.NAME, "firstName").send_keys("Deborah")
    driver.find_element(By.NAME, "lastName").send_keys("Fellous")
    driver.find_element(By.NAME, "phone").send_keys("0587088398")
    driver.find_element(By.NAME, "userName").send_keys("deborah770@gmail.com")
    driver.find_element(By.NAME, "address1").send_keys("bran 45")
    driver.find_element(By.NAME, "city").send_keys("jerusalem")
    driver.find_element(By.NAME, "state").send_keys("bbb")
    driver.find_element(By.NAME, "postalCode").send_keys("123456")
    select_country = driver.find_element(By.NAME, "country")
    select = Select(select_country)
    select.select_by_value("ISRAEL")
    driver.find_element(By.NAME, "email").send_keys("deborah770@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123456")
    confirm_password = driver.find_element(By.NAME, "confirmPassword")
    confirm_password.send_keys("123456")
    confirm_password.send_keys(Keys.ENTER)
    time.sleep(2)
    assert driver.find_element(By.CSS_SELECTOR, "img[src='images/mast_register.gif']")
