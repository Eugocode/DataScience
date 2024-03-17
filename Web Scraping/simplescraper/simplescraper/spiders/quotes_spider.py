# Import scrapy
import scrapy
import pandas as pd 
import re

# Import the CrawlerProcess
from scrapy.crawler import CrawlerProcess
from ..items import SimplescraperItem

# Create the Spider class
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = {
        "https://quotes.toscrape.com/"
    }

    def parse(self, response):
        items = SimplescraperItem()

        all_div_quotes = response.css('div.quote')
        
        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

        # # Extracting data
        # dorm_name = response.xpath('//h1[contains(@class,"entry-title")]/text()').extract_first()
        # location = response.xpath('//div[contains(@class,"entry-taxonomies")]/span/a/text()').extract_first()
        # # dorm_details = self.extract_table_data(response.xpath('.//table'))
        # address = response.xpath('//address/text()').extract_first()
        # phone_number = response.xpath('//div/a/text()').extract()
        # email = response.xpath('//div/a/text()').extract()

            # items['dorm_name'] = dorm_name
            # items['location'] = location
            # items['address'] = address
            # items['phone_number'] = phone_number[1]
            # items['email'] = email[2]

            yield items  

        # To scrape next pages
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)