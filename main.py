from fonctions import getUrl,clickerButtonParExpression,clickerButtonByPath,navigationLienByExpression,recuperationLiens,recuperationLienComment,sauvegardeInfosToJson,sauvegardeBD


def main(url):
    driver = getUrl(url)
    if driver:
        print("Extraction de données en cours...")
        clickerButtonParExpression(".dRCGjd",driver)
        clickerButtonByPath('//label[@id="imdbHeader-navDrawerOpen"]',driver)
        driver=navigationLienByExpression('.navlinkcat__listContainerInner', driver)
        liens=recuperationLiens(".ipc-sub-grid-item--span-2",driver)
        liensComment=[]
        for lien in liens:
            driver=getUrl(lien)
            clickerButtonParExpression(".dRCGjd",driver)
            liensComment.append(recuperationLienComment('section[data-testid="UserReviews"] a',driver))
        for lien in liensComment:
            print(lien)
        dictionnaire = {"liens": liensComment}
        sauvegardeInfosToJson(dictionnaire, "liens.json")
        sauvegardeBD("liens.json")
    else:
        print("Erreur lors de la récupération du driver")

if __name__ == "__main__":
    url = "https://www.imdb.com/"
    main(url)

