from selenium import webdriver
import time
import re
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import progress
import datetime

profile = FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
pd.options.mode.chained_assignment = None  # default='warn'
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(firefox_profile=profile)

df = pd.read_csv('D:\\Users\\chenchr\\Desktop\\Stage\\mailsboulangers.csv')

df['Mails'] = np.nan
mails = df['Mails']
prefixes = df['Nom de la boulangerie']

prefixes = np.array(prefixes)

liens = ['http://' + x + '.maboulangerie.com' for x in prefixes]

# accès aux sites

for i in range(len(liens)):
    driver.get(liens[i])
    try:
        wait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]")))
        selecteur = driver.find_element_by_xpath("//a[starts-with(@href, 'mailto:')]")
        mails.loc[i] = selecteur.text
        print(selecteur.text)
    except:
        print('\n site HS/long à charger \n')
        print('Resetting .....\n')
        driver.close()
        driver = webdriver.Firefox(firefox_profile=profile)
        time.sleep(2)
        print('Reset Successfull, restarting Browser.')
        i = i - 1
df.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\finalmailsboulangers.csv')