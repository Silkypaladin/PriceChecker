import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import driver_options as opt
from selenium.webdriver.common.keys import Keys

DRIVER = "C:\\PriceChecker\\chromedriver"
TARGET_URL = "https://www.x-kom.pl"

chosen_item = ""
price_range = []


options = opt.get_options()
#opt.set_headless_mode(options)
opt.set_incognito_mode(options)

browser = webdriver.Chrome(executable_path=DRIVER, options=options)
browser.get(TARGET_URL)

search_bar = WebDriverWait(browser, 120, 1).until(
                expect.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Czego szukasz?']")))
search_bar.send_keys("test")