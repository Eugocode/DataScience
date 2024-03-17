# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DormitoryscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dorm_name = scrapy.Field()
    location = scrapy.Field()
    dorm_details = scrapy.Field()
    # address = scrapy.Field()
    # phone_number = scrapy.Field()
    # email = scrapy.Field()
