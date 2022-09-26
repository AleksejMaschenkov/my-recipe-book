# -*- coding: utf-8 -*-

"""
Поиск информации по тексту

"""

import re
from typing import Union


# ============================================================
#
# ============================================================
class Filtr(object):
    f = {}

    def __init__(self, d: Union[dict, None] = None):
        __temp__ = None
        if d is not None:
            self.f = d

    @property
    def value(self):
        return self.__temp__

    def run(self, text):
        self.__temp__ = {key: run(text) for key, run in self.f.items()}
        return self.__temp__  #

    def all(self, text=None):
        """
        Перевычисляет при необходимости.
        Проверяет, что все элементы в последовательности True"""
        if text is not None:
            self.__temp__ = self.run(text)
        if self.value is None:
            raise ValueError('value is None')
        return all(self.value)


# ============================================================
#
# ============================================================

class SISTEMA(object):
    l_firma = ['FAG', 'KOYO', 'NTN', 'SKF', 'NSK', 'ASAHI']

    def __init__(self, manufacturer=None):
        if manufacturer is not None:
            self.l_firma = manufacturer

    def findall(self, my_str, pattern):
        p = re.compile(pattern)
        return p.findall(my_str)

    def my_output(self, value):
        if isinstance(value, list) and len(value):
            return value
        return False

    def my_findall(self, my_text, pattern):
        if isinstance(my_text, str):
            v = re.compile(pattern).findall(my_text)
            return self.my_output(v)
        return False

    def INN(self, my_text):
        """
             ИНН (в России) бывает 10-значный (у юрлиц)
             или 12-значный (у физлиц)
        """
        pattern = r"\d{12}|\d{10}"
        return self.my_findall(my_text, pattern)

    def PostKodeRU(self, my_text):
        """В России все просто: шесть цифр подряд без разделителей"""
        pattern = r"^\b\d{6}\b"
        pattern = r"\b\d{6}\b"
        return self.my_findall(my_text, pattern)

    def SitySearch(self, my_text):
        # SRC: https://www.planetaexcel.ru/techniques/7/4844/
        """мы ищем текст от "г." до ДАЛЬНЕЙ(<?>) запятой """
        """['г.Орёл,','г. Курск,','г. Курск  ,',"г. нижний новгород,"] -TRUE """
        pattern = r"г\..*?,"
        return self.my_findall(my_text, pattern)

    def SitySearch1(self, my_text):
        # SRC: https://www.planetaexcel.ru/techniques/7/4844/
        """мы ищем текст от "г." до ДАЛЬНЕЙ(<?>) . """
        """['г.Орёл .'] -TRUE """
        pattern = r"г\..*."
        return self.my_findall(my_text, pattern)

    def Firma(self, my_text):
        temp = '|'.join(self.l_firma).lower()
        """ без lower вырубалось на \F r'\FAG|Timken|KOYO|NTN|SKF' """
        pattern = f"\{temp}"
        # pattern = r"\SkF|Timken|KOYO|NTN|FAG"
        p = re.compile(pattern, re.IGNORECASE)
        return self.my_output(p.findall(my_text))

    def Mix(self, my_text: str):
        """Смесь латинских букв и цифр"""
        def cyrillic_has(words):
            # есть русские буквы
            return bool(re.search('[а-яёА-ЯЁ]', words))

        def latin_has(words):
            # есть латинские буквы
            return bool(re.search('[A-Za-z]', words))

        def number_has(words):
            # есть цифры
            return bool(re.search('[0-9]', words))

        my_text = self.__clear__(my_text)
        ll = my_text.split(' ')
        v = [item for item in ll if number_has(item) and latin_has(item)]
        return self.my_output(v)

    @staticmethod
    def __clear__(s: str):
        """in one line (no spaces or newlines)"""
        s = s.replace('\n', ' ')
        while "  " in s:
            s = s.replace("  ", "")
        return s

    @staticmethod
    def word_spliter(txt):
        """
        print(re.split(r'\W+', 'Где, скажите мне, мои очки??!'))
        # -> ['Где', 'скажите', 'мне', 'мои', 'очки', '']
        6305-2RS1/C3 тоже разбило
        """

        return re.split(r'\W+', txt)


# ============================================================
#                   MAIN (EXAMPLE AND TEST)
# ============================================================


if __name__ == '__main__':

    mail_text = """ 
        Просим сообщить наличий подшипников SKF 6305-2RS1/C3 (20шт).
        Возможена замена на аналог Timken.
        Можете ли вы поставить их в г.Москву 1700010.
        С уважением Иванов Иван Иваныч инн 1770000009 АО"Сокол", 
        170009 г. Тверь, ул. Победы 10
    """

    # ========================================================
    #       create a list of manufacturers [append]
    my_firma = SISTEMA.l_firma.extend(['Timken', 'Craft', 'MPZ'])
    #                 and analizator
    ReSHATEL = SISTEMA(my_firma)
    # ========================================================
    query = {
        'mix': ReSHATEL.Mix,
        'firma': ReSHATEL.Firma,
        'inn': ReSHATEL.INN,
        'sity': ReSHATEL.SitySearch,
        'sity1': ReSHATEL.SitySearch1,
        'postkodeRU': ReSHATEL.PostKodeRU,
    }

    my_filtr = Filtr(query)
    rezult:dict = my_filtr.run(mail_text)
    # ============= output  ===================================
    for key, value in rezult.items():
        print(f'{key:30} {value}')

    # =======================================================
    """
    mix                            ['6305-2RS1/C3.']
    firma                          ['SKF', 'Timken']
    inn                            ['1770000009']
    sity                           ['г. Тверь,']
    sity1                          ['г.Москву 1700010.', 'г. Тверь, ул. Победы 10']
    postkodeRU                     ['170009']
    """
