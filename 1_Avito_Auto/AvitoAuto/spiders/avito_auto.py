# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import HtmlResponse
from AvitoAuto.items import AvitoAutoItem
from scrapy.loader import ItemLoader


class AvitoAutoSpider(scrapy.Spider):
    name = 'avito_auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/iskitim/transport']

    def parse(self, response: HtmlResponse):
        ads_links = response.css('div.styles-root-2Jty7 ::attr(href)')
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoAutoItem(), response=response)

        loader.add_css('title',
                       'h1.title-info-title span.title-info-title-text ::text')

        loader.add_css('images',
                       'div[class*="gallery-img-frame"] ::attr(data-url)')

        loader.add_css('auto_params', 'li.item-params-list-item ::text')

        loader.add_css('prices', 'span[class="js-item-price"] ::attr(content)')

        loader.add_value('url', response.url)

        yield loader.load_item()

#        loader.add_xpath('prices', './/span[@class="js-item-price"][1]/text()')
