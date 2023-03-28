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

PROXY = "3.88.169.225:80"


def youtube_login(email, password):

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
    driver = webdriver.Chrome(options=op)
    driver.execute_script("document.body.style.zoom='80%'")
    driver.get('https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https'
               '%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dht'
               'tps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    print("=================================================="
          "===========================================================")
    print("Google Login")

    # finding email field and putting our email on it
    email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
    email_field.send_keys(email)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(5)
    print("email - done")

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)
    print("password - done")
    WebDriverWait(driver, 200).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver


# WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//yt-formatted-string[@class='style-s"
#                                                                                  "cope ytd-comment-renderer' and @id='c"
#                                                                                  "ontent-text'][@slot='content']")))[0]\
#     .find_element_by_id("")
email = config.email
password = config.password

driver = youtube_login(email, password)
driver.get("https://www.youtube.com/watch?v=AgFQ6EhD3Qc")
time.sleep(5)
driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
time.sleep(2)
main_comments = driver.find_elements_by_css_selector('#contents #comment')
op = 1
comment_box = driver.find_elements_by_xpath('//*[@id="contenteditable-root"]')
replies = driver.find_elements_by_xpath('//*[@id="reply-button-end"]')
for reply in replies:
    mc = main_comments.pop(0)
    reply.click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, window.scrollY + 150)")
    time.sleep(1)
    # comment_box = driver.find_element_by_css_selector('#contenteditable-textarea')
    # comment_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#input-container')))
    ActionChains(driver).move_to_element(comment_box[op-1]).click(comment_box[op-1]).perform()
    add_comment_onit = driver.find_element_by_xpath('//*[@id="contenteditable-root"]')
    add_comment_onit.send_keys("Nicely done")
    time.sleep(1)
    # driver.find_element_by_css_selector('#submit-button').click()
    print(op)
    op += 1