from selenium import webdriver


def get_options():
    return webdriver.ChromeOptions()

def set_headless_mode(options):
    options.add_argument("headless")

def set_incognito_mode(options):
    options.add_argument("--incognito")

def set_fullscreen(options):
    options.add_argument("--start-maximized")

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


