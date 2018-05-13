# -*- coding: utf-8 -*-

import ast
from nltk import pos_tag

from func_names_analyzer.utils import flat, find_py_files_in_dir,\
    split_upper_case_name, pick_top_from_iterable


def create_syntax_trees(inspected_path, with_file_names=False, with_file_content=False):
    trees = []
    py_files = find_py_files_in_dir(inspected_path)
    for py_file in py_files:
        with open(py_file, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
            tree_data = tree
            if with_file_names and with_file_content:
                tree_data = (py_file, main_file_content, tree)
            elif with_file_names:
                tree_data = (py_file, tree)
            trees.append(tree_data)
        except SyntaxError:
            pass
    return trees


def get_all_names_from_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def check_word_is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return 'VB' in pos_info[0][1]


def extract_verbs_from_function_name(function_name):
    return [w for w in function_name.split('_') if check_word_is_verb(w)]


def find_all_names_in_repo(repo_path):
    trees = create_syntax_trees(repo_path)
    all_names = flat([get_all_names_from_tree(t) for t in trees])
    names = [n for n in all_names if not (n.startswith('__') and n.endswith('__'))]
    return flat([split_upper_case_name(name) for name in names])


def find_func_names_in_repo(repo_path):
    all_func_nodes = list()
    trees = create_syntax_trees(repo_path)
    for tree in trees:
        current_tree_nodes = [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        all_func_nodes.extend(current_tree_nodes)
    func_names = [f for f in all_func_nodes if not (f.startswith('__') and f.endswith('__'))]
    return func_names


def pick_top_func_names(repo_path, top_size=10):
    func_names = find_func_names_in_repo(repo_path)
    return pick_top_from_iterable(func_names, top_size)


def pick_top_verbs(repo_path, top_size=3):
    func_names = find_func_names_in_repo(repo_path)
    verbs = flat([extract_verbs_from_function_name(func_name) for func_name in func_names])
    return pick_top_from_iterable(verbs, top_size)


def display_results(result_list):
    print('Топ используемых глаголов:')
    print('=' * 25)
    for pair in result_list:
        print('| {:16s} | {:2d} |'.format(*pair))
    print('=' * 25)
