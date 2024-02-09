from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import json
from pymongo import MongoClient


def getUrl(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        return driver
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ouverture de l'URL : {e}")
        return None

def clickerButtonParId(stringId,driver):
      button = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, f'.{stringId}')))
      button.click()

def clickerButtonParClass(StringClass, driver):
    button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, f'.{StringClass}')))
    button.click()
    
def clickerButtonByPath(path, driver):
    menu_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH,  f'.{path}')))
    menu_button.click()
    
def clickerButtonParExpression(expr, driver):
    try:
        button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,f'{expr}')))
        button.click()
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")

def navigationLienByExpression(expr,driver):
    try:
        div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'{expr}'))
        )
        lienItem = div.find_element(By.CSS_SELECTOR, 'a:nth-child(2)')
        lienUrl = lienItem.get_attribute('href')
        driver.get(lienUrl)
        return driver
    except Exception as e:
        print(f"Une erreur s'est produite lors de la navigation vers le lien : {e}")
    
def searchInput(expr, driver, texte):
    try:
        inputText = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'{expr}')))
        inputText=driver.find_element(By.CSS_SELECTOR,f'{expr}')
        inputText.send_keys(texte)
        inputText.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def recuperationLiens(expr, driver):
    try:
        urls=[]
        divs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'{expr}'))
        )
        for div in divs:
            liens = div.find_elements(By.CSS_SELECTOR, 'a')
            for lien in liens:
                lienUrl = lien.get_attribute('href')
                urls.append(lienUrl)
        return urls
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        
def recuperationLienComment(expr, driver):
    try:
        liens= WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'{expr}'))
        )
        if liens:
            lienUrl = liens[0].get_attribute('href')
            return lienUrl
        else:
            print("Aucun lien trouvé.")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    
def sauvegardeInfosToCsv(meteo_infos, chemin_fichier_csv):
    try:
        df = pd.DataFrame([vars(info) for info in meteo_infos])
        df.to_csv(chemin_fichier_csv, index=False)
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'enregistrement des informations dans le fichier CSV : {e}")


def sauvegardeInfosToJson(meteo_infos, chemin_fichier_json):
    try:
        with open(chemin_fichier_json, 'w') as f:
            json.dump(meteo_infos, f, indent=4)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde des données dans le fichier JSON : {e}")

def sauvegardeBD(chemin_fichier_json):
    client = MongoClient("mongodb+srv://group:123@projet.qzgbbxd.mongodb.net/")
    db = client.liensDb
    collection = db.liensCollection
    with open(chemin_fichier_json, 'r') as file:
        data = json.load(file)
        liens = data["liens"]
        if liens:  
            collection.insert_many([{"lien": lien} for lien in liens])
            print("Données sauvegardées avec succès.")
        else:
            print("La liste de liens est vide. Aucune opération de sauvegarde n'a été effectuée.")
    print("Les données ont été importées avec succès dans MongoDB.")