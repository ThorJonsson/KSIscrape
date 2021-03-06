import scrapy
from scrapy.spiders import Spider
from KSIbot.items import PlayerItem

import logging


class MySpider(Spider):
	name = "agespider"
	allowed_domains = ["ksi.is"]
	years_to_check = 1



	# default value, overwritten in main.py
	#start_urls = ["http://www.ksi.is/mot/leikmenn/?felag=107&stada=1&kyn=1&ArgangurFra=1800&ArgangurTil=2020"]

	def parse(self, response):

		for sel in response.xpath('//tr[@class="alt"]'):
			player = PlayerItem()
			player['name'] = sel.xpath('td/a/text()')[0].extract().encode("utf-8")
	    		player['year'] = sel.xpath('td[3]/text()')[0].extract()

			player_url = sel.xpath('td/a/@href').extract()[0]
		    	game_info_url = '&pListi=7&dFra-dd=01&dFra-mm=01&dFra-yy=' + \
		    			str(2015 - self.years_to_check) + '&dTil-dd=31&dTil-mm=12&dTil-yy=2015'
		    	full_url = response.urljoin(player_url + game_info_url)
            		player['link'] = full_url

			request = scrapy.Request(full_url, callback=self.parse_dir_contents)
			request.meta['player'] = player

			#utf8_encode = lambda x: x.encode('utf-8')

            		yield request

	def parse_dir_contents(self, response):
		player = response.meta['player']
		player['flokkur'] = []
		for sel in response.xpath('//tr[@class="alt"]'):
			player['flokkur'].append(sel.xpath('td[2]/text()')[0].extract().encode("utf-8"))

	    	yield player
