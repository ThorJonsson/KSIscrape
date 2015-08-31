#!/usr/bin/python
# -*- coding: utf-8 -*-

# Compares average age of players in each team with data from ksi.is
# Only checks players age 18 or older who have played at least one game in "meistaraflokkur"
# and ignores players whose last game was more than max_years_since_game years ago

from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

from datetime import date


class CrawlerWorker():

	def __init__(self, spider_name, custom_start_urls = None, years_to_check = 0):

		self.items = [] # data to return

		self.settings = get_project_settings()
		if custom_start_urls:
			# overwrite start_urls
			self.settings.set('start_urls', custom_start_urls)
		self.settings.set('max_years_since_game', years_to_check)
		self.process = CrawlerProcess(self.settings)
		self.process.crawl(spider_name, domain='ksi.is')
		# 'agespider' is the name of one of the spiders of the project.
		dispatcher.connect(self.add_item, signals.item_passed)

	def add_item(self, item):
		self.items.append(item)

	
	def run(self):
		self.process.start() # the script will block here until the crawling is finished



def get_team_ages(team_code, gender, min_age=18, max_years_since_game=0):
	# crawls ksi.is and finds the ages of the players of the chosen team
	# returns a vector of ints

	# team_code: string, e.g. KR: 107
	# gender: string, 'male', 'female' or 'both'
	# min_age: int, e.g. 18

	start_url_base = "http://www.ksi.is/mot/leikmenn/?"
	start_url_team = team_code				# add area code
	start_url_status= "&stada=1"				# players = 1, other = 2
	if gender == "male":
		start_url_gender = "&kyn=1"
	elif gender == "female":
		start_url_gender = "&kyn=2"
	else:
		start_url_gender = "&kyn=%25"
	start_url_years = ("&ArgangurFra=1900&ArgangurTil=" +
				str(date.today().year - min_age) )
	start_url = start_url_base + start_url_team + start_url_status + start_url_gender + start_url_years
	start_urls = [start_url]

	player_age_worker = CrawlerWorker('agespider', custom_start_urls = start_urls, years_to_check = max_years_since_game)
	player_age_worker.run()

	# new_worker.items contains vector of ints with player ages


if __name__ == "__main__":


	# ignores players whose last game was more than max_years_since_game years ago
	# ignores players born later than minimum_age

	# parameters:
	minimum_age= 18
	max_years_since_game= 1
	teams = {'KR': '107'}

	get_team_ages(teams['KR'], gender = 'female', min_age=minimum_age, max_years_since_game=1)


