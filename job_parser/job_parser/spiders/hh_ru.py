import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem
from scrapy.loader import ItemLoader


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    def __init__(self, vacancy=None):
        super(HhRuSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=2019&st=searchVacancy&text={vacancy}'
        ]

    def parse(self, response: HtmlResponse, start=True):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)') \
            .extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items = response.css(
            'div.vacancy-serp \
            div.vacancy-serp-item \
            div.vacancy-serp-item__row_header \
            a.bloko-link::attr(href)'
            ).extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=JobParserItem(), response=response)

        loader.add_css('name',
                       'h1.bloko-header-1 ::text')

        loader.add_css('company_name',
                       'div.vacancy-company-name-wrapper \
                        span.bloko-section-header-2 ::text')

        loader.add_css('company_address', 'div.vacancy-company_with-logo \
                        p[data-qa="vacancy-view-location"] ::text')

        loader.add_css('salary', 'div.vacancy-title p.vacancy-salary ::text')

        loader.add_value('vacancy_link', response.url)

        loader.add_value('site_scraping', self.allowed_domains[0])

        yield loader.load_item()
