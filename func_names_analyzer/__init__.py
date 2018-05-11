# -*- coding: utf-8 -*-

import argparse
import sys

from func_names_analyzer.analyzer import pick_top_verbs, display_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--repo_path', type=str, nargs='?', default='.',
                        help='Путь к репозиторию с проектом')
    parser.add_argument('-s', '--size_of_top', type=int, nargs='?', default=3,
                        help='Рармер топа популярных слов')
    args = parser.parse_args(sys.argv[1:])

    repo_path = args.repo_path
    top_size = args.size_of_top

    top = pick_top_verbs(repo_path, top_size)
    display_results(top)
