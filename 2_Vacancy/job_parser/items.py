# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst, Join


def get_space_0(value):
    value = value.replace(u'\xa0', u'')
    return value

class JobParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    company_name = scrapy.Field(input_processor=MapCompose(get_space_0), output_processor=Join())
    company_address = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose(get_space_0), output_processor=Join())
    vacancy_link = scrapy.Field(output_processor=TakeFirst())
    site_scraping = scrapy.Field(output_processor=TakeFirst())
