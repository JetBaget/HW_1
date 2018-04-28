import ast
import os
import collections

from nltk import pos_tag


def flat(_list):
    """
    Разворачивает вложенные массивы в один список
    [[1,2], [3,4,5], [6]] -> [1,2,3,4,5,6]

    :param _list:           Список, содержащий вложенные массивы
    :return:                Список элементов вложенных массивов
    """
    return [i for v in _list for i in v]


def is_verb(word):
    """
    Осуществляет проверку, является ли слово глаголом

    :param word:            Строка
    :return:                boolean
    """
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def collect_pyfiles_in_path(inspected_path):
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
    pathes_to_pyfiles = collect_pyfiles_in_path(inspected_path)
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


def get_all_names(tree):
    """
    Возвращает список всех имен, содержащихся в синтаксическом дереве

    :param tree:            Объект дерева
    :return:                list
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def extract_verbs_from_function_name(function_name):
    """
    Извлекает из названий функций глаголы

    :param function_name:           Название функции
    :return:                        list
    """
    return [w for w in function_name.split('_') if is_verb(w)]


def split_name_to_words(name):
    """
    Разбивает название в snake_case на слова

    :param name:            Название в snake_case
    :return:                list
    """
    return [n for n in name.split('_') if n]


def get_all_words_in_path(path):
    """
    Возвращает все названия, кроме защищенных

    :param path:            Путь к директории
    :return:                list
    """
    trees = create_syntax_trees(path)
    func_names = [f for f in flat([get_all_names(t) for t in trees]) if
                  not (f.startswith('__') and f.endswith('__'))]
    return flat([split_name_to_words(func_name) for func_name in func_names])


def get_func_names_in_path(path):
    """
    Возвращает все названия функций, кроме защищенных

    :param path:            Путь к директории
    :return:                list
    """
    trees = create_syntax_trees(path)
    names = [f for f in flat([[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                              for tree in trees]) if not (f.startswith('__') and f.endswith('__'))]
    return names


def pick_top_func_names(path, top_size=10):
    """
    Делает выборку самых популярных названий функций

    :param path:            Путь к директории
    :param top_size:        Объём выборки
    :return:                list
    """
    func_names = get_func_names_in_path(path)
    return collections.Counter(func_names).most_common(top_size)


def pick_top_verbs(path, top_size=10):
    """
    Делает выборку самых популярных глаголов

    :param path:            Путь к директории
    :param top_size:        Объём выборки
    :return:                list
    """
    func_names = get_func_names_in_path(path)
    verbs = flat([extract_verbs_from_function_name(func_name) for func_name in func_names])
    return collections.Counter(verbs).most_common(top_size)


if __name__ == '__main__':
    path = str(input('Введите путь к директории, содержащей проект на python:\n'))
    if not os.path.exists(path):
        print('Указанный путь не существует в файловой системе')
        exit(1)
    try:
        print('Наиболее часто используемые глаголы:')
        print('='*19)
        for pair in pick_top_verbs(path):
            print('| {:10s} | {:2d} |'.format(*pair))
        print('=' * 19)
    except (FileNotFoundError, OSError) as err:
        print('Ошибка: {}'.format(err))
        exit(1)
