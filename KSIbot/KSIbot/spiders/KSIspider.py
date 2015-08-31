from scrapy.spiders import Spider
from KSIbot.items import KsibotItem

import logging


class MySpider(Spider):
	name = "testspider"
	allowed_domains = ["ksi.is"]
	start_urls = ["http://www.ksi.is/mot/leikmenn/?felag=107&stada=1&kyn=1&ArgangurFra=1800&ArgangurTil=2020"]

	def parse(self, response):

		for sel in response.xpath('//ul/li'):
			item = KsibotItem()
			item['title'] =  sel.xpath('a/text()').extract()
	    		item['link'] = sel.xpath('a/@href').extract()
            		item['desc'] = sel.xpath('text()').extract()

			map(lambda x: x.encode('utf-8'), item['title'])

			#for title in item['title']:
			#	item['title'] = title.encode('utf-8')

            		yield item
