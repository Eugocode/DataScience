# Program: Scraping Data Science Job Data 
# Programmer: Dleamnor Euraze M. Cawaling
"""
To Scrape data from the net, we need to follow these steps:
1. Basics on scraping jobs on LinkedIn
2. Setting up basic spiders and proxy
3. Scraping Data directly thru API calls

Resources:
Data Camp Web Scraping Course
https://www.youtube.com/watch?v=d4iz2NrZVRg&ab_channel=ScrapeOps

"""

# Scraped from: https://maniladormitory.com/emerald-residences-sampaloc-dormitory-near-feu/

# Import scrapy
import scrapy
import pandas as pd 
import re

# Import the CrawlerProcess
from scrapy.crawler import CrawlerProcess
# from scrapy import signals

# Create the Spider class
class DormitorySpider(scrapy.Spider):
    name = 'DormitorySpider'
    # start_requests method
    def start_requests( self ):
        yield scrapy.Request(url ="https://maniladormitory.com/emerald-residences-sampaloc-dormitory-near-feu/"
    , callback=self.parse)
        
    def parse(self, response):
        # Extracting data
        dorm_name = response.xpath('//h1[contains(@class,"entry-title")]/text()').extract_first()
        location = response.xpath('//div[contains(@class,"entry-taxonomies")]/span/a/text()').extract_first()
        dorm_details = self.extract_table_data(response.xpath('.//table'))
        address = response.xpath('//address/text()').extract_first()
        phone_number = response.xpath('//div/a/text()').extract()
        email = response.xpath('//div/a/text()').extract()

        # Yield the extracted data
        yield {
            'Dormitory Name': dorm_name,
            'Location': location,
            'Address': address,
            'Phone': phone_number[1],
            'Email': email[2],
            **dict(dorm_details)
        }

    def extract_table_data(self, table_xpath):
        table_data = {}
        rows = table_xpath.xpath('.//tr')
        for row in rows:
            key = row.xpath('.//td[1]//text()').extract_first()
            value = row.xpath('.//td[2]//text()').extract_first()
            table_data[key] = value

        print(table_data)

        return table_data
    
    # Method to be called when spider is closed
    def closed(self, reason):
        # Create DataFrame from the collected data
        df = pd.DataFrame(self.data)
        # Print DataFrame
        print(df)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(DormitorySpider)
    process.start()