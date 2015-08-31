#!/usr/bin/python
# -*- coding: utf-8 -*-

# Compares average age of players in each team with data from ksi.is
# Only checks players age 18 or older who have played at least one game in "meistaraflokkur"
# and ignores players whose last game was more than years_since_game_threshold years ago

from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import multiprocessing

from datetime import date

# ignores players whose last game was more than years_since_game_threshold years ago
years_since_game_threshold = 1
year_treshold = date.today().year - years_since_game_threshold


class CrawlerWorker():

	def __init__(self, spider_name):

		self.items = [] # data to return
		self.process = CrawlerProcess(get_project_settings())
		self.process.crawl(spider_name, domain='ksi.is')
		# 'testspider' is the name of one of the spiders of the project.
		dispatcher.connect(self.add_item, signals.item_passed)

	def add_item(self, item):
		self.items.append(item)

	
	def run(self):
		self.process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":

	result_queue = Queue()
	new_worker = CrawlerWorker('testspider')

	new_worker.run()

	for it in new_worker.items:
		for s in it['title']:
			print s


