# gb_parsing
# Методы сбора и обработки данных из сети Интернет


## Lesson 01
### Основы клиент-серверного взаимодействия. Парсинг API

1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл. 
В решении задания взят API вконтакте (https://vk.com/dev/first_guide) и сделан запрос на получение списка всех сообществ на которые подписан пользователь.


## Lesson 02
### Парсинг HTML. BeautifulSoup
#### Задание 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:

- Наименование вакансии
- Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
- Ссылку на саму вакансию
- Сайт откуда собрана вакансия

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.


#### Задание 2
Источник https://geekbrains.ru/posts/
Необходимо обойти все записи в блоге и извлечь из них информацию следующих полей:

- url страницы материала
- Заголовок материала
- Первое изображение материала
- Дата публикации (в формате datetime)
- имя автора материала
- ссылка на страницу автора материала

Пример словаря:

{

"url": "str",

"title": "str",

"image": "str",

"writer_name": "str",

"writer_url": "str",

"pub_date": datetime object,


}

Полученые материалы сохранить в MongoDB. Предусмотреть метод извлечения данных из БД за период передаваемый в качестве параметров


## Lesson 03
### Системы управления базами данных MongoDB и SQLite в Python

1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД

2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы

3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта


## Lesson 04
### Парсинг HTML. XPath

Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:

- название источника,
- наименование новости,
- ссылку на новость,
- дата публикации

Собрать все в базу данных (MongoDB)

