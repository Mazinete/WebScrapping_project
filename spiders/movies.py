import scrapy
from IMDb_project.items import ImdbProjectItem
import json
import os

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["www.imdb.com"]

    def start_requests(self):
        #chemin absolu du fichier JSON
        json_file_path = os.path.join(os.getcwd(), 'liens.json')

        #charger les liens à partir du fichier JSON
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            liens = data['liens']

        #utiliser les liens comme start_urls
        for lien in liens:
            yield scrapy.Request(url=lien, callback=self.parse)

    def parse(self, response):
        #extraction du titre du film et de sa date de sortie
        title = response.css('h3 > a::text').get()
        release_date = response.css('h3 > span.nobr::text').get()

        #création d'un objet Item pour stocker les données du film
        item = ImdbProjectItem()
        item['title'] = title
        item['release_date'] = release_date
        item['reviews'] = []

        #extraction des commentaires
        reviews = response.css('div.lister-item-content')

        #parcourir les commentaires extraits
        for review in reviews:
            comment = review.css('div.content > div.text::text').extract_first()
            rating = review.css('span.rating-other-user-rating > span::text').extract_first()
            if comment:
                #qjout du commentaire et de l'évaluation à la liste des avis du film
                item['reviews'].append({
                    'comment': comment,
                    'rating': rating
                })

        yield item