from selenium import webdriver


def get_options():
    return webdriver.ChromeOptions()

def set_headless_mode(options):
    options.add_argument("--headless")

def set_incognito_mode(options):
    options.add_argument("--incognito")

