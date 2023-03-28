import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

video_url = 'https://www.youtube.com/watch?v=AgFQ6EhD3Qc'
driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
driver.get(video_url)
time.sleep(2)
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)
elem = driver.find_element_by_xpath(".//div[@class='style-scope ytd-comments-header-renderer' and @id='title']//following-sibling::yt-formatted-string[contains(@class,'ytd-comments-header-renderer')]/span[1]")
driver.execute_script("arguments[0].scrollIntoView();", elem)
print(elem.text)