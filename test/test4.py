#!/usr/bin/env python3

import dns.resolver
import json
import yaml

# файлы для дампа встроенными функциями
prev_check_json = './prev.json'
prev_check_yaml = './prev.yml'
# файлы для вывода в формате, указанном в ДЗ
prev_check_json_form = './fprev.json'
prev_check_yaml_form = './fprev.yml'
#
addr_dict_old = {}
addr_dict_new = {}
addr_list = ['drive.google.com', 'mail.google.com', 'google.com']

# Один из используемых файлов (prev.json) считаем базовым, и данные предыдущей проверки берем оттуда.
with open(prev_check_json, 'r') as fread:
    addr_dict_old = json.load(fread)

# Осуществляем разрешение имен в первый из возвращаемых адресов, выводим результаты, заносим их в словарь.
for addr in addr_list:
    answer = dns.resolver.query(addr, 'A')
    ip_a = answer[0].to_text()
    print(addr, '-', ip_a)
    addr_dict_new[f'{addr}'] = ip_a

# Очищаем файл json, заносим в него данные текущего осмотра.
with open(prev_check_json, 'w') as f:
    f.truncate(0)
    f.write(json.dumps(addr_dict_new, indent=4))

# Очищаем файл yaml, заносим в него данные текущего осмотра.
with open(prev_check_yaml, 'w') as f:
    f.truncate(0)
    yaml.dump(addr_dict_new, f, default_flow_style=False, explicit_start=True)


# Открываем файлы требуемого формата, очищаем от старых значений.
p_c_j_f = open(prev_check_json_form, 'w')
p_c_y_f = open(prev_check_yaml_form, 'w')
p_c_j_f.truncate(0)
p_c_y_f.truncate(0)

# Производим сравнение словарей со старыми и новыми сочетаниями узел-адрес,
# записываем новые данные в файлы требуемого формата, выводим сообщение об ошибке в случае несовпадения.
for key, value in addr_dict_new.items():
    p_c_j_f.write(f'{{ "{key}" : "{value}"}}\n')
    p_c_y_f.write(f'- {key}: {value}\n')
    if addr_dict_new.get(key) != addr_dict_old.get(key):
        print(f'[ERROR] {key} IP mismatch: {addr_dict_old.get(key)} {addr_dict_new.get(key)}')

# Закрываем открытые файлы
p_c_j_f.close()
p_c_y_f.close()
