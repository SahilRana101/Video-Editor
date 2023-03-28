import os
import time
import random
import spintax
import requests
import config
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

def stop(n):
    time.sleep(n)


op = webdriver.ChromeOptions()
# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# op.add_argument('--headless')
op.add_argument('--disable-dev-shm-usage')
# op.add_argument('--no-sandbox')
op.add_argument('--disable-gpu')
# op.add_argument("--window-size=1920,1080")
op.add_argument("--disable-infobars")
op.add_argument("--log-level=3")
op.add_argument("--disable-extensions")
# op.add_argument('--proxy-server=%s' % PROXY)
# op.add_argument("--proxy-bypass-list=*")
driver = webdriver.Chrome(options=op, executable_path=CM().install())

driver.get("https://www.youtube.com/watch?v=GVsUOuSjvcg")
time.sleep(5)
driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
time.sleep(2)
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    print(1)
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        print(3)
        break
    last_height = new_height
    print(1)
print(2)
time.sleep(2)
