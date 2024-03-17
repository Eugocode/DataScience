import scrapy
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

        # if next_page is not None:
        #     yield response.follow(next_page, callback = self.parse)
        # for quotes in all_div_quotes:
        #     title = quotes.css('span.text::text').extract()
        #     author = quotes.css('.author::text').extract()
        #     tag = quotes.css('.tag::text').extract()

        #     items['title'] = title
        #     items['author'] = author
        #     items['tag'] = tag

        # # Extracting data
        dorm_name = response.xpath('//h1[contains(@class,"entry-title")]/text()').extract_first()
        location = response.xpath('//div[contains(@class,"entry-taxonomies")]/span/a/text()').extract_first()
        dorm_details = self.extract_table_data(response.xpath('.//table'))
        # dorm_details = response.css('.grippy-host , td::text').extract()

        

        # address = response.xpath('//address/text()').extract_first()
        # phone_number = response.xpath('//div/a/text()').extract()
        # email = response.xpath('//div/a/text()').extract()
        # print(dorm_details)
        items['dorm_name'] = dorm_name
        items['location'] = location
        items['dorm_details'] = dorm_details

        # items['address'] = address
        # items['phone_number'] = phone_number[1]
        # items['email'] = email[2]

        yield items  

    def extract_table_data(self, table_xpath):
        table_data = {}
        rows = table_xpath.xpath('.//tr')
        for row in rows:
            key = row.xpath('.//td[1]//text()').extract_first()
            value = row.xpath('.//td[2]//text()').extract_first()
            table_data[key] = value

        # print(table_data)

        return table_data
        # # To scrape next pages
        # next_page = response.css('li.next a::attr(href)').get()

        # if next_page is not None:
        #     yield response.follow(next_page, callback = self.parse)
