def main():
	'''
	from bs4 import BeautifulSoup
	import urllib3
	import requests
	import re


	r = requests.get('http://allrecipes.com/recipe/10813/best-chocolate-chip-cookies/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%202')
	soup = BeautifulSoup(r.content, 'lxml')


	#print(soup.title)
	#print(soup.prettify())
	#print(soup.get('"ctl00_CenterColumnPlaceHolder_recipe_h5Prep"'))
	ingredients_html = soup.find_all('li' , {'class':  "checkList__line"})
	#print(soup.get_text())
	'''

from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string

from urllib import request
from bs4 import BeautifulSoup

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}


class AbstractScraper():

    def __init__(self, url, test=False):
        if test:  # when testing, we load a file
            with url:
                self.soup = BeautifulSoup(url.read(), "html.parser")
        else:
            self.soup = BeautifulSoup(request.urlopen(request.Request(url, headers=HEADERS)).read(), "html.parser")

    def host(self):
        """ get the host of the url, so we can use the correct scraper (check __init__.py) """
        raise NotImplementedError("This should be implemented.")

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """ total time it takes to preparate the recipe in minutes """
        raise NotImplementedError("This should be implemented.")

    def ingredients(self):
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
raise NotImplementedError("This should be implemented.")
class AllRecipes(AbstractScraper):

    def host(self):
        return 'allrecipes.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return get_minutes(self.soup.find('span', {'class': 'ready-in-time'}))

    def ingredients(self):
        ingredients_html = self.soup.findAll('li', {'class': "checkList__line"})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
            if ingredient.get_text(strip=True) not in ('Add all ingredients to list', '')
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('span', {'class': 'recipe-directions__list--item'})

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
])



