import scrapy
from IMDb_project.items import ImdbProjectItem

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv"]

    def parse(self, response):
        #extraction du titre du film et de sa date de sortie
        title = response.css('h3[itemprop="name"] a::text').get()
        release_date = response.css('h3[itemprop="name"] .nobr::text').get()

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