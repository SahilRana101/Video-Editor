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


def virtual_human(key, element):
    for j in key:
        element.send_keys(j)
        time.sleep(float("{:.2f}".format(random.uniform(0.1, 0.4))))


op = webdriver.ChromeOptions()
op.add_argument('--disable-dev-shm-usage')
op.add_argument('--disable-gpu')
op.add_argument("--disable-infobars")
op.add_argument("--log-level=3")
op.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=op)

f = open("urls.txt", "r")
urls = f.readlines()
yo = int(urls.pop(-1))
for url in urls:
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
    time.sleep(2)
    for i in range(yo):
        driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
        time.sleep(float("{:.2f}".format(random.uniform(0.1, 0.4))))
