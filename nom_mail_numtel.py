import os
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import progress
profile = FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
pd.options.mode.chained_assignment = None  # default='warn'
#options = webdriver.ChromeOptions()
#driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(firefox_profile=profile)

df = pd.read_csv('D:\\Users\\chenchr\\Desktop\\Stage\\aeo_stripe.csv')
#print(df)
liens = df['URL webapp']
col_mails = df['e-mail contact']
col_num_tel = df['téléphone']
col_nom = df["Nom sur site All Eat One"]
liens=np.array(liens)

bar = progress.ProgressBar("[{progress}] {percentage:.2f}% ({minutes}:{seconds})", width=30)

start_int= int(input('\n Choisir index de départ : \n valider par Entrée \n'))
bar.show()
for i in range(start_int,len(liens)):
    driver.get(liens[i])
    try:
        wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'tel')]")))
        tel=driver.find_elements_by_xpath("//a[starts-with(@href, 'tel')]")
        tel=tel[0].text
        col_num_tel.loc[i]=tel

        wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto')]")))
        mail=driver.find_elements_by_xpath("//a[starts-with(@href,'mailto')]")
        mail=mail[0].text
        col_mails.loc[i]=mail

        wait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME,"ttl-holder")))
        nom = driver.find_element_by_class_name("ttl-holder")
        nom = nom.find_element_by_xpath(".//h2")
        nom=nom.parent.title
        col_nom.loc[i]=nom
        print('\n'+nom+' '+mail+' '+tel+' ajouté \n')

    except:
        print('\n site HS/long à charger \n')
        print('Resetting .....\n')
        driver.close()
        driver = webdriver.Firefox(firefox_profile=profile)
        time.sleep(2)
        print('Reset Successfull, restarting Browser.')
        i=i-1
    bar.update(i/len(liens))
    bar.show()

#col_to[2]='b'
print(df['e-mail contact'])
df.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\aeo_stripe_modified.csv')

driver.close()