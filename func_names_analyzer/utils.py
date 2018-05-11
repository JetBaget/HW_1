# -*- coding: utf-8 -*-

import os
from collections import Counter


def flat(_list):
    """
    Разворачивает вложенные массивы в один список
    [[1,2], [3,4,5], [6]] -> [1,2,3,4,5,6]

    :param _list:           Список, содержащий вложенные массивы
    :return:                Список элементов вложенных массивов
    """
    return [i for v in _list for i in v]


def find_pyfiles_in_path(inspected_path):
    """
    Возвращает список .py-файлов, найденных рекурсивно в директории dir_path

    :param inspected_path:      Путь к директории, где будет выполняться поиск .py-файлов
    :return:                    list
    """
    pathes_to_pyfiles = []
    for root, dirs, files in os.walk(inspected_path, topdown=True):
        for file in files:
            if not file.endswith('.py'):
                continue
            pathes_to_pyfiles.append(os.path.join(root, file))
            if len(pathes_to_pyfiles) == 100:
                break
    return pathes_to_pyfiles


def split_upper_case_name(name):
    """
    Разбивает название в snake_case на слова

    :param name:            Название в snake_case
    :return:                list
    """
    return [n for n in name.split('_') if n]


def pick_top_from_iterable(iterable, top_size=3):
    """
    Возвращает наиболее часто встречающиеся элементы последовательности.
    Размер выборки задается параметром top_size (по умолчанию равен 5)

    :param iterable:            Объект с поддержкой протокола итератора
    :param top_size:            Объём выборки
    :return:                    Список кортежей
    """
    return Counter(iterable).most_common(top_size)