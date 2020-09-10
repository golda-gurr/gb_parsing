from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongobase = client.mvideo
collection = mongobase['hits']

chrome_options = Options()
chrome_options.add_argument("--headless")  # Режим без интерфейса
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru')

assert 'М.Видео' in driver.title

try:
    hits = driver.find_element_by_xpath(
        '//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]'
    )
except exceptions.NoSuchElementException:
    print('Hits has not been found')

while True:
    try:
        next_button = WebDriverWait(hits, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')
            )
        )

        driver.execute_script("$(arguments[0]).click();", next_button)
    except exceptions.TimeoutException:
        print('Сбор данных окончен')
        break

goods = hits.find_elements_by_css_selector('li.gallery-list-item')

item = {}
for good in goods:
    item['title'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('innerHTML')

    item['good_link'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('href')

    item['price'] = float(
        good.find_element_by_css_selector(
            'div.c-pdp-price__current').get_attribute('innerHTML').replace(
                '&nbsp;', '').replace('¤', ''))

    item['image_link'] = good.find_element_by_css_selector(
        'img[class="lazy product-tile-picture__image"]') \
        .get_attribute('src')

    collection.update_one({'good_link': item['good_link']}, {'$set': item},
                          upsert=True)
driver.quit()
