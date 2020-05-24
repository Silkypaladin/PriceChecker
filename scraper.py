from selenium import webdriver
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import driver_options as opt
from selenium.webdriver.common.keys import Keys
import time
import math
import json
from item import Item
import pandas as pd

DRIVER = ".\\chromedriver"
TARGET_URL = "https://www.x-kom.pl"

chosen_item = ""
price_range = []
fetched_items = []
PAGES_TO_SEARCH = 0
SLEEP_TIME = 0.5

def is_number(num):
        try:
                float(num)
                return True
        except ValueError:
                return False
        


def get_users_input():
        global chosen_item, price_range
        price = ""
        print("Welcome to our price checker. What are you looking for?")
        print("What should i search for? Give a name, eg. 'Monitor 27'.")
        chosen_item = input(">")
        while chosen_item == "":
                print("Please, enter valid item name.")
                chosen_item = input(">")
        print("Now, type in lower bound price. You can type in '0' to make scraper ignore the lower bound.")
        price = input(">")
        while not is_number(price):
                print("Please, enter a valid number.")
                price = input(">")
        price_range.append(float(price))
        print("Now, type in upper bound price. You can type in '0' to make scraper ignore the upper bound.")
        price = input(">")
        while not is_number(price):
                print("Please, enter a valid number.")
                price = input(">")
        price_range.append(float(price))

def format_item_data(item, link):
        fields = item.split("\n")
        l = len(fields)
        #return Item(fields[0], fields[1:l-1],fields[l-1], link)
        if fields[0] =="Polecamy":
                fields=fields[1:]
                l-=1
        return {
                "Name": fields[0],
                "Parameters": fields[1:l-1],
                "Price": fields[l-1],
                "Link": link
        }


def perform_search():
        global PAGES_TO_SEARCH, fetched_items, SLEEP_TIME
        link = ""
        options = opt.get_options()
        #opt.set_headless_mode(options)
        opt.set_incognito_mode(options)
        opt.set_fullscreen(options)
        opt.set_ignore_certificate_error(options)

        browser = webdriver.Chrome(executable_path=DRIVER, options=options)
        browser.get(TARGET_URL)

        search_bar = WebDriverWait(browser, 30, 1).until(expect.visibility_of_element_located((By.XPATH, "//input[@placeholder='Czego szukasz?']")))
        search_bar.send_keys(chosen_item)
        search_bar.send_keys(Keys.ENTER)
        pages = WebDriverWait(browser, 30, 1).until(expect.visibility_of_element_located((By.XPATH, "//input[@class='sc-11oikyw-1 hFPCZt sc-1s2eiz4-0 dySqGZ']")))
        pages_num = int(pages.get_attribute('max'))
        if pages_num == 0:
                browser.close()
                print("No results to analyze. Try running the script again and check your input.")
                return
        if pages_num < 8:
                PAGES_TO_SEARCH = pages_num
        elif pages_num <= 12 and pages_num > 8:
                PAGES_TO_SEARCH = math.floor(pages_num/2)
        elif pages_num > 12 and pages_num < 30:
                PAGES_TO_SEARCH = math.floor(pages_num/3)
        else:
                PAGES_TO_SEARCH = math.floor(pages_num*0.15)
        page_count = 1
        for i in range(0, PAGES_TO_SEARCH+1):
                elems = WebDriverWait(browser, 30, 1).until(expect.visibility_of_all_elements_located((By.XPATH, "//*[@class='sc-162ysh3-1 esXNpw sc-bwzfXH dXCVXY']"))) 
                for e in elems:
                        try:
                                link = WebDriverWait(e, 30, 1).until(expect.visibility_of_element_located((By.XPATH, ".//a"))).get_attribute('href') 
                        except:
                                link = "Not fetched."
                        fetched_items.append(format_item_data(e.text, link))
                page_count+=1
                btn_next = WebDriverWait(browser, 30, 1).until(expect.visibility_of_element_located(
                        (By.XPATH, f"//a[contains(@href,'/szukaj?page={page_count}')]")))
                btn_next.click()
                time.sleep(SLEEP_TIME)
        print("Items fetched. Performing caculations now.")
        browser.quit()

def analyze_results():
        global fetched_items, price_range
        results = []
        # price format: '4 377,44 zł'"
        pr = ""
        for item in fetched_items:
                pr = item["Price"] 
                # Remove the currency
                pr = pr[:len(pr)-3]
                pr = pr.replace(",", ".")
                pr = pr.replace(" ", "")
                pr = float(pr)
                if price_range[0] != 0 and price_range[1] != 0:
                        if pr >= price_range[0] and pr <= price_range[1]:
                                results.append(item)
                elif price_range[0] == 0 and price_range[1] == 0:
                        results.append(item)
                elif price_range[0] == 0 and price_range[1] != 0:
                        if pr <= price_range[1]:
                                results.append(item)
                else:
                        if pr >= price_range[0]:
                                results.append(item)
        return results

def results_into_json(results):
        with open("items.json", "w+") as file:
                json.dump(results, file, indent=3)
        print("Finished calculating. Check 'items.json' file to view the results.")

def generate_csv():
        print("Do you want to generate a csv file? Type in 'yes' or 'no'")
        inp = input(">")
        while inp != 'yes' and inp != 'no':
                print("Please type 'yes' or 'no'")
                inp = input(">")
        if inp == 'yes':
                df = pd.read_json(r'.\\items.json')
                df.to_excel(r'.\\items.csv', mode="w+", index=None, header=True)

if __name__ == "__main__":
        get_users_input()
        perform_search()
        res = analyze_results()
        results_into_json(res)
        generate_csv()
