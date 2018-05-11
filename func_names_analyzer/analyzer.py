# -*- coding: utf-8 -*-

import ast
from nltk import pos_tag

from func_names_analyzer.utils import flat, find_pyfiles_in_path,\
    split_upper_case_name, pick_top_from_iterable


def create_syntax_trees(inspected_path, with_file_names=False, with_file_content=False):
    """
    Возвращает список абстрактных синтаксических деревьев для всех .py файлов,
    содержащихся в указанной директории/поддиректориях.
    В зависимости от значений ключей with_file_names, with_file_content добавляется
    информация об имени файла и его содержимом, соответственно.

    :param inspected_path:              Путь к директории, где будет выполняться поиск .py-файлов
    :param with_file_names:             Флаг, добавляющий название файла
    :param with_file_content:           Флаг, добавляющий содержимое файла
    :return:                            list
    """
    trees = []
    pathes_to_pyfiles = find_pyfiles_in_path(inspected_path)
    for py_file_path in pathes_to_pyfiles:
        with open(py_file_path, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
            tree_data = tree
            if with_file_names and with_file_content:
                tree_data = (py_file_path, main_file_content, tree)
            elif with_file_names:
                tree_data = (py_file_path, tree)
            trees.append(tree_data)
        except SyntaxError:
            pass
    return trees


def get_all_names_from_tree(tree):
    """
    Возвращает список всех имен, содержащихся в синтаксическом дереве

    :param tree:            Объект дерева
    :return:                list
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def check_word_is_verb(word):
    """
    Осуществляет проверку, является ли слово глаголом

    :param word:            Строка
    :return:                boolean
    """
    if not word:
        return False
    pos_info = pos_tag([word])
    return 'VB' in pos_info[0][1]


def extract_verbs_from_function_name(function_name):
    """
    Извлекает из названий функций глаголы

    :param function_name:           Название функции
    :return:                        list
    """
    return [w for w in function_name.split('_') if check_word_is_verb(w)]


def find_all_names_in_repo(repo_path):
    """
    Возвращает все названия, кроме защищенных

    :param repo_path:       Путь к директории с репозиторием
    :return:                list
    """
    trees = create_syntax_trees(repo_path)
    all_names = flat([get_all_names_from_tree(t) for t in trees])
    names = [n for n in all_names if not (n.startswith('__') and n.endswith('__'))]
    return flat([split_upper_case_name(name) for name in names])


def find_func_names_in_repo(repo_path):
    """
    Возвращает все названия функций, кроме защищенных

    :param repo_path:       Путь к директории с репозиторием
    :return:                list
    """
    all_func_nodes = list()
    trees = create_syntax_trees(repo_path)
    for tree in trees:
        all_func_nodes.extend([node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
    func_names = [f for f in all_func_nodes if not (f.startswith('__') and f.endswith('__'))]
    return func_names


def pick_top_func_names(repo_path, top_size=10):
    """
    Делает выборку самых популярных названий функций

    :param repo_path:       Путь к директории с репозиторием
    :param top_size:        Объём выборки
    :return:                list
    """
    func_names = find_func_names_in_repo(repo_path)
    return pick_top_from_iterable(func_names, top_size)


def pick_top_verbs(repo_path, top_size=3):
    """
    Делает выборку самых популярных глаголов

    :param repo_path:       Путь к директории с репозиторием
    :param top_size:        Объём выборки
    :return:                list
    """
    func_names = find_func_names_in_repo(repo_path)
    verbs = flat([extract_verbs_from_function_name(func_name) for func_name in func_names])
    return pick_top_from_iterable(verbs, top_size)


def display_results(result_list):
    print('Наиболее часто используемые глаголы:')
    print('=' * 19)
    for pair in result_list:
        print('| {:10s} | {:2d} |'.format(*pair))
    print('=' * 19)