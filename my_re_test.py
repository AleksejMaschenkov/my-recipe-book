# -*- coding: utf-8 -*-


import timeit
import my_re


# ============================================================
#       EXAMPLE timeit And test my_re
# ============================================================


def cyrillic_only(string: str):
    # если входят только  русские буквы и ""," "
    txt = string.lower()
    rus_letters = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л",
                   "м", "н", "о", "п", "р", "с", "т",
                   "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я",
                   "", " "]

    return all([i in rus_letters for i in txt])


def cyrillic_has_1(text):
    # если входит хоть одна русская буква
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


# ============================================================
#
# ============================================================
lll = ['ёлка',
       'test', 'testя', 'тест',
       '123Ы', '', ' ',
       'частнопредпринимательский',
       'частнопредприниматель1ский',
       ]


def info(ll):
    for i, item in enumerate(ll):
        print(i, 'analiz:', item)
        print(f'my_re.check_str({item}) ->', cyrillic_only(item))
        print(f'my_re.has_cyrillic1({item}) ->', cyrillic_has_1(item))
        print(f'Cyrilic.cyrillic_only({item}) ->', my_re.Cyrilic.cyrillic_only(item))
        print(f'Cyrilic.cyrillic_has({item}) ->', my_re.Cyrilic.cyrillic_has(item))
        print(f'Cyrilic.cyrillic_no({item}) ->', my_re.Cyrilic.cyrillic_no(item))
        print(f'Cyrilic.mix({item}) ->', my_re.Cyrilic.mix(item))
        a = my_re.Cyrilic.cyrillic_only_get(item)
        print(f'Cyrilic.cyrillic_only_get({item}) ->', a)
        print('--------------------------------------')


# ============================================================
#
# ============================================================
def my_re_cyrillic_only(ll):
    for i, item in enumerate(ll):
        a = cyrillic_only(item)


def my_re_cyrillic_has_1():
    ll = lll
    for i, item in enumerate(ll):
        a = cyrillic_has_1(item)


def test_speed_main():
    for func in ["my_re_cyrillic_only(lll)", "my_re_cyrillic_has_1()"]:
        print(func, timeit.timeit(func, number=10000, globals=globals()))
    print('--')
    print('my_re.cyrillic_only', timeit.timeit("my_re_cyrillic_only(lll)",
                                               number=10000,
                                               setup="from __main__ import my_re_cyrillic_only, lll"))


# ============================================================
#
# ============================================================
def test_sped_def():
    """ПРИМЕР ЗАМЕРА - всё в этой функции"""

    # =========================================
    ll_local = lll.copy()

    # or example ll_local = ['Ёжик','test','яtest','123Ы']

    def test_01(ll: list):
        for i, item in enumerate(ll):
            a = my_re.Cyrilic.cyrillic_only(item)

    def test_02(ll: list):
        for i, item in enumerate(ll):
            a = my_re.Cyrilic.cyrillic_has(item)

    def test_03(ll: list):
        for i, item in enumerate(ll):
            a = my_re.Cyrilic.cyrillic_no(item)

    def test_04(ll: list):
        for i, item in enumerate(ll):
            a = my_re.Cyrilic.mix(item)

    def test_cyrillic_only_get(ll: list):
        for i, item in enumerate(ll):
            a = my_re.Cyrilic.cyrillic_only_get(item)

    # ---------------------------------------------------------
    def wrapper(func, *args, **kwargs):
        def wrapper():
            return func(*args, **kwargs)

        return wrapper

    # ---------------------------------------------------------
    for txt, func in [('Cyrilic.cyrillic_only   ', wrapper(test_01, ll_local)),
                      ('Cyrilic.cyrillic_has     ', wrapper(test_02, ll_local)),
                      ('Cyrilic.cyrillic_no      ', wrapper(test_03, ll_local)),
                      ('Cyrilic.mix              ', wrapper(test_04, ll_local)),
                      ('Cyrilic.cyrillic_only_get', wrapper(test_cyrillic_only_get, ll_local))
                      ]:
        print(txt, timeit.timeit(func, number=10000))


# ============================================================
# ============================================================

text3 = """                
Добрый день!Прошу Кп на направляющие THK1) shs15   2) shs253)  shs35  по 2 м - 1 шт или по метру - 2 шт 
каждой
    С уважением к Вам и Вашему делу !-- Смирнов Егор  
E-mail:egor@stalp.ruООО  "Сталь-Подшипник", 196105, г. Санкт-Петербург, проспект Юрия Гагарина, дом № 2, 
этаж 8, офис 12Т/ф 336-23-50,Т.м.
+7 921-564-8988 Т. 986-36-54.с уважением Поставки отечественных и импортных подшипников, уплотнений, ремней, цепей
с уважением"""


def test_split(my_text):
    top, bottoms = my_re.Cyrilic.split(my_text, 'с уважением')
    # top, bottoms = examp1(text3)

    print("TOP", top)
    for item in bottoms:
        print("ITOG", item)
    return top


# ============================================================
#
# ============================================================
if __name__ == '__main__':
    print(' STEP 1 EXAMPLE. FUNCTION RESULTS')
    info(lll)
    print(' STEP 1 SPEED')
    test_speed_main()
    print(' STEP 2 SPEED')
    test_sped_def()

    print(' STEP 3  PARSE')
    rez = my_re.Cyrilic.word_spliter(text3)
    print("Cyrilic.word_spliter:", rez)
    test_split(text3)
