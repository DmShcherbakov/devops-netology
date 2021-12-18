# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач" - Дмитрий Щербаков

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- |--|
| Какое значение будет присвоено переменной `c`?  | В данном случае, будет получено сообщение об ошибке: `TypeError: unsupported operand type(s) for +: 'int' and 'str'` |
| Как получить для переменной `c` значение 12?  | Следует задать переменную `a` следующим образом: `a = '1'` |
| Как получить для переменной `c` значение 3?  | Следует задать переменную `b` следующим образом: `b = 1` |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
С учетом того, что у меня настроен русский язык, я решил дополнительно добавить распознавание и на нем: 
```python
#!/usr/bin/env python3

import os

dir_path = "~/netology/sysadm-homeworks"
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
    if result.find('modified') != -1:
        res_prep_print(result, 'en')
    elif result.find('изменено') != -1:
        res_prep_print(result, 'ru')
```

### Вывод скрипта при запуске при тестировании:
У меня каталог другой, поэтому вместо `~/netology/sysadm-homeworks` в моем выводе `~/devops-netology/`
```
~/devops-netology/DZ/4.2.Python/readme.md
~/devops-netology/test/test
~/devops-netology/test/test.py
~/devops-netology/test/test.py_bck
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
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
```

### Вывод скрипта при запуске при тестировании:
```
$ ./test2.py /root/ /123/1 ~/devops-netology
/root/ is not a git repository
/123/1 doesn't exists
/home/dimka/devops-netology/DZ/4.2.Python/readme.md
/home/dimka/devops-netology/test/test.py
/home/dimka/devops-netology/test/test2.py
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```