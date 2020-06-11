import os
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import progress

profile = FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
pd.options.mode.chained_assignment = None  # default='warn'
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(firefox_profile=profile)

df = pd.read_csv('D:\\Users\\chenchr\\Desktop\\Stage\\aeo_stripe_modified.csv')
time.sleep(2)
ids = df['ID']
dates_de_reception = df['Date de reception']
offres = df['OFFRE']
liens = df['URL webapp']
col_nom = df["Nom sur site All Eat One"]
liens = np.array(liens)
noms = np.array(col_nom)

bar = progress.ProgressBar("[{progress}] {percentage:.2f}% ({minutes}:{seconds})", width=30)

print('Connexion...')
driver.get('https://alleatone.fr/admin/stores')
driver.find_element_by_id('email').send_keys('admin@fyre.fr')
driver.find_element_by_id('password').send_keys('Fyre@ll3@t12020')
driver.find_element_by_id('password').send_keys(Keys.ENTER)
wait(driver, 15).until(EC.presence_of_element_located((By.NAME, "user_role_id")))
driver.find_element_by_name('user_role_id')
select = Select(driver.find_element_by_name('user_role_id'))
select.select_by_visible_text('Fyre Admin')
driver.find_element_by_id('password').send_keys(Keys.ENTER)
wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'https://alleatone.fr/admin/stores')]")))
driver.find_elements_by_xpath("//a[starts-with(@href, 'https://alleatone.fr/admin/stores')]")[0].click()
time.sleep(2)
start_int = 0
bar.show()

print('\n')
print('début traitement \n')
input()
for i in range(len(noms)):
    print(str(i)+':')
    try:
        if noms[i]!=np.nan:
            print("Recherche de " + noms[i])
            wait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'store_name')))
            driver.find_element_by_name('store_name').clear()
            driver.find_element_by_name('store_name').send_keys(noms[i])
            driver.find_element_by_name('store_name').send_keys(Keys.ENTER)
            time.sleep(2)
            wait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'summary')))
            ### si il y au moins un résultat ####
            if driver.find_element_by_class_name('summary').text != "Showing 0 entries.":
                print('récupération ID et date de création \n')
                selecteur = driver.find_element_by_xpath("//a[contains(@href, '" + liens[i] + "')]")
                parent = selecteur.find_element_by_xpath("..")
                parent = parent.find_element_by_xpath("..")
                row = parent.find_elements_by_xpath(".//td")
                id_rest = row[0].text
                date_creation = row[3].text
                print('récupération offre\n')
                ####
                plus_info_bouton = row[7].find_element_by_xpath('.//div')
                plus_info_bouton.click()
                wait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'plan_id')))
                plan_selector = Select(driver.find_element_by_name('plan_id'))
                plan = plan_selector.first_selected_option.text
                print(noms[i]+': '+id_rest + ' ' + date_creation+' '+plan)
                ids.loc[i]=id_rest
                dates_de_reception.loc[i]=date_creation
                offres.loc[i]=plan
                driver.execute_script("window.history.go(-1)")
            else:
                print("cette recherche ne comporte aucun résultat\n")
        else:
            print("cette ligne n'a pas de nom\n")
    except:
        print('Probleme avec cet element, skipping ... \n')
        driver.get('https://alleatone.fr/admin/stores')
    bar.update(i / len(noms))
    bar.show()
    print('\n')
df.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\aeo_stripe_modified2.csv')
input()
driver.close()
