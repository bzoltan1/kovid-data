#!/usr/bin/python3
import datetime
from datetime import timedelta
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import re
import argparse
from argparse import RawTextHelpFormatter
import sys

chrome_driver_path = '/home/balogh/chromedriver'
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
chrome_options.add_argument('--headless')
chrome_options.add_argument("enable-automation");
chrome_options.add_argument("--window-size=1920,1080");
chrome_options.add_argument("--no-sandbox");
chrome_options.add_argument("--disable-extensions");
chrome_options.add_argument("--dns-prefetch-disable");
chrome_options.add_argument("--disable-gpu");


webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)



epilog_text = "Backup tool for https://koronavirus.gov.hu/elhunytak\n"

parser = argparse.ArgumentParser(description="Backup https://koronavirus.gov.hu/elhunytak",
                                 epilog=epilog_text,
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument('-u',
                    '--url',
                    dest='url',
                    action="store")

options = parser.parse_args()


period = 1000
limit = 60
counter = 0

with webdriver as driver:
    wait = WebDriverWait(driver, 1)
    driver.maximize_window()


    driver.get(options.url)
    driver.implicitly_wait(1)


    forward = True
    i = 0
    page = 1

    while forward:


        table=driver.find_elements_by_xpath('//*[@id="block-system-main"]/div/div[2]/table/tbody/tr')
        for result in table:
            gender = result.find_element_by_xpath('./td[2]').text
            age = result.find_element_by_xpath('./td[3]').text
            comment = result.find_element_by_xpath('./td[4]').text
            i += 1
            if not i % period:
#                print("Above %d -> %s" % (limit, "{:.2%}".format(counter/period)))
#                print("%s" % ("{:.2}".format(counter/period)))
                counter = 0

            if (int(age) > limit):
                counter += 1
          #  print("%s" % (comment))

            print("%d,%s,%s,%s" % (i, age, gender, comment))
        try:
            next_table = driver.find_element_by_link_text("következő ›")
            next_table.click()
        except WebDriverException:
            sys.exit(0)
        page += 1
    driver.close()

