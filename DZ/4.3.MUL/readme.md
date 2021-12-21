# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML" - Дмитрий Щербаков


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
Нужно найти и исправить все ошибки, которые допускает наш сервис

Исправленный вариант будет выглядеть так (7175 надо заменить на нормальный ip-адрес, но он в задании не указан):
```json
    { "info" : "Sample JSON output from our service\t",
        "elements" : [
            { "name" : "first",
            "type" : "server",
            "ip" : "12.34.56.78" 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```


## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
С учетом того, что я изначально писал скрипт с использованием словарей, гораздо удобнее импортировать/экспортировать из/в заданные форматы целиком весь соварь, однако при этом формат записей несколько отличается от указанного в задании. Поэтому, я решил в скрипте производить работу как с тем, так и с другим форматом.
```python
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
```

### Вывод скрипта при запуске при тестировании:
```
$ ./test4.py 
drive.google.com - 173.194.221.194
mail.google.com - 142.251.1.17
google.com - 74.125.131.102
[ERROR] mail.google.com IP mismatch: 142.251.1.19 142.251.1.17
[ERROR] google.com IP mismatch: 142.250.150.102 74.125.131.102
```

### json-файл(ы), который(е) записал ваш скрипт:
fprev.json
```json
{ "drive.google.com" : "173.194.221.194"}
{ "mail.google.com" : "142.251.1.17"}
{ "google.com" : "74.125.131.102"}
```
prev.json 
```json
{
    "drive.google.com": "173.194.221.194",
    "mail.google.com": "142.251.1.17",
    "google.com": "74.125.131.102"
}
```

### yml-файл(ы), который(е) записал ваш скрипт:
fprev.yml
```yaml
- drive.google.com: 173.194.221.194
- mail.google.com: 142.251.1.17
- google.com: 74.125.131.102
```
prev.yml
```yaml
---
drive.google.com: 173.194.221.194
google.com: 74.125.131.102
mail.google.com: 142.251.1.17
```
