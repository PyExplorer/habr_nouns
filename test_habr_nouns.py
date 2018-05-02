# # -*- coding: utf-8 -*-
#
import unittest

import habr_nouns


class TestHabrNouns(unittest.TestCase):

    # def setUp(self):
    #     pass

    def test_get_number_of_page(self):
        self.assertEqual(habr_nouns.get_number_of_page(), 20)

    def test_format_one_line_to_print(self):
        header_list = ['Начало недели', 'Конец недели', 'Популярные слова']
        size_list = [13, 12, 20]
        self.assertEqual(
            habr_nouns.format_one_line_to_print(
                header_list, size_list, '|', filler=' '
            ),
            '| Начало недели | Конец недели | Популярные слова     |'
        )

    def test_get_max_len_words_for_output(self):
        list_nouns_with_dates = [
            ('09.01.2017', '15.01.2017', 'программирование, голос, основа'),
            ('23.04.2018', '30.04.2018', 'Дайджест, материал, видео')
        ]
        self.assertEqual(
                habr_nouns.get_max_len_words_for_output(list_nouns_with_dates),
                31
            )

    def test_get_range_of_weeks_by_day(self):
        self.assertEqual(habr_nouns.get_range_of_weeks_by_day('12/04/2018'),
                         ('09/04/2018', '15/04/2018'))
        self.assertEqual(habr_nouns.get_range_of_weeks_by_day('01/03/2018'),
                         ('26/02/2018', '04/03/2018'))
        self.assertEqual(habr_nouns.get_range_of_weeks_by_day('05/02/2018'),
                         ('05/02/2018', '11/02/2018'))
        self.assertEqual(habr_nouns.get_range_of_weeks_by_day('29/02/2016'),
                         ('29/02/2016', '06/03/2016'))

    def test_get_nouns_from_text(self):
        test_str = 'Программирование голоса stm32f103 с самых основ ' \
                   'программирования'
        self.assertCountEqual(
            habr_nouns.get_nouns_from_text(test_str),
            ['программирование', 'голос', 'основа']
        )

    def test_is_noun(self):
        self.assertEqual(habr_nouns.is_noun('голос'), True)
        self.assertEqual(habr_nouns.is_noun('программировать'), False)
        self.assertEqual(habr_nouns.is_noun('с'), False)
        self.assertEqual(habr_nouns.is_noun('по'), False)
        self.assertEqual(habr_nouns.is_noun('и'), False)

    def test_get_normal_form(self):
        self.assertEqual(habr_nouns.get_normal_form('голоса'), 'голос')
        self.assertEqual(
            habr_nouns.get_normal_form('программирования'), 'программирование'
        )

    def test_dict_get_nouns_of_weeks(self):
        test_list = [
            ('12/04/2018', 'Программирование голоса'),
            ('13/04/2018', 'Анализ кода'),
            ('13/05/2018', 'языки и питон'),
            ('14/05/2018', 'разбор полетов'),
        ]

        self.assertCountEqual(
            habr_nouns.get_dict_nouns_of_weeks(test_list),
            {
                ('09/04/2018', '15/04/2018'):
                    ['голос', 'программирование', 'анализ', 'код'],
                ('14/05/2018', '20/05/2018'):
                    ['полёт', 'разбор'],
                ('07/05/2018', '13/05/2018'):
                    ['питон', 'язык']
            }
        )

    def test_dict_to_list(self):
        test_dict = {
                ('09/04/2018', '15/04/2018'):
                ['голос', 'программирование', 'анализ', 'код'],
                ('14/05/2018', '20/05/2018'):
                ['полёт', 'разбор'],
                ('07/05/2018', '13/05/2018'):
                ['питон', 'язык']
            }

        self.assertCountEqual(
            habr_nouns.dict_to_list(test_dict),
            [
                (
                    ('09/04/2018', '15/04/2018'),
                    ['голос', 'программирование', 'анализ', 'код']
                ),
                (
                    ('14/05/2018', '20/05/2018'),
                    ['полёт', 'разбор']
                ),
                (
                    ('07/05/2018', '13/05/2018'),
                    ['питон', 'язык']
                ),

            ])

    def test_create_nouns_of_week(self):
        self.assertCountEqual(
            habr_nouns.create_nouns_of_week(
                ('12/04/2018', 'Программирование голоса')),
            (('09/04/2018', '15/04/2018'), ['голос', 'программирование']))

    def test_format_date(self):
        dt_today = habr_nouns.datetime.today()
        dt_yesterday = habr_nouns.datetime.today() - habr_nouns.timedelta(1)

        self.assertEqual(habr_nouns.format_date('сегодня в 12:03'),
                         dt_today.strftime("%d/%m/%Y")
                         )
        self.assertEqual(habr_nouns.format_date('вчера в 16:41'),
                         dt_yesterday.strftime("%d/%m/%Y")
                         )
        self.assertEqual(habr_nouns.format_date('29 апреля в 21:14'),
                         '29/04/2018'
                         )
        self.assertEqual(habr_nouns.format_date('22 декабря 2017 в 12:48'),
                         '22/12/2017'
                         )


if __name__ == "__main__":
    unittest.main()
