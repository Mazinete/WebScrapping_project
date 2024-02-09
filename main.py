from concurrent.futures import ThreadPoolExecutor
from fonctions import getUrl, clickerButtonParExpression, clickerButtonByPath, navigationLienByExpression, recuperationLiens, recuperationLienComment, sauvegardeInfosToJson, sauvegardeBD

def extract_comments(lien):
    driver = getUrl(lien)
    if driver:
        clickerButtonParExpression(".dRCGjd", driver)
        return recuperationLienComment('section[data-testid="UserReviews"] a', driver)

def main(url):
    driver = getUrl(url)
    if driver:
        print("Extraction de données en cours...")
        clickerButtonParExpression(".dRCGjd", driver)
        clickerButtonByPath('//label[@id="imdbHeader-navDrawerOpen"]', driver)
        driver = navigationLienByExpression('.navlinkcat__listContainerInner', driver)
        liens = recuperationLiens(".ipc-sub-grid-item--span-2", driver)

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(extract_comments, liens)

        liensComment = list(results)       

        dictionnaire = {"liens": liensComment}
        sauvegardeInfosToJson(dictionnaire, "liens.json")
        # sauvegardeBD("liens.json")
    else:
        print("Erreur lors de la récupération du driver")

if __name__ == "__main__":
    url = "https://www.imdb.com/"
    main(url)
