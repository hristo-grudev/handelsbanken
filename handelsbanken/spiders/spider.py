import scrapy

from scrapy.loader import ItemLoader
from ..items import HandelsbankenItem
from itemloaders.processors import TakeFirst


class HandelsbankenSpider(scrapy.Spider):
	name = 'handelsbanken'
	start_urls = ['https://vp292.alertir.com/sv/node/1']

	def parse(self, response):
		post_links = response.xpath('//span[@class="field-content"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content"]//div[@class="body"]//text()[normalize-space() and not(ancestor::div[@class="empty"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date-display-single"]/text()').get()

		item = ItemLoader(item=HandelsbankenItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
