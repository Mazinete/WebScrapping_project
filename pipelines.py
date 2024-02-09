from itemadapter import ItemAdapter
import json
    
class DataCleaning_Pipeline:
    #Pipeline pour nettoyer et normaliser les données avant de les envoyer en json. Principalement, les titres
    #et les date de sorties des films qui avaient des problèmes de format.
    def process_item(self, item, spider):
        if item['title']:
            item['title'] = item['title'].strip()
        if item['release_date']:
            item['release_date'] = item['release_date'].strip()
        for review in item['reviews']:
            if review['comment']:
                review['comment'] = review['comment'].strip()
            if review['rating']:
                review['rating'] = review['rating'].strip()
        return item

class Json_Pipeline:
    #Piepline pour créer le fichier json qu'on envoie ensuite pour l'entrainement de notre modèle ML
    def open_spider(self, spider):
        self.file = open('data.json', 'w')
        self.first_item = True
        self.file.write('[')

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False
        
        line = json.dumps(dict(item))
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()