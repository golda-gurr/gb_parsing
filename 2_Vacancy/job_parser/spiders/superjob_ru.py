import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem
from scrapy.loader import ItemLoader


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacancy=None):
        super(SuperjobRuSpider, self).__init__()
        self.start_urls = [
            f'https://russia.superjob.ru/vacancy/search/?keywords={vacancy}'
        ]

    def parse(self, response: HtmlResponse, start=True):
        next_page = response.css('a.f-test-link-Dalshe ::attr(href)') \
            .extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.css(
            'div.f-test-vacancy-item \
            a[class*=f-test-link][href^="/vakansii"]::attr(href)'
            ).extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=JobParserItem(), response=response)

        loader.add_css('name',
                       'div._3MVeX h1 ::text')

        loader.add_css('company_name',
                       'h2._15msI ::text')

        loader.add_css('company_address', 'div.f-test-address span._2JVkc ::text')

        loader.add_css('salary', 'div._3MVeX span[class="_3mfro _2Wp8I PlM3e _2JVkc"] ::text')

        loader.add_value('vacancy_link', response.url)

        loader.add_value('site_scraping', self.allowed_domains[0])

        yield loader.load_item()
