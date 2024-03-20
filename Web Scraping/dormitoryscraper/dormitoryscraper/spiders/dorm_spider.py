import scrapy
import re
from ..items import DormitoryscraperItem


class DormSpiderSpider(scrapy.Spider):
    name = "dorm_spider"
    start_urls = ["https://maniladormitory.com/"]

    def parse(self, response):
        
        home_page_links = response.css('.grippy-host , .has-large-font-size a::attr(href)').extract()
        
        for link in home_page_links:
            yield response.follow(link, callback=self.parse2)

    def parse2(self, response):
        # This function should handle parsing the data from each individual page.
        category_links = response.css('.entry-title a::attr(href)').extract()
        for link in category_links:
            yield response.follow(link, callback=self.parse3)
        # print(category_links)

    def parse3(self, response):
        items = DormitoryscraperItem()

        # # Extracting data
        dorm_name = response.xpath('//h1[contains(@class,"entry-title")]/text()').extract_first()
        location = response.xpath('//div[contains(@class,"entry-taxonomies")]/span/a/text()').extract_first()
        dorm_details = self.extract_table_data(response.xpath('.//table'))
        # dorm_details = response.css('.grippy-host , td::text').extract()
        address = response.xpath('//address/text()').extract_first()
        emails = response.xpath('//a[contains(@href, "mailto:")]/text()').extract()
        phone_numbers = response.xpath('//a[contains(@href, "tel:")]/text()').extract()

        # Some emails and phone numbers don't have mailto or tel tags
        # We will use regular expression to extract email addresses and phone numbers 
        if not emails:
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_regex, response.text)
        
        if not phone_numbers:
            phone_regex = r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
            phone_numbers = re.findall(phone_regex, response.text)

        items['dorm_name'] = dorm_name
        items['location'] = location
        items['dorm_details'] = dorm_details
        items['address'] = address
        items['phone_number'] = phone_numbers
        items['email'] = emails

        yield items  

    def extract_table_data(self, table_xpath):
        table_data = {}
        rows = table_xpath.xpath('.//tr')
        for row in rows:
            key = row.xpath('.//td[1]//text()').extract_first()
            value = row.xpath('.//td[2]//text()').extract_first()
            table_data[key] = value

        return table_data
