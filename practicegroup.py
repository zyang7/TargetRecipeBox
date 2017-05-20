from urllib import request
from bs4 import BeautifulSoup
import re

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}



TIME_REGEX = re.compile(r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?')


def get_minutes(dom_element):
	try:
		tstring = dom_element.get_text()
		if '-' in tstring:
			tstring = tstring.split('-')[1]  # some time formats are like this: '12-15 minutes'
		matched = TIME_REGEX.search(tstring)
		minutes = int(matched.groupdict().get('minutes') or 0)
		minutes += 60 * int(matched.groupdict().get('hours') or 0)
		return minutes
	except AttributeError:  # if dom_element not found or no matched
		return 0


def normalize_string(string):
	return re.sub(r'\s+', ' ', string.replace(
			'\xa0', ' ').replace(  # &nbsp;
			'\n', ' ').replace(
			'\t', ' ').strip())

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

		return [normalize_string(ingredient.get_text()) for ingredient in ingredients_html if ingredient.get_text(strip=True) not in ('Add all ingredients to list', '')]

	def instructions(self):
		instructions_html = self.soup.findAll('span', {'class': 'recipe-directions__list--item'})

		return '\n'.join([normalize_string(instruction.get_text()) for instruction in instructions_html])

def main():
	finallist = []
	url = AllRecipes('http://allrecipes.com/recipe/10813/best-chocolate-chip-cookies/?internalSource=hub%20recipe&referringContentType=search%20results&clickId=cardslot%202')
	list1 = url.ingredients()
	for item in list1:
		list2 = item.split(' ')
		list2.pop(-1)
		str1 = " ".join(list2)
		print(str1)
		if len(str1)!= 0:
			finallist.append(str1)
	print(finallist)
main()




