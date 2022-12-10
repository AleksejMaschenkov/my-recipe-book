# -*- coding: utf-8 -*-

"""
   Преобразоание json файла FireFox в форму для построения дерева
   Converting a FireFox json file to a form for building a tree

   !!!!!!   json_obj_to_list_gener(json_obj) !!!!!!
"""
import copy
import json
from typing import List


# =============================================================================
#                       GUT FAST
# =============================================================================
def recursive_gen(json_obj):
    """list(recursive_gen(json_obj))"""
    if json_obj is not None:
        if isinstance(json_obj, dict):
            yield json_obj
            yield from recursive_gen(json_obj.get('children'))
        elif isinstance(json_obj, list) and len(json_obj):
            for item in json_obj:
                yield from recursive_gen(item)


def dict_parent(src: list):
    # ------------- step 1 ---------------------------

    def set_parent_id(values: list, lsrc: list) -> dict:
        id_parentid = {row['id']: None for row in lsrc}
        for parent in values:
            children = parent.get('children', [])
            for child in children:
                # set parent id
                id_parentid[child['id']] = parent['id']
        return id_parentid

    by_id = set_parent_id(src, src)
    # -------------- step 2 --------------------------
    """ вычислим родителей и уровень потомка и присвоим значения"""

    def parent_generator_id(i):
        # gives generator, where next is title of parent
        # дает генератор, где следующий id родителя
        while i > 1:
            i = by_id[i]
            yield i

    for item in src:
        parents = list(parent_generator_id(item['id']))
        item['parent'] = parents[0] if len(parents) else None
        item['level'] = len(parents) - 1
        item['children'] = [child['id'] for child in item.get('children', [])]
    return src


def json_obj_to_list_gener(json_obj):
    src = list(recursive_gen(json_obj))
    return dict_parent(src)
  
  
def builder_json_gener(json_nfile: str):
    # БЫСТРЕЕ В 5 раз на малом / на большом(2500) в 20 раз
    with open(json_nfile, 'r', encoding='utf-8') as datafile:
        jdata = json.load(datafile)
    src = json_obj_to_list_gener(jdata)
    return src

# =============================================================================
#
# =============================================================================
def item_all_cpecial(json_input):
    rez = []

    def rez_append(rezult: list, json_obj: dict):
        jscopy = copy.deepcopy(json_obj)
        # заменим объект child в 'children' на его код (
        children = jscopy.get('children', [])
        jscopy['children'] = [child.get('id') for child in children]
        rezult.append(jscopy)

    def recursive(json_obj):
        if isinstance(json_obj, dict):
            key = json_obj.get('id')
            if json_obj.get('parent') is None:
                # create new key 'parent'
                json_obj['parent'] = None
            for child in json_obj.get('children', []):
                child['parent'] = key
            rez_append(rez, json_obj)
            recursive(json_obj.get('children', []))  # Recursion
        elif isinstance(json_obj, list):
            for item in json_obj:
                recursive(item)  # # Recursion

    # ------ run ---------------
    recursive(json_input)
    return rez


def buider_level(src: List) -> List:
    """ вычислим уровень потомка и присвоим его"""
    by_id = {row['id']: row['parent'] for row in src}

    def parent_generator_id(i):
        # gives generator, where next is title of parent
        # дает генератор, где следующий id родителя
        while i > 1:
            i = by_id[i]
            yield i

    def get_level(index):
        return len(list(parent_generator_id(index))) - 1

    for item in src:
        item['level'] = get_level(item['id'])
    return src


def builder_json(json_nfile: str):
    with open(json_nfile, 'r', encoding='utf-8') as datafile:
        jdata = json.load(datafile)
    src = buider_level(item_all_cpecial(jdata))
    return src


# =============================================================================
#
# =============================================================================
def standardize(src: list) -> list:
    """возвращает все записи (словари) с одним набором ключей
       returns all records (dictionaries) with the same set of keys
    """
    keys = ['guid', 'title', 'index', 'dateAdded', 'lastModified', 'id', 'typeCode',
            'type', 'root', 'uri', 'iconUri', 'charset', 'tags', 'keyword', 'postData']
    keys.extend(['level', 'children', 'parent'])

    return [{key: el.get(key) for key in keys} for el in src]


# =============================================================================
#                           __main__  (test)
# =============================================================================


if __name__ == '__main__':

    def example(f_name, exampl=0):
        if exampl:
            rezult = builder_json(f_name)
        else:
            rezult = builder_json_gener(f_name)
        if rezult is not None:
            for row in rezult:
                a, b, c = str(row['parent']), str(row['children']), row['level']
                print(f"paren:{a:>5} children:{b:<20} level:{c:>2} id={row['id']:>3}", row)
        #
        st_rez = standardize(rezult)
        for row in st_rez:
            print(len(row.keys()))


    # ----------------------------------------
    example('test.json', exampl=1)
