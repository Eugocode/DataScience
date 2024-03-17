# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SimplescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()

    # dorm_name = scrapy.Field()
    # location = scrapy.Field()
    # address = scrapy.Field()
    # phone_number = scrapy.Field()
    # email = scrapy.Field()

