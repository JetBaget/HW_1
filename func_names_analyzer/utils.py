# -*- coding: utf-8 -*-

import os
from collections import Counter


def flat(_list):
    return [i for v in _list for i in v]


def find_py_files_in_dir(repo_path):
    py_files = list()
    for root, dirs, files in os.walk(repo_path, topdown=True):
        for file in files:
            if not file.endswith('.py'):
                continue
            py_files.append(os.path.join(root, file))
    return py_files


def split_upper_case_name(name):
    return [n for n in name.split('_') if n]


def pick_top_from_iterable(iterable, top_size=3):
    return Counter(iterable).most_common(top_size)