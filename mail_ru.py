from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://mail.ru/')

assert 'Mail.ru' in driver.title

try:
    mail_button = driver.find_element_by_css_selector(
        'div[class="mailbox__body"]'
    )
except exceptions.NoSuchElementException:
    print('Mail login not found')


field_login = driver.find_element_by_xpath(
    "//div[@class='mailbox__login']//input[@id='mailbox:login-input']")
field_login.send_keys('Login')  # Login - нужно указать реальный логин

remember_button = driver.find_element_by_xpath(
    "//input[@id='mailbox:saveauth']")

remember_button.click()

passwd_button = driver.find_element_by_xpath(
    "//input[@class='o-control']")
passwd_button.click()

wait = WebDriverWait(driver, 10)
field_passwd = wait.until(
    EC.presence_of_element_located((By.ID, 'mailbox:password-input')))
field_passwd.send_keys('Password')  # Password - нужно указать реальный пароль
field_passwd.send_keys(Keys.ENTER)

driver.quit()
