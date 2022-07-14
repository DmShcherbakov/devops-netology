#!/usr/bin/env python3

import os

#dir_path = "~/netology/sysadm-homeworks"
dir_path = '~/devops-netology'
bash_command = [f"cd {dir_path}", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False

def res_prep_print(res_find, lng):
    if lng == 'en':
        prepare_result = res_find.replace('\tmodified:   ', '')
    elif lng == 'ru':
        prepare_result = res_find.replace('\tизменено:   ', '')
    prepare_result = prepare_result.strip()
    print(f"{dir_path}/{prepare_result}")

for result in result_os.split('\n'):
#    if result.find('изменено') != -1:
    if result.find('modified') != -1:
        res_prep_print(result, 'en')
    elif result.find('изменено') != -1:
        res_prep_print(result, 'ru')
