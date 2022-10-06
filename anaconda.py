# -*- coding: utf-8 -*-

"""
Information Extraction (IE)
автоматическое экстрагирование значимых для человека данных
 https://www.hse.ru/data/2017/08/12/1174382138/NLPandDA_4print.pdf
В качестве извлекаемых из текстов данных обычно выступают [16]:
∙ значимый объект: имя персоналии, название компании и пр. для но-
востных сообщений, термин предметной области специального текста,
ссылка на литературу для научно-технических документов и т. д.;
∙ атрибуты объекта, дополнительно характеризующие его, например,
для компании это юридический адрес, телефон, имя руководителя и
т.п.;
∙ отношение между объектами: к примеру, отношение «быть владель-
цем» связывает компанию и персону-владельца, «быть частью» со-
единяет факультет и университет;
∙ событие/факт, связывающее несколько объектов, например, событие
«прошла встреча» включает участников встречи, а также место и вре-
мя ее проведения.
Согласно видам извлекаемой информации общая задача извлечения
информации из текстов включает следующие основные подзадачи:
∙ распознавание и извлечение именованных сущностей (named
entities): А.П. Чехов, Нижний Тагил, ПКО «Картография» и т.п.;
∙ выделение атрибутов (attributes) объектов и семантических отно-
шений (relations) между ними: даты рождения персоны, отношения
«работать в» и т. д.;
∙ извлечение фактов и событий (events), охватывающих несколько их
параметров (атрибутов), например, событие «кораблекрушение» с ат-
рибутами дата, время, ме
"""

import re
from typing import Union


# =========================================================
# =========================================================
def listmerge(lst):
    res = []
    for el in lst:
        res += listmerge(el) if isinstance(el, list) else [el]
    return res


# =========================================================
# =========================================================

def FUNC(s):
    # SRC !!!https://stackoverflow.com/questions/71204703/python-regex-extract-numbers-from-text-that-may-contain-thousands-or-millions

    ppp = r'\b\d{1,2}\.\d{1,2}\.\d{2}(?:\d{2})?\b|\b(?<!\d[.,])(\d{1,3}(?=([.,])?)(?:\2\d{3})*|\d+)(?:(?(2)(?!\2))[.,](\d+))?\b(?![,.]\d)'

    def postprocess(x):
        if x.group(3):
            return f"{x.group(1).replace(',', '').replace('.', '')}.{x.group(3)}"
        elif x.group(2):
            return f"{x.group(1).replace(',', '').replace('.', '')}"
        elif x.group(1):
            return x.group(1)
        else:
            return None

    ll = []
    for el in list(re.finditer(ppp, s)):
        ll.append([el.group(0), el.span(0), postprocess(el)])
    return ll


def strip_comments(s):
    # https://coder-solution-ru.com/solution-ru-blog/819451
    """Return s with comments removed.

    Comments in an email address are any characters enclosed in parentheses.
    These are essentially ignored, and do not affect what the address is.

    >>> strip_comments('exam(alammma)ple@e(lectronic)mail.com')
    'example@email.com'"""
    COMMENT_PATTERN = re.compile(r'\(.*?\)')
    return re.sub(COMMENT_PATTERN, " ", s)


# =========================================================
#       Spirit - сущность ,привидение
#       power - сила (можно сортировать)
# =========================================================


class Spirit(object):
    key = ''
    power = 0

    def __init__(self, s, span, key=['?', 5]):
        self.s = s
        self.span = span
        if isinstance(key, list):
            self.key, self.power = key[0], key[1]
        else:
            self.key = key

    def get_pos(self):
        return list(range(self.span[0], self.span[1]))

    # def __str__(self):
    #     return f'Spirit<{self.key}:{self.power}>: {self.s} pos:{self.span}'

    def __repr__(self):
        return f'Spirit<{self.key}>: {self.s} |'

    def __lt__(self, other):
        return self.power < other.power


class SpiritNumeric(Spirit):
    def __init__(self, s, span, key='?'):
        super().__init__(s, span, self.key)
        s = s.replace(',', '.')
        """self.s, self.key = int(s),'Int'
            ValueError: invalid literal for int() with base 10: '2RS1/C3'
        """
        if '.' in s:  # TODO try
            self.s, self.key = float(s), 'Float'
        else:
            self.s, self.key = int(s), 'Int'
        # self.kol = kol


class SpiritNumericLat(Spirit):
    key = 'NumbLat'
    power = 50

    def __init__(self, s, span, kol):
        super().__init__(s, span, self.key)
        self.kol = kol


class SpiritThing(Spirit):
    key = 'Pcs'
    power = 80

    def __init__(self, s, span, kol):
        super().__init__(s, span, self.key)
        self.kol = kol

    def __repr__(self):
        return f'Spirit<{self.key}>: {self.s}->{self.kol} |'

    # def __str__(self):
    #     return f'Spirit<{self.key}>: {self.s}->{self.kol}'


# =========================================================
#            regex = r"\b\подш[.а-яёА-ЯЁ]*\b"
# regex = r"\b[_]*[A-Za-z0-9/-_]+[_]*\b" => __DDD766-DD__
# =========================================================

class Re_find(object):
    """Вынесено в отд класс для изоляции кода """

    @staticmethod
    def split_list(seq, chunk, skip_tail=False):
        """
        seq=[1, 2, 5, 8, 555, 100000, 'xxxxx']  chunk=3
        result: [[1, 2, 5], [8, 555, 100000], ['xxxxx']]
        # --------------------
        seq=  "123456789abcdefghijAAAAHFRGЫРГОП лоилоилди"  chunk=4
        result: ['12345', '6789a', 'bcdef', 'ghijA', 'AAAHF', 'RGЫРГ', 'ОП ло', 'илоил', 'ди']
        """
        lst = []
        if chunk <= len(seq):
            lst.extend([seq[:chunk]])
            lst.extend(Re_find.split_list(seq[chunk:], chunk, skip_tail))  # Recurs
        elif not skip_tail and seq:
            # chunk>len(seq) skip_tail=Fals
            lst.extend([seq])
        return lst

    # @staticmethod
    # def list_findall_HARD(my_text: str, my_list: list) -> list:
    #     """Ищем все "Чистые(без вхождений в другие слова)" слова
    #     из списка my_list  в тексте my_text (без учета регистра)
    #     "один один-один одиночка" ['один'] => один
    #     """
    #     temp_list = Re_find.split_list(my_list, 2, False)  # False !!!!
    #     """
    #     обходим возможный сбой на pattern for ref
    #     ['FAG', 'KOYO', 'NTN', 'SKF', 'NSK', 'ASAHI', 'Timken', 'Craft', 'MPZ']
    #     to if 4
    #     [['FAG', 'KOYO', 'NTN', 'SKF'], ['NSK', 'ASAHI', 'Timken', 'Craft'], ['MPZ']]
    #     """
    #     rezult = []
    #     for values in temp_list:
    #         keys = [w.strip() for w in values]
    #         ll = [rf'(\s|\b^)(?P<word>{k})(?=\s)' for k in keys]  # rf !!!!!
    #         """ \b^ - в начале строки   """
    #         patt_re = f"{'|'.join(ll)}"
    #         for match in list(re.finditer(patt_re, my_text, re.IGNORECASE)):
    #             print("-----", values, match)
    #             for groupNum in range(0, len(match.groups())):
    #                 groupNum = groupNum + 1
    #                 print('          ',groupNum ,match,  match.group(groupNum))
    #                 print(match.group('word'))
    #             rezult.append([match.group(2), match.span(2)])
    #     return rezult
    @staticmethod
    def selection_initial(my_text: str, my_list: list) -> list:
        # В лоб если 300 элементов в my_list а текст всего 100 слов
        # отберем нужные для анализа
        # можно и просто искать
        temp = my_text.lower()
        return [w for w in my_list if w.lower() in temp]

    def list_findall_HARD(my_text: str, my_list: list) -> list:
        """Ищем все "Чистые(без вхождений в другие слова)" слова
        из списка my_list  в тексте my_text (без учета регистра)
        "один один-один одиночка" ['один'] => один
        """
        rezult = []
        for key in Re_find.selection_initial(my_text, my_list):
            patt_re = rf"(\s|\b^)(?P<word>{key})(?=\s)"
            for match in list(re.finditer(patt_re, my_text, re.IGNORECASE)):
                rezult.append([match.group('word'), (match.start('word'), match.end('word'),)])
        return rezult

    @staticmethod
    def list_findall(my_text, my_list: list):  # TODO сохр ключ для Spirit
        "если входит но не чистый 333SKF, 4SKF, reSKF-4 но SKF не войдёт"
        temp_list = Re_find.split_list(my_list, 4, False)  # False !!!!
        """
        обходим возможный сбой на pattern for ref
        ['FAG', 'KOYO', 'NTN', 'SKF', 'NSK', 'ASAHI', 'Timken', 'Craft', 'MPZ']
        to if 4
        [['FAG', 'KOYO', 'NTN', 'SKF'], ['NSK', 'ASAHI', 'Timken', 'Craft'], ['MPZ']]
        """
        rezult = []
        for key in Re_find.selection_initial(my_text, my_list):
            p0 = fr"\b[^\s.]+{key}"  # rf !!!!!
            p1 = fr"\b{key}[^\s.]+"  # rf !!!!!
            p2 = fr"\b[^\s.]+{key}[^\s.]+"  # rf !!!!!
            patt_re = f"{p0}|{p1}|{p2}"

            for match in re.finditer(patt_re, my_text, re.IGNORECASE):
                rezult.append([match.group(0), match.span(0)])
        return rezult

    @staticmethod
    def number_find(text):
        patt_re = "([0-9]*[.,]?[0-9]*[0-9^])"
        rezult = []
        for el in list(re.finditer(patt_re, text)):
            rezult.append([el.group(0), el.span(0)])
        return rezult


# =========================================================
#
# =========================================================

class Anakonda(object):

    def __init__(self, s: str):
        self.s = self.text_clear(s)

    def __control__(self, s, key: str):
        text = self.s if s is None else s
        if text is None:
            ValueError(f'@6554 {key}')  # TODO
        return text

    @staticmethod
    def text_clear(s: str) -> str:
        s = s.replace('\n', ' ')
        # s = s.replace('. ', ' . ')  # для слов в конце предл-я
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    @staticmethod
    def rus_or_lat(s: str):
        rus, space, lat, other = 0, 0, 0, 0
        for b in s.lower():
            if b in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                rus += 1
            elif b == ' ':
                space += 1
            elif b in "abcdefghijklmnopqrstuvwxyz":
                lat += 1
            else:
                other += 1
        # print(len(s), rus, lat, space, other, len(s.split(' ')))
        if not rus:
            return False
        if not lat:
            return True
        if (rus - lat) / rus > 0.2:
            return True
        return False

    def FindInList(self, values: list,
                   key: Union[str, None],
                   s: Union[str, None] = None):
        text = self.__control__(s, 'def FindInList')
        t = [Spirit(el[0], el[1], key) for el in Re_find.list_findall(text, values)]
        return t

    def FindInListHard(self, values: list, key: Union[str, None], s: Union[str, None] = None):
        text = self.__control__(s, 'def FindInList')
        t = [Spirit(el[0], el[1], key) for el in Re_find.list_findall_HARD(text, values)]
        return t

    def mix_words_re(self, key: Union[str, None], s: Union[str, None] = None):
        text = self.__control__(s, 'def mix_words_re')
        """
        patt_re = r"([a-zA-Z]+[-\/\\]?[0-9]+[\S]*|[0-9]+[-\/\\]?[a-zA-Z]+[\S]*)"
        """
        patt_re = r"([a-zA-Z]+[\-\/\\]?[0-9]+[\S]*|[0-9]+[\-\/\\]?[a-zA-Z]+[\S]*)"
        patt_re = r"([a-zA-Z]+[\-\/\\]?[0-9]+[\S]*|[0-9]+([-\/\\]?[0-9a-zA-Z]+)[\S]+)"
        ll = []
        for i, el in enumerate(list(re.finditer(patt_re, text))):
            temp = Re_find.number_find(el.group(0))
            if len(temp) == 1 and temp[0][0] == el.group(0):
                # это просто число
                continue

            ll.append(Spirit(el.group(0), el.span(0), key))
        return ll

    def NUMB(self, s: Union[str, None] = None):
        text = self.__control__(s, 'def NUMB')
        patt_re = "([0-9]*[.,]?[0-9]*[0-9^])"
        ll = []
        for el in list(re.finditer(patt_re, text)):
            ll.append(SpiritNumeric(el.group(0), el.span(0), 'Num'))
        return ll

    def numb_lat_spirit(self, s: Union[str, None] = None):
        text = self.__control__(s, 'def NUMB')
        return [SpiritNumericLat(el[0], el[1], el[2]) for el in FUNC(text)]

    def termin_ru_spirit(self, term: str, s: Union[str, None] = None):
        """ spir_term =[]
            for t in ['подшипн','узел']:
                spir_term.extend(parser.termin_ru_spirit(t))"""

        text = self.__control__(s, 'def termin_ru_spirit')
        patt_re = fr"\b\{term}[.а-яёА-ЯЁ]*\b"
        ll = list(re.finditer(patt_re, text, re.IGNORECASE))
        return [Spirit(el.group(0), el.span(0), f'Term {term}') for el in ll]

    @staticmethod
    def __thing_ru_patt__():
        ddd = r"([0-9]*[.,]?[0-9]*[0-9^])"
        # a = fr"[\s\(\[]+({ddd}[-\s]*\шт[.а-яёА-ЯЁ]*)"
        a = r"[\s\(\[](([0-9]*[.,]?[0-9]*[0-9^])[-\s]*\шт[.а-яёА-ЯЁ]*)[\)\]]?"
        b = fr"[\s]?[\(\[]?(шт[.а-яёА-ЯЁ]*[-\s]*{ddd})[\s\)\]]"
        patt_re = fr"({a}|{b})"
        return patt_re

    # def thing_ru(self, s=None):
    #     text = self.s if s is None else s
    #     if text is None:
    #         ValueError('@6554')  # TODO
    #
    #     # ------------------------------------------------
    #     patt_re = Anakonda.__thing_ru_patt__()
    #     rezult = []
    #     for el in re.findall(patt_re, text, re.IGNORECASE):
    #         kol = el[4] if el[2] == '' else el[2]
    #         rezult.append([el[0], kol])
    #     return rezult

    def thing_ru_spirit(self, s: Union[str, None] = None):
        text = self.s if s is None else s
        if text is None:
            ValueError('@6554')  # TODO

        ll = []
        patt_re = Anakonda.__thing_ru_patt__()
        for el in re.finditer(patt_re, text, re.IGNORECASE):
            kol = el[3] if el[5] is None else el[5]
            ll.append(SpiritThing(el.group(0), el.span(0), kol))
        return ll

    def thing_lat_spirit(self, s: Union[str, None] = None):
        """англ штуки """
        text = self.__control__(s, 'def thing_lat_spirit')

        # REF:https://stackoverflow.com/questions/21124256/regular-expression-get-computer-specs-from-plain-text
        ddd = "([0-9]*[.,]?[0-9]*[0-9^])"
        patt_re = fr"({ddd}*[-\s]*[pP][cC][sS])"
        ll = []
        for el in re.finditer(patt_re, text):
            kol = el[2]
            ll.append(SpiritThing(el.group(0), el.span(0), kol=el[2]))
        return ll


# ===========================================================================
#
# ===========================================================================

def EXAMPLE(my_text):
    print(my_text)
    print("------------- Попытка разбора ----------------------------")
    parser = Anakonda(my_text)
    print(f"RUS text: {parser.rus_or_lat(parser.s)} ")
    # ------------- common -----------------------------------------
    # common
    firma_name = ['ASAHI', 'SKF', 'FAG', 'Timken']
    spir_fh = parser.FindInListHard(firma_name, ['Firma', 170])
    spir_f = parser.FindInList(firma_name, ['?Firma?', 30])
    print('Ищем:', firma_name)
    print(' spir_f hard', spir_fh)
    print(' spir_f ????', spir_f)
    # ----------------------------------------------------------
    vendor_code = ['GEZ500ES', '6305-2RS1/C3', 'UCF X20']
    spir_arth = parser.FindInListHard(vendor_code, ['Art.', 170])
    spir_artq = parser.FindInList(vendor_code, 'Art.?')
    print('Ищем:', vendor_code)
    print(' spir_artq hard:', spir_arth)
    print(' spir_artq ????:', spir_arth)
    # ----------------------------------------------------------
    spir_mix: list = parser.mix_words_re(['Mix', 60])
    print('spir_mix', spir_mix)

    spir_numb = parser.NUMB()

    # ===============================================
    spir_numb_lat, spir_thing_lat = [], []
    spir_term, spir_thing_ru = [], []
    if parser.rus_or_lat(parser.s):
        spir_thing_ru = parser.thing_ru_spirit()
        print(f'spir_thing_ru [шт] {spir_thing_ru}')

        terms = ['подшипн', 'узел']
        spir_term = []
        for t in terms:  # Todo промеж выриант termin_ru_spirit
            spir_term.extend(parser.termin_ru_spirit(t))
        print('Ищем:', terms)
        print(f' spir_term:{spir_term}')

    else:

        spir_numb_lat = parser.numb_lat_spirit()
        spir_thing_lat = parser.thing_lat_spirit()

        print('thing_lat_spirit:', parser.thing_lat_spirit())
        for query in ['+31 (0)165 722 011', '+310000 165 722 011']:
            rez = Re_find.selection_initial(parser.s, [query])
            print(f'Ищем {query}   {bool(len(rez))}')

    # -----------------------------------------------------------------
    print('!!! ВВЕДИ ЧИСЛО И НАЖМИ ENTER ДЛЯ ПРОДОЛЖЕНИЯ (В ОКНЕ ВЫВОДА)')
    _ = input()
    print("------------- Структура текста ----------------------------")
    sp_l = [spir_f, spir_fh, spir_arth, spir_artq, spir_term, spir_thing_ru,
            spir_thing_lat, spir_mix, spir_numb_lat, spir_numb, ]

    bb = [[b, []] for i, b in enumerate(parser.s)]
    for spirits in sp_l:  # OR ????   # spirits=listmerge(sp_l)
        for el in spirits:
            _ = [bb[i][1].append(el) for i in el.get_pos()]
    # ================================
    for i, item in enumerate(bb):
        a = max(item[1]) if isinstance(item[1], list) and len(item[1]) else item[1]
        item[1].sort(reverse=True)
        print(f'{i:<4} {item[0]} -> {item[1]}')


if __name__ == '__main__':
    my_text_ru = """
        Прoсим сообщить наличие подшипников SKF 6305-2RS1/C3 (10шт).
Возможена замена на аналог (Timken, FAG, Asah1)
Интересуют манжеты 788VVV2  шт 200.
Узел подшипниковый ASAHI UCF X20 шт 30
Узел подшипниковый FYJ 100 TF SKF      
Сообшите возможную цену для GEZ500ES - 50шт
"""

    my_text_lat = """
GEZ500ES SKF 2.0pcs in stock of 4 pcs requested, additional 1 pc expected to be available 19/12/2022. 
Product quantity price total
GEZ500ES SKF 1 604,8156 604,82
GEZ500ES SKF 2 604,8156 1.209,63
total ex VAT 1.814,45
Shipping
Delivery at Laagrimees OÜ Tatari 58 , 10134, Tallinn, Estonia. Total weight about 50,63 KG
UPS Standard On Request 66,40
UPS Express Saver On Request 254,10
Pick-up at ABF  Pick-up on business days from 8:30 to 17:59 (CET) FREE
Bart van Oevelen
Product Manager
+31 (0)165 722 011
Matilda Hahn
Account Manager
+31 (0)165 722 607
Jonas Fertig
Region Manager
+31 (0)165 235 302
"""

    _ = 1
    if _ == 1:
        EXAMPLE(my_text_ru)
    else:
        EXAMPLE(my_text_lat)
