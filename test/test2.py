#!/usr/bin/env python3

import os
import sys

def res_prep_print(res_find, lng, dir_pa):
    if lng == 'en':
        prepare_result = res_find.replace('\tmodified:   ', '')
    elif lng == 'ru':
        prepare_result = res_find.replace('\tизменено:   ', '')
    prepare_result = prepare_result.strip()
    print(f"{dir_pa}/{prepare_result}")

def git_rep_check(dirp):
    bash_command = [f"cd {dirp}", "git status"]
    result_os = os.popen(' && '.join(bash_command)).read()
    for result in result_os.split('\n'):
    #    if result.find('изменено') != -1:
        if result.find('modified') != -1:
            res_prep_print(result, 'en', dirp)
        elif result.find('изменено') != -1:
            res_prep_print(result, 'ru', dirp)

for arg_dir in sys.argv [1:]:
    if not os.access(arg_dir, os.F_OK):
        print(arg_dir,'doesn\'t exists')
    else:
        if not os.access(f'{arg_dir}/.git/config', os.F_OK):
            print(arg_dir,'is not a git repository')
        else:
            git_rep_check(arg_dir)
