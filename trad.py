import re
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

example = ""
driver = webdriver.Firefox()
driver.get(
    "https://translate.google.fr/?hl=fr#view=home&op=translate&sl=zh-CN&tl=fr&text=%E9%87%8F%E5%8C%96%E5%BA%A6%E9%87%8F")
source = driver.find_element_by_id("source")
listentab = driver.find_elements_by_class_name("jfk-button-img")
listen=listentab[2]
driver.minimize_window()
while example != 'quit':
    try:
        example = input("new trad\n")
    except:
        print("invalid")
    example = re.sub('\(.*?\)', '', example, flags=re.DOTALL)
    source.clear()
    source.send_keys(example)
    source.click()
    time.sleep(1)
    listen.click()
    time.sleep(3)
driver.quit()
