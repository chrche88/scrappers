import os
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
import os, fnmatch
import tkinter
import tkinter.filedialog as fd

date = datetime.datetime.today().strftime('%Y-%m-%d')

def diff_list(l1, l2):
    """élément dans l2 et pas dans l1"""
    s1 = set(l1)
    s2 = set(l2)
    return s2 - s1


profile = FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
pd.options.mode.chained_assignment = None  # default='warn'
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(firefox_profile=profile)
root = tkinter.Tk()
root.withdraw()  # use to hide tkinter window

# currdir = os.getcwd()
path_to_f = fd.askopenfilename(title='Choisir le fichier à scinder', parent=root,
                           filetypes=(("Template files", "*.csv"), ("All files", "*")))
df = pd.read_csv(path_to_f)

time.sleep(2)
df['ID'] = np.nan
df['Offre'] = np.nan
ids = df['ID']
offres = df['Offre']
liens = df['URL']
col_nom = df["Etablissement"]
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
wait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'https://alleatone.fr/admin/stores')]")))
time.sleep(1)
driver.find_elements_by_xpath("//a[starts-with(@href, 'https://alleatone.fr/admin/stores')]")[0].click()
time.sleep(2)
start_int = 0
bar.show()

print('\n')
print('début traitement \n')
wait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
pagination = driver.find_element_by_class_name("pagination")
list_pagination = pagination.find_elements_by_xpath(".//li")
list_pagination = list_pagination[2:-1]
page_actuelle = 1
nb_pages = len(list_pagination)
last_height = driver.execute_script("return document.body.scrollHeight")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
for element in list_pagination:
    wait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'store_name')))
    ActionChains(driver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
    time.sleep(1)
    # driver.get("https://alleatone.fr/admin/stores?page=" + str(n))
time.sleep(4)
all_tabs = driver.window_handles
main_window = driver.current_window_handle
print('Chargement des onglets\n')
for tab in all_tabs:
    driver.switch_to.window(tab)
    wait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))
for i in range(len(noms)):
    if noms[i] == '':
        print(str(i) + '/' + str(len(noms)) + ':' + noms[i])
    for tab in all_tabs:
        driver.switch_to.window(tab)
        chaine = liens[i]
        m = re.search('//(.+?)[.]alleatone', chaine)
        if True:
            try:

                if m:
                    mot = m.group(1)+'.'
                    selecteur = driver.find_element_by_xpath("//a[contains(@href, '" + mot + "')]")
                    parent = selecteur.find_element_by_xpath("..")
                    parent = parent.find_element_by_xpath("..")
                    row = parent.find_elements_by_xpath(".//td")
                    id_rest = row[0].text
                    #### Récup offre
                    plus_info_bouton = row[7].find_element_by_xpath('.//div')
                    driver.execute_script("arguments[0].scrollIntoView();", plus_info_bouton)
                    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).click(plus_info_bouton).key_up(
                        Keys.CONTROL).key_up(Keys.SHIFT).perform()
                    time.sleep(1)
                    temp_tabs = diff_list(all_tabs, driver.window_handles)
                    temp_tab_handle = temp_tabs.pop()
                    driver.switch_to.window(temp_tab_handle)
                try:
                    wait(driver, 120).until(EC.presence_of_element_located((By.NAME, 'plan_id')))
                    plan_selector = Select(driver.find_element_by_name('plan_id'))
                    plan = plan_selector.first_selected_option.text
                    print(noms[i] + ': ' + id_rest + ' ' + plan)
                    offres.loc[i] = plan
                    ids.loc[i] = id_rest
                    driver.close()
                    break
                except:
                    driver.close()
                    break
            except:
                print()

    bar.update(i / len(noms))
    bar.show()
    print('\n')
df.to_csv('D:\\Users\\chenchr\\Desktop\\Stage\\'+date+'_aeo_stripe_modified2.csv')
for tab in all_tabs:
    driver.switch_to.window(tab)
    driver.close()
