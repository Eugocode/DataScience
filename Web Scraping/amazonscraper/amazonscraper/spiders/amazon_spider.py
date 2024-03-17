import scrapy
from ..items import AmazonscraperItem

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon"
    start_urls = [
        "https://www.amazon.com/s?k=best+sellers+books&i=stripbooks-intl-ship&rh=n%3A283155%2Cp_n_feature_browse-bin%3A2656020011&dc&crid=25AE6IN7O1NGA&qid=1710691081&rnid=618072011&sprefix=best+sellers+books+2024%2Cstripbooks-intl-ship%2C310&ref=sr_nr_p_n_feature_browse-bin_2&ds=v1%3AAyv4lY%2F%2FxKnCWsYY%2BpPF0ayrJGrcM9C2D2AGpyu%2F49Y"
    ]

    def parse(self, response):
        items = AmazonscraperItem

        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_author = response.css('.a-color-secondary .a-row .a-size-base+ .a-size-base').css('::text').extract()
        product_price = response.css('.a-price span span').css('::text').extract()
        product_imaglink = response.css('.s-image::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imaglink'] = product_imaglink

        yield items