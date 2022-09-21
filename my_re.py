# -*- coding: utf-8 -*-

import re


# ============================================================
#
# ============================================================

class Cyrilic(object):
    """
    a = Cyrilic.cyrillic_only(my_words)

    """

    @staticmethod
    def cyrillic_only(words):
        # если входят только русские буквы
        p = re.compile("[а-яёА-ЯЁ]+")
        # Функция fullmatch() модуля re вернет объект сопоставления,
        # если вся строка string соответствует шаблону регулярного выражения pattern
        flag = False if p.fullmatch(words) is None else True
        return flag

    @staticmethod
    def cyrillic_has(words):
        # есть русские буквы
        return bool(re.search('[а-яёА-ЯЁ]', words))

    @staticmethod
    def cyrillic_no(words):
        # нет русских букв
        return not bool(re.search('[а-яёА-ЯЁ]', words))

    @staticmethod
    def cyrillic_only_get(words) -> list:
        # список русских букв в слове
        p = re.compile("[а-яёА-ЯЁ]")
        russian = [w for w in filter(p.match, words)]
        # russian - список только русских букв
        return russian

    @staticmethod
    def mix(words):
        # это смесь
        if not Cyrilic.cyrillic_only(words) and Cyrilic.cyrillic_has(words):
            return True
        return False

    def split(new_text, pattern=' '):
        top, bottoms = new_text, []

        p = re.compile(f'({pattern})', re.I)
        iterator = p.finditer(new_text)
        xxx = [match.span() for match in iterator]
        # ref examp [(124, 135), (343, 354), (429, 440)]
        if len(xxx) > 0:
            ll = [el[0] for el in xxx]
            ll.reverse()  # ref examp [429, 343, 124]
            for end_pos in ll:
                top, end = top[:end_pos], top[end_pos:]
                bottoms.append(end)
            bottoms.reverse()
            # clear
            text = re.sub(" +", " ", top)
            top = '' if text == ' ' else top
        return top, bottoms

    @staticmethod
    def word_spliter(txt):
        """
        print(re.split(r'\W+', 'Где, скажите мне, мои очки??!'))
        # -> ['Где', 'скажите', 'мне', 'мои', 'очки', '']
        """
        return re.split(r'\W+', txt)
