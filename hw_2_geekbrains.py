
"""
Урок 2. Парсинг HTML. BeautifulSoup, MongoDB
Практическое задание

Источник https://geekbrains.ru/posts/

Необходимо обойти все записи в блоге и извлеч из них информацию следующих полей:

url страницы материала
Заголовок материала
Первое изображение материала
Дата публикации (в формате datetime)
имя автора материала
ссылка на страницу автора материала
пример словаря:

{
"url": "str",
"title": "str",
"image": "str",
"writer_name": "str",
"writer_url": "str",
"pub_date": datetime object,

}
полученые материалы сохранить в MongoDB
предусмотреть метод извлечения данных из БД за период передаваемый в качестве параметров

"""
from typing import List, Dict
import re
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint

class GBBlogParse:
    domain = 'https://geekbrains.ru'
    start_url = 'https://geekbrains.ru/posts'

    # Контролируем посещенные адреса страниц
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['parse_gb_blog']
        self.collection = self.db['posts']
        self.visited_urls = set()
        self.post_links = set()  # сохраним ссылки в множество
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.posts_data = []


    # Функция print_period производит поиск и выводит на экран посты за период, передаваемый в качестве параметров
    # Поиск выполняется по полю pub_date
    def print_period(self, start_date, end_date):
        objects = self.collection.find({'$and': [ {'pub_date': {'$gte': start_date}}, {'pub_date': {'$lte': end_date}} ]})
        for obj in objects:
            pprint(obj)


    # обход ленты по пагинации
    def parse_rows(self, url=start_url):
        while url:
            if url in self.visited_urls:
                break
            response = requests.get(url, headers=self.headers)
            self.visited_urls.add(url)
            soap = bs(response.text, 'lxml')
            url = self.get_next_page(soap)
            self.search_post_links(soap)

    def get_next_page(self, soap: bs) -> str:
        ul = soap.find('ul', {'class': 'gb__pagination'})
        # a = ul.find('a', {'rel':'next'})
        a = ul.find('a', text=re.compile('›'))
        return f'{self.domain}{a.get("href")}' if a and a.get("href") else None

    # Извлечение из ленты ссылки на материалы
    def search_post_links(self, soap: bs) -> List[str]:
        # return list()
        wrapper = soap.find('div', {'class': "post-items-wrapper"})
        posts = wrapper.find_all('div', {'class': "post-item"})
        # tmp = wrapper.find('div', attrs={'class': "post-item"})
        # w = tmp.find('a').get("href")
        links = {f'{self.domain}{itm.find("a").get("href")}' for itm in posts}
        # print(links)
        self.post_links.update(links)
        # print(self.post_links)

    # Зайти на страницу материала
    def post_page_parse(self):
        for url in self.post_links:
            if url in self.visited_urls:
                continue
            response = requests.get(url, headers=self.headers)
            self.visited_urls.add(url)
            soap = bs(response.text, 'lxml')
            if len(self.posts_data) > 50:  # ограничим количество записейю, выводимых в БД
                break
            self.posts_data.append(self.get_posts_data(soap))

    # Извлечение данных из страницы материала
    def get_posts_data(self, soap: bs) -> Dict[str, str]:
        result = {}

        # url
        post_url = soap.find('head').find('link')['href']
        result['url'] = post_url

        # title
        result['title'] = soap.find('h1', {'class': "blogpost-title"}).text

        # image
        content = soap.find('div', {'class': "blogpost-content", 'itemprop': 'articleBody'})
        img = content.find('img')
        if img:
            result['image'] = img.get('src')

        # writer_name
        writer_name = soap.find('div', {'class': 'text-lg text-dark', 'itemprop': 'author'}).getText()
        result['writer_name'] = writer_name

        # writer_url
        writer_url = soap.find('div', {'class': 'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}) \
            .find('a')['href']

        result['writer_url'] = f'{self.domain}{writer_url}'

        # pub_date
        pub_date = soap.find('time', {'class': 'text-md text-muted m-r-md'})['datetime']
        result['pub_date'] = pub_date

        return result

    def save_to_mongo(self):
        self.collection.insert_many(self.posts_data)

if __name__ == '__main__':
    parser = GBBlogParse()
    parser.parse_rows()
    parser.post_page_parse()
    parser.save_to_mongo()
#    parser.print_period('2016-09-28', '2018-10-23')
