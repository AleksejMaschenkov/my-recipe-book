# -*- coding: utf-8 -*-

"""
Поиск информации по тексту
"""

import functools
import re

from typing import Union


# ============================================================
#
# ============================================================
class Filtr(object):
    df = {}  # dict for function

    def __init__(self, d: Union[dict, None] = None):
        self.__temp__ = None
        if d is not None:
            self.df = d

    @property
    def value(self):
        return self.__temp__

    def run(self, text):
        self.__temp__ = {key: run(text) for key, run in self.df.items()}
        return self.__temp__

    def all(self, text=None):
        """  Перевычисляет при необходимости.
            Проверяет, что все элементы в последовательности True
        """
        if text is None and self.__temp__ is None:
            raise ValueError('No required data')  # TODO or return None ???
        if text is not None or self.__temp__ is None:
            self.run(text)
        if self.value is None:
            raise ValueError('value is None')
        return all(self.value)


# ============================================================
#
# ============================================================
def toListOrFalse():
    """ДЕКОРАТОР"""

    def _output_(fn):
        """:return False or List. if len(..)==0 return False """

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            data = fn(*args, **kwargs)
            # for the sake of this (ради этого)
            if isinstance(data, list) and len(data) > 0:
                return data
            return False

        return wrapper

    return _output_


def split_str(seq:Union[str,list], chunk:int, skip_tail=False):
    """
    seq=[1, 2, 5, 8, 555, 100000, 'xxxxx']
    chunk=3
    result: [[1, 2, 5], [8, 555, 100000], ['xxxxx']]


    seq=  "123456789abcdefghijAAAAHFRGЫРГОП лоилоилди"
    chunk=3
    result: ['12345', '6789a', 'bcdef', 'ghijA', 'AAAHF', 'RGЫРГ', 'ОП ло', 'илоил', 'ди']

    """
    lst = []
    if chunk <= len(seq):
        lst.extend([seq[:chunk]])
        lst.extend(split_str(seq[chunk:], chunk, skip_tail))  # Recurs
    elif not skip_tail and seq:
        # chunk>len(seq) skip_tail=False
        lst.extend([seq])
    return lst


# ============================================================
#
# ============================================================


class Mixture(object):

    @staticmethod
    def words_spliter_py(s: str) -> list:  # TODO протестировать время и тд
        s = s.replace('\n', ' ')
        s = s.replace('. ', ' . ')  # для слов в конце предл-я
        while "  " in s:
            s = s.replace("  ", " ")
        """REF: s = '    ' >>> ll = s.split(' ') >>> ll is ['', '', '', '', ''] """
        return [w for w in s.split(' ') if not w == '']

    @staticmethod
    def cyrillic_has(words):
        # есть русские буквы
        return bool(re.search('[а-яёА-ЯЁ]', words))

    @staticmethod
    def latin_has(words):
        # есть латинские буквы
        return bool(re.search('[A-Za-z]', words))

    @staticmethod
    def number_has(words):
        # есть цифры
        return bool(re.search('[0-9]', words))

    @staticmethod
    def cyrilic_bad(word):
        #   а цифры ????
        f = Mixture.cyrillic_has(word) and Mixture.latin_has(word)
        return f

    @staticmethod
    def podgot(my_text: Union[str, list]):
        if isinstance(my_text, list):
            return my_text
        elif isinstance(my_text, str):
            return Mixture.words_spliter_py(my_text)  # !!!
        else:
            raise Exception('BAD type(my_text)')

    @staticmethod
    def is_mix(my_text: Union[str, list], var: int = 0):
        """Смесь латинских букв и цифр"""
        ll = Mixture.podgot(my_text)

        # -----------------------------------------------------
        if var == 0:
            return [item for item in ll if Mixture.number_has(item) and Mixture.latin_has(item)]
        elif var == 1:
            return [item for item in ll if Mixture.cyrilic_bad(item)]
        else:
            raise Exception('BAD var')

    @staticmethod
    def get_dog(my_text: Union[str, list], clear_tail: bool = False):
        words = Mixture.podgot(my_text)
        ll = [w for w in words if '@' in w]
        if clear_tail:
            return [w[:-1] for w in ll if w[-1] in ['.', ',', ';']]
        return ll


# ============================================================
# ============================================================
class Re_Common(object):

    @staticmethod
    def my_findall(text, patt):
        return re.compile(patt).findall(text) if isinstance(text, str) else False

    @staticmethod
    def __clear__(s: str):
        """in one line (no spaces or newlines)"""
        s = s.replace('\n', ' ')
        while "  " in s:
            s = s.replace("  ", "")
        return s

    @staticmethod
    def word_spliter_re(txt):
        """
        print(re.split(r'\W+', 'Где, скажите мне, мои очки??! ))
        # -> ['Где', 'скажите', 'мне', 'мои', 'очки', '']
                  !!!     6305-2RS1/C3 тоже разбило
        """
        return re.split(r'\W+', txt)

    @staticmethod
    def words_spliter_py(s: str) -> list:  # TODO протестировать время и тд
        s = s.replace('\n', ' ')
        s = s.replace('. ', ' . ')  # для слов в конце предл-я
        while "  " in s:
            s = s.replace("  ", " ")

        # if s=='' or s ==' ' or s = '    '
        """
        s = '    ' >>> ll = s.split(' ') >>> ll is ['', '', '', '', '']
        """
        return [w for w in s.split(' ') if not w == '']

    @staticmethod
    def list_findall(my_text, my_list: list):
        temp_list = split_str(my_list, 4, False)  # False !!!!
        """
        обходим возможный сбой на pattern for ref
        ['FAG', 'KOYO', 'NTN', 'SKF', 'NSK', 'ASAHI', 'Timken', 'Craft', 'MPZ']
        to if 4
        [['FAG', 'KOYO', 'NTN', 'SKF'], ['NSK', 'ASAHI', 'Timken', 'Craft'], ['MPZ']]
        """
        rezult = []
        for values in temp_list:
            ll = [w.lower() for w in values]
            """ ??? без lower вырубалось на \F r'\FAG|Timken|KOYO|NTN|SKF' """
            first = f"^{'|^'.join(ll)}"
            vezde = "|".join(ll)
            pattern = f"\{first}|{vezde}"
            # REF example: pattern = r"\^timken|^craft|timken|craft"
            __ = re.compile(pattern, re.IGNORECASE).findall(my_text)
            rezult.extend(__)
        return rezult

    @staticmethod
    def _perebor(part_words: list, words: Union[list, str]) -> list:
        """Текст переводим в слова. И далее поиск слов куда могут входить элементы из temp"""
        part_words = list(set(part_words))  # выкидываем повторы
        if not len(part_words):
            return []
        if isinstance(words, str):
            words = Re_Common.word_spliter_re(words)
        rezult = []
        for part in part_words:
            _ = [word for word in words if part in word]
            rezult.append((part, _))
        return rezult

    """
    def split_with_separators(regex, txt:str):
        # ref regex = re.compile(f'({key})', re.I)
        return list(filter(None, regex.split(txt)))
    """

    @staticmethod
    def split_modif(key: str, _text: str, ):  # TODO rename
        # key='(с уважением)'
        regex = re.compile(f'({key})', re.I)
        s = list(filter(None, regex.split(_text)))
        # _text = 'С уважением Иванов С уважением xxxx'
        # s= ['С уважением',' Иванов','С уважением', 'xxxx']
        # создадим список ['С уважением Иванов','С уважением xxxx']
        return [s[i] + s[i + 1] for i in range(0, len(s), 2)]

    @staticmethod
    def obrazec(my_text, keys: [list, str], strip: bool = False):
        """
        l = re.findall(' подшип.+? |^подшип.+? ', my_text, re.IGNORECASE)
        пробелы ВАЖНЫ
        [' подшипников ', ' подшипники ', ' подшипников, ']

        сразу по всем ключам
        """

        if isinstance(keys, list):
            keys: list = list(set(keys))  # for duplicat
        elif isinstance(keys, str):
            keys = [keys]
        else:
            raise Exception('Bad type(keys) no in[list,str]')

        my_list = [f' {key}.+? |^{key}.+? ' for key in keys]
        pattern = '|'.join(my_list).lower()
        ll = re.findall(pattern, my_text, re.IGNORECASE)
        data = [s.strip() for s in ll] if strip else ll
        return data

    @staticmethod
    def obrazec_as_dict(my_text, keys: [list, str], strip: bool = False):
        if not isinstance(keys, list):
            raise  # no list
        # words = Re_Common.words_spliter_py(my_text)
        ll = [{k: Re_Common.obrazec(my_text, k)} for k in keys]
        if strip:
            for my_dict in ll:
                for k, items in my_dict.items():
                    my_dict[k] = [s.strip() for s in items]
        return ll

    @staticmethod
    def obrazec_as_dict_py(my_text, keys: [list, str], strip: bool = False):
        if isinstance(keys, str):
            keys = [keys]
        if isinstance(keys, list) and len(keys):
            words = Re_Common.words_spliter_py(my_text)
            return [{patt: [w for w in words if patt in w]} for patt in keys]
        # TODO oytput info
        return []

    # ------------------------------------------------------------------
    @staticmethod
    def word_dog_fidall(text):
        """возможно email - (примитивный поиск без валидации)"""
        return re.findall(r'\S+@\S+', text)  # !!!!

    @staticmethod
    def inn_findall(my_text):
        """
             ИНН (в России) бывает 10-значный (у юрлиц)
             или 12-значный (у физлиц)
        """
        pattern = r"\d{12}|\d{10}"
        return Re_Common.my_findall(my_text, pattern)

    @staticmethod
    def PostKodeRU(my_text):
        """В России все просто: шесть цифр подряд без разделителей"""
        # pattern = r"^\b\d{6}\b"
        pattern = r"\b\d{6}\b"
        return Re_Common.my_findall(my_text, pattern)


# ============================================================


# ============================================================
#
# ============================================================


class SISTEMA(object):
    l_firma = ['FAG', 'KOYO', 'NTN', 'SKF', 'NSK', 'ASAHI']
    l_key = ['подшипн', 'Твер', '6305-2RS1/C3', 'Timken']

    #
    def __init__(self, manufacturer=None):
        if manufacturer is not None:
            self.l_firma = manufacturer
        self.text_by_word = []
        self.my_findall = Re_Common.my_findall

    # -----------------------------------------------------------

    @toListOrFalse()
    def INN(self, my_text):
        return Re_Common.inn_findall(my_text)

    @toListOrFalse()
    def Email(self, text):
        return Mixture.get_dog(text, clear_tail=True)
        return Re_Common.word_dog_fidall(text)

    @toListOrFalse()
    def PostKodeRU(self, my_text):
        return Re_Common.PostKodeRU(my_text)

    @toListOrFalse()
    def Mix(self, my_text: str):  # TODO
        """Смесь латинских букв и цифр"""
        return Mixture.is_mix(my_text)

    # -----------------------------------------------------------
    @toListOrFalse()
    def CyrilicBad(self, my_text):
        return Mixture.is_mix(my_text, 1)

    @toListOrFalse()
    def SitySearch(self, my_text):
        """Ищем текст от "г." до ДАЛЬНЕЙ(<?>) запятой.
        SRC: https://www.planetaexcel.ru/techniques/7/4844/

        ['г.Орёл,','г. Курск,','г. Курск  ,','г. нижний новгород,'] -TRUE """
        return self.my_findall(my_text, r"г\..*?,")

    @toListOrFalse()
    def SitySearch1(self, my_text):
        """Ищем текст от "г." до точки. Examp: ['г.Орёл .'] -TRUE
        SRC: https://www.planetaexcel.ru/techniques/7/4844/
        """
        return self.my_findall(my_text, r"г\..*.")

    @toListOrFalse()
    def Firma(self, my_text):
        return Re_Common.list_findall(my_text, self.l_firma)

    @toListOrFalse()
    def KEY(self, my_text):
        keys: list = list(set(self.l_key))  # for duplicat
        if 1:
            return Re_Common.obrazec_as_dict_py(my_text, keys)
        else:
            # НЕ ИЩЕТ '6305-2RS1/C3'
            part_list = Re_Common.list_findall(my_text, keys)
            return Re_Common._perebor(part_list, my_text) if part_list else []


# ==================================================================

def Podval(text: str):
    """Разбиваем text по ключу 'с уважением'
    txt = 'Часть 1. С уважением Иванов С уважением xxxx'
    :return ['Часть 1',['С уважением Иванов','С уважением xxxx']]
    """
    text_lower: str = text.lower()
    if 'уважен' in text_lower:
        zz = text_lower.split('с уважением', maxsplit=-1)
        # !!! а если встретится 'с     уважением' -> не сработает
        # zz = text_lower.partition('с уважением') #говорят быстрее
        if len(zz) == 1:
            return text, []
        elif len(zz) == 2:
            pos = len(zz[0])
            return text[:pos], [text[pos:]]
        else:
            pos = len(zz[0])
            top_text, bottom_text = text[:pos], text[pos:]
            return top_text, Re_Common.split_modif('с уважением', bottom_text)


# ============================================================
#                   MAIN (EXAMPLE AND TEST)
# ============================================================


if __name__ == '__main__':
    mail_text_src = """
        ПрOсим сообщить наличий подшипников SKF 6305-2RS1/C3 (20шт).
        Возможена замена на аналог Timken(Asahi) .  
        [ гТвер  6305-2RS1/C32222  ффффkoyo  ]
        
        Можете ли вы поставить их в г.Москву 170010.
        Сообщите можете ли поставить подшипники маломагнитные 
           С уважением Иванов Иван Иваныч инн 1770000009 АО"Сокол", 
        170009 г. Тверь, ул. Победы   
        с уважением ivanov@mail.ru, 
    """
    print(mail_text_src)


    def example(mail_text):
        #  create a list of manufacturers [append]
        my_firma = SISTEMA.l_firma.extend(['Timken', 'Craft', 'MPZ'])
        #  and analizator
        ReSHATEL = SISTEMA(my_firma)
        # ========================================================
        query = {
            'mix(?kod)': ReSHATEL.Mix,
            'firma': ReSHATEL.Firma,
            'inn': ReSHATEL.INN,
            'sity': ReSHATEL.SitySearch,
            'sity1': ReSHATEL.SitySearch1,
            'for analiz email': ReSHATEL.Email,
            'postkodeRU': ReSHATEL.PostKodeRU,
            'special_word': ReSHATEL.KEY,
            'LatinAndCyrilic': ReSHATEL.CyrilicBad,
            'Podval': Podval,
        }

        my_filtr = Filtr(query)
        rezult: dict = my_filtr.run(mail_text)
        return rezult


    print('============= начинаем анализ =====================')
    rezult = example(mail_text_src)

    # ============= output  ===================================
    for key, value in rezult.items():
        print(f'{key:30} {value}')

    print('========== Разбор на инфо блоки ===================')
    razdel = rezult.get('Podval')
    top, bottom = razdel[0], razdel[1]
    print(top)
    for txt in bottom:
        print(f'{10 * "-":^20}')
        print(txt)

    # =======================================================
"""
============= начинаем анализ =====================
mix(?kod)                      ['6305-2RS1/C3', '6305-2RS1/C32222]']
firma                          ['SKF', 'koyo', 'Timken', 'Asahi']
inn                            ['1770000009']
sity                           ['г. Тверь,']
sity1                          ['г.Москву 170010.', 'г. Тверь, ул. Победы   ']
for analiz email               ['ivanov@mail.ru']
postkodeRU                     ['170010', '170009']
special_word                   [{'6305-2RS1/C3': ['6305-2RS1/C3', '6305-2RS1/C32222]']}, {'Timken': ['Timken']}, {'подшипн': ['подшипников', 'подшипники']}, {'Твер': ['eТвер', 'Тверь,']}]
LatinAndCyrilic                ['Прoсим', 'ффффkoyo', 'eТвер']
Podval     .......
.....................................                    
"""
