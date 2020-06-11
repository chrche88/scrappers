import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "D:/Users/chenchr/Downloads",
         "directory_upgrade": True,
         "profile.default_content_settings.popups": 0,
         "safebrowsing_for_trusted_sources_enabled": False,
         "safebrowsing.enabled": False
         }
# options.add_argument('prefs', prefs)
dirpath = os.path.realpath("D:\\Users\chenchr\Desktop\\attest")
prefs = {"download.default_directory": dirpath}
# options.add_argument("download.default_directory=D:/Users/chenchr/Desktop/attest")
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)

choix = input("Veuillez choisir un motif de sortie:"
              "\n0: Déplacements entre le domicile et le lieu d’exercice de l’activité professionnelle, lorsqu'ils sont "
              "indispensables à l'exercice d’activités ne pouvant être organisées sous forme de télétravail ou "
              "déplacements professionnels ne pouvant être différés. "
              "\n1: Déplacements pour effectuer des achats de fournitures nécessaires à l’activité professionnelle et "
              "des achats de première nécessité dans des établissements dont les activités demeurent autorisées ("
              "liste des commerces et établissements qui restent ouverts). "
              "\n2: Consultations et soins ne pouvant être assurés à distance et ne pouvant être différés ; "
              "consultations et soins des patients atteints d'une affection de longue durée. "
              "\n3: Déplacements pour motif familial impérieux, pour l’assistance aux personnes vulnérables ou la garde "
              "d’enfants. "
              "\n4: Déplacements brefs, dans la limite d'une heure quotidienne et dans un rayon maximal d'un kilomètre "
              "autour du domicile, liés soit à l'activité physique individuelle des personnes, à l'exclusion de toute "
              "pratique sportive collective et de toute proximité avec d'autres personnes, soit à la promenade avec "
              "les seules personnes regroupées dans un même domicile, soit aux besoins des animaux de compagnie. "
              "\n5: Convocation judiciaire ou administrative."
              "\n6: Participation à des missions d’intérêt général sur demande de l’autorité administrative."
              "\n")


# fxProfile: FirefoxProfile = FirefoxProfile()
# fxProfile.set_preference("browser.download.folderList", 2)
# fxProfile.set_preference("browser.download.manager.showWhenStarting", False)
# fxProfile.set_preference("browser.download.dir", "D:/Users/chenchr/Desktop/attest")
# fxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/pdf")
class Person:
    def __init__(self):
        self.nom = ""
        self.prenom = ""
        self.birthdate = ""
        self.birthplace = ""
        self.adress = ""
        self.ville = ""
        self.codep = ""


list_person = []
nb_person = 3
for i in range(nb_person):
    list_person.append(Person())

list_person[0].nom = "Chen"
list_person[0].prenom = "Haifen"
list_person[0].birthdate = "04/02/1971"
list_person[0].birthplace = "CHINE"
list_person[0].adress = "44 Bis Rue Jean Charcot"
list_person[0].ville = "Aulnay-sous-bois"
list_person[0].codep = "93600"

list_person[1].nom = "Chen"
list_person[1].prenom = "Jinrong"
list_person[1].birthdate = "02/07/1961"
list_person[1].birthplace = "CHINE"
list_person[1].adress = "44 Bis Rue Jean Charcot"
list_person[1].ville = "Aulnay-sous-bois"
list_person[1].codep = "93600"

list_person[2].nom = "Chen"
list_person[2].prenom = "Christian"
list_person[2].birthdate = "06/01/1996"
list_person[2].birthplace = "Montreuil"
list_person[2].adress = "44 Bis Rue Jean Charcot"
list_person[2].ville = "Aulnay-sous-bois"
list_person[2].codep = "93600"
driver.get("https://media.interieur.gouv.fr/deplacement-covid-19/")
dprenom = driver.find_element_by_id('field-firstname')
dnom = driver.find_element_by_id('field-lastname')
dbirthdate = driver.find_element_by_id('field-birthday')
dbirthplace = driver.find_element_by_id('field-lieunaissance')
dadresse = driver.find_element_by_id('field-address')
dville = driver.find_element_by_id('field-town')
dcodep = driver.find_element_by_id('field-zipcode')
liste_choix = driver.find_elements_by_class_name("form-check")
ddate = driver.find_element_by_id('field-heuresortie')
button_dl = driver.find_element_by_class_name('btn.btn-primary.btn-attestation')
# for i in range(len(list_person)):
for i in range(len(list_person)):
    wait(driver, 15).until(EC.presence_of_element_located((By.ID, "field-firstname")))
    time.sleep(1)
    try:
        maj = driver.find_element_by_id("reload-btn")
        maj.click()
        print("Mise à jour de la page")
        dprenom = driver.find_element_by_id('field-firstname')
        dnom = driver.find_element_by_id('field-lastname')
        dbirthdate = driver.find_element_by_id('field-birthday')
        dbirthplace = driver.find_element_by_id('field-lieunaissance')
        dadresse = driver.find_element_by_id('field-address')
        dville = driver.find_element_by_id('field-town')
        dcodep = driver.find_element_by_id('field-zipcode')
        liste_choix = driver.find_elements_by_class_name("form-check")
        ddate = driver.find_element_by_id('field-heuresortie')
        button_dl = driver.find_element_by_class_name('btn.btn-primary.btn-attestation')
    except:
        print("Pas de mise à jour nécessaire")
    print("--- Génération pour " + list_person[i].prenom + "---")
    time.sleep(2)
    dprenom.clear()
    dnom.clear()
    dbirthplace.clear()
    dbirthdate.clear()
    dville.clear()
    dadresse.clear()
    dcodep.clear()

    dprenom.send_keys(list_person[i].prenom)
    dnom.send_keys(list_person[i].nom)
    dbirthdate.send_keys(list_person[i].birthdate)
    dbirthplace.send_keys(list_person[i].birthplace)
    dville.send_keys(list_person[i].ville)
    dadresse.send_keys(list_person[i].adress)
    dcodep.send_keys(list_person[i].codep)
    if i == 0:
        liste_choix[int(choix)].click()
    button_dl.click()
    time.sleep(3)
path = "D:/Users/chenchr/Downloads"
wechat = "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
path = os.path.realpath(path)
path2 = os.path.realpath(wechat)
os.startfile(dirpath)
print('Fermeture....')
driver.quit()
print('Terminée')
quit()
