# -*- coding: utf-8 -*-

import random
import re
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timedelta
from time import sleep
from urllib.parse import urljoin
from urllib.request import urlopen

import pymorphy2
from bs4 import BeautifulSoup

START_URL = 'https://habr.com/all/'


def parse_args():
    parser = ArgumentParser(description='Static noun code analyser.')
    parser.add_argument('-p', '--pages', type=int, default=20, dest='pages')
    parser.add_argument('-t', '--top', type=int, default=3, dest='top')
    return parser.parse_args()


def get_number_of_page():
    args = parse_args()
    return args.pages


def get_top_words():
    args = parse_args()
    return args.top


def get_response(url):
    try:
        sleep(random.random())
        v_data = urlopen(url).read()
    except:
        v_data = ""
        print(url)

    return v_data


def get_raw_data_from_habr(response):
    raw_data = []
    soup = BeautifulSoup(response, "html.parser")
    articles = soup.findAll('article', {'class': 'post_preview'})
    for article in articles:
        title = article.find('a', {'class': 'post__title_link'}).contents[0]
        date = article.find('span', {'class': 'post__time'}).contents[0]
        raw_data.append((date, title))
    return raw_data


def format_date(raw_date):
    replaced_months = {
        'января': 'January',
        'февраля': 'February',
        'марта': 'March',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December',
        'сегодня': datetime.today().strftime("%d %B %Y"),
        'вчера': (datetime.today() - timedelta(1)).strftime("%d %B %Y")
    }

    for month, replaced in replaced_months.items():
        if month in raw_date:
            raw_date = raw_date.replace(month, replaced)
            break

    try:
        dt = datetime.strptime(raw_date, "%d %B %Y в %H:%M")

    except:
        dt = datetime.strptime(raw_date, "%d %B в %H:%M").replace(
            year=datetime.today().year
        )

    return dt.strftime("%d/%m/%Y")


def get_formatted_data(raw_data):
    formatted_date = []
    for data in raw_data:
        formatted_date.append((format_date(data[0]), data[1]))
    return formatted_date


def get_next_page_url_from_response(response):
    soup = BeautifulSoup(response, "html.parser")
    next_page = soup.find('a', {'id': 'next_page'}).attrs.get('href')
    next_page = urljoin(START_URL, next_page)
    return next_page


def get_page_number_from_url(url):
    page_number = re.search(r"\/page(\d+)\/", url)
    if not page_number:
        return 0
    return int(page_number.group(1))


def get_data_from_habr(pages):
    """
    :param pages: number of pages to parse
    :return: list like  [(date, title), (date, title)]
    [('12/04/2018', 'Программирование голоса'),
    ('13/04/2018', 'Анализ кода')]

    """
    data = []
    response = get_response(START_URL)
    if not response:
        return []
    while True:
        raw_data = get_raw_data_from_habr(response)
        data.extend(get_formatted_data(raw_data))
        next_page = get_next_page_url_from_response(response)
        if not next_page:
            break
        page_number = get_page_number_from_url(next_page)
        if page_number and page_number > pages:
            break
        response = get_response(next_page)

    return data


def create_dict_with_nouns_by_weeks(data):
    """
    :param data: list like [(date, title), (date, title)]
    [('12/04/2018', 'Программирование голоса'),
    ('13/04/2018', 'Анализ кода')]

    :return: dict like {(date start week, date end week): [nouns])), (...)}
    {
    ('09/04/2018', '15/04/2018'): ['Программирование','голос','анализ','код'],
    ((...): [])
    }
    """
    dict_nouns_of_weeks = {}
    for line in data:
        nouns_of_week = create_nouns_of_week(line)
        base_list = dict_nouns_of_weeks.get(nouns_of_week[0], [])
        base_list.extend(nouns_of_week[1])
        dict_nouns_of_weeks[nouns_of_week[0]] = base_list

    return dict_nouns_of_weeks


def dict_to_list(dict_nouns_with_dates):
    list_nouns_of_weeks = []
    for key, value in dict_nouns_with_dates.items():
        list_nouns_of_weeks.append((key, value))
    return list_nouns_of_weeks


def create_nouns_of_week(date_with_title):
    range_of_weeks = get_range_of_weeks_by_day(date_with_title[0])
    list_with_nouns = get_nouns_from_text(date_with_title[1])
    return (range_of_weeks[0], range_of_weeks[1]),  sorted(list_with_nouns)


def get_range_of_weeks_by_day(day):
    dt = datetime.strptime(day, '%d/%m/%Y')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start.strftime('%d/%m/%Y'), end.strftime('%d/%m/%Y')


def get_nouns_from_text(raw_string):
    """
    :param raw_string: string with sentence
    :return: list like ['noun', 'noun']
    """
    nouns = set()
    for word in re.sub(r'[^а-яё ]', ' ', raw_string.lower()).split():
        if is_noun(word):
            normal_form = get_normal_form(word)
            nouns.add(normal_form)
    return list(nouns)


def get_normal_form(word):
    morph = pymorphy2.MorphAnalyzer()
    options = morph.parse(word)
    for option in options:
        if {'NOUN'} in option.tag:
            return option.normal_form
    return word


def is_noun(word):
    morph = pymorphy2.MorphAnalyzer()
    options = morph.parse(word)
    if len(options) == 0:
        return False

    for option in options:
        if {'PREP'} in option.tag:
            return False
        if {'CONJ'} in option.tag:
            return False
    for option in options:
        if {'NOUN'} in option.tag:
            return True
    return False


def format_one_line_to_print(source, sizes, delimiter, filler=' '):
    template_output = '{}{}{}{}{}{}{}'

    output_str = template_output.format(
        delimiter.ljust(2, filler), source[0].center(sizes[0], filler),
        delimiter.center(3, filler), source[1].center(sizes[1], filler),
        delimiter.center(3, filler), source[2].ljust(sizes[2], filler),
        delimiter.rjust(2, filler))
    return output_str


def get_max_len_words_for_output(list_nouns_with_dates):
    max_len = 0
    for str_with_nouns in list_nouns_with_dates:
        if len(str_with_nouns[2]) > max_len:
            max_len = len(str_with_nouns[2])
    return max_len


def output_results(list_nouns_with_dates):
    max_length_words = get_max_len_words_for_output(list_nouns_with_dates)
    size_list = [13, 12, max(16, max_length_words)]
    delimiter_vert = '|'
    delimiter_hor = '-'

    header_list = ['Начало недели', 'Конец недели', 'Популярные слова']
    splitter_list = [one_size * delimiter_hor for one_size in size_list]

    print(format_one_line_to_print(
        splitter_list, size_list, delimiter_hor, delimiter_hor)
    )
    print(format_one_line_to_print(
        header_list, size_list, delimiter_vert)
    )
    print(format_one_line_to_print(
        splitter_list, size_list, delimiter_hor, delimiter_hor)
    )
    for one_line in list_nouns_with_dates:
        print(format_one_line_to_print(
            one_line, size_list, delimiter_vert)
        )
    print(format_one_line_to_print(
        splitter_list, size_list, delimiter_hor, delimiter_hor)
    )


def get_most_common_words(nouns_with_dates, top=3):
    most_common_words = []
    for one_week in nouns_with_dates:
        most_common_words.append(
            (
                one_week[0],
                [mcw for mcw in Counter(one_week[1]).most_common(top)]
            )
        )
    return most_common_words


def prepare_most_common_words_to_output(most_common_words):
    prepared_most_common_words = []
    for word in most_common_words:
        prepared_most_common_words.append(
            (word[0][0],
             word[0][1],
             ', '.join(w[0] for w in word[1]))
        )
    return prepared_most_common_words


def main():
    pages = get_number_of_page()
    top = get_top_words()
    data = get_data_from_habr(pages)
    dict_with_nouns_by_weeks = create_dict_with_nouns_by_weeks(data)
    list_with_nouns_by_weeks = dict_to_list(dict_with_nouns_by_weeks)
    most_common_words_by_weeks = get_most_common_words(
        list_with_nouns_by_weeks,
        top
    )
    most_common_words_by_weeks_to_output = prepare_most_common_words_to_output(
        most_common_words_by_weeks
    )

    output_results(most_common_words_by_weeks_to_output)


if __name__ == '__main__':
    main()
