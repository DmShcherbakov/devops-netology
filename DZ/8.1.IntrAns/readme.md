# 08.01 Введение в Ansible - Дмитрий Щербаков

## Подготовка к выполнению
### 1. Установите ansible версии 2.10 или выше.
```commandline
$ ansible --version
ansible [core 2.13.1]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/dim/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/dim/.local/lib/python3.8/site-packages/ansible
  ansible collection location = /home/dim/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/dim/.local/bin/ansible
  python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
  jinja version = 3.1.2
  libyaml = True
```
### 2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
```commandline
$ git remote -v
origin	git@github.com:DmShcherbakov/ansible.git (fetch)
origin	git@github.com:DmShcherbakov/ansible.git (push)
```
### 3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
```commandline
10:45:26 dim@dm:~/Nextcloud2/Обмен/ansible$ git commit 
[main 5425c3b] playbook added
 7 files changed, 41 insertions(+)
 create mode 100644 playbook/README.md
 create mode 100644 playbook/group_vars/all/examp.yml
 create mode 100644 playbook/group_vars/deb/examp.yml
 create mode 100644 playbook/group_vars/el/examp.yml
 create mode 100644 playbook/inventory/prod.yml
 create mode 100644 playbook/inventory/test.yml
 create mode 100644 playbook/site.yml
10:46:06 dim@dm:~/Nextcloud2/Обмен/ansible$ git push
Перечисление объектов: 16, готово.
Подсчет объектов: 100% (16/16), готово.
При сжатии изменений используется до 4 потоков
Сжатие объектов: 100% (9/9), готово.
Запись объектов: 100% (15/15), 1.65 КиБ | 1.65 МиБ/с, готово.
Всего 15 (изменения 0), повторно использовано 0 (изменения 0)
To github.com:DmShcherbakov/ansible.git
   0639ebd..5425c3b  main -> main
```

## Основная часть
### 1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт `some_fact` для указанного хоста при выполнении playbook'a.
С учетом того, что "some_fact" размещен в задании с именем "Print fact", из вывода интересует следующее:
```commandline
$ ansible-playbook -i inventory/test.yml site.yml 
...
TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}
...
```
### 2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.
```commandline
$ sed -i 's/12/all default fact/g' `grep -rl 12 *`
$ ansible-playbook -i inventory/test.yml site.yml 
...
TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "all default fact"
}
...
```
### 3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
### 4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.
```commandline
$ cat inventory/prod.yml 
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: local

$ ansible-playbook -i inventory/prod.yml site.yml 

PLAY [Print os facts] ************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ******************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [ubuntu] => {
    "msg": "deb"
}
ok: [centos7] => {
    "msg": "el"
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
### 5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.
```commandline
12:09:57 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ sed -i 's/some_fact: "deb"/some_fact: "deb default fact"/g' `grep -rl 'some_fact: "deb"' *`
12:10:31 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ sed -i 's/some_fact: "el"/some_fact: "el default fact"/g' `grep -rl 'some_fact: "el"' *`
```
### 6. Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.
```commandline
12:11:52 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ ansible-playbook -i inventory/prod.yml site.yml 
...
TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
...
```
### 7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
```commandline
12:34:07 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ ansible-vault encrypt_string 'deb default fact' --name 'some_fact'
New Vault password: 
Confirm New Vault password: 
Encryption successful
some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63303633376362386232616630653939396439353133303533343430356465353264663062336236
          3837353163666435636463626338663439653261303738340a633330343332356364356632316131
          33613938323035636663623665366563646536323966613066356262383363613935393231373631
          3135356234616266630a616633643633623136373839376166656338356530363732613163353937
          64333964346436326462376334323232343061656662346335623630323131376563

12:35:25 dim@dm:~/Nextcloud2/Обмен/ansible/playbook/group_vars/el$ ansible-vault encrypt_string 'el default fact' --name 'some_fact'
New Vault password: 
Confirm New Vault password: 
Encryption successful
some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          36386138333661376266323336306538323762346237616264363931323265386335366637643862
          3561613232623438613232346632313837643432323662360a343535316161386130316331396535
          36303436383839646234366434323733303334396434336461616638383534653462663231343038
          6566373232636637650a393838313661373838376436323464333630353933383266356563336635
          3437

12:36:43 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ cat group_vars/deb/examp.yml 
---
some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63303633376362386232616630653939396439353133303533343430356465353264663062336236
          3837353163666435636463626338663439653261303738340a633330343332356364356632316131
          33613938323035636663623665366563646536323966613066356262383363613935393231373631
          3135356234616266630a616633643633623136373839376166656338356530363732613163353937
          64333964346436326462376334323232343061656662346335623630323131376563
12:37:56 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ cat group_vars/el/examp.yml 
---
some_fact: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          36386138333661376266323336306538323762346237616264363931323265386335366637643862
          3561613232623438613232346632313837643432323662360a343535316161386130316331396535
          36303436383839646234366434323733303334396434336461616638383534653462663231343038
          6566373232636637650a393838313661373838376436323464333630353933383266356563336635
          3437
```
### 8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.
```commandline
12:36:20 dim@dm:~/Nextcloud2/Обмен/ansible/playbook$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] ************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ******************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
### 9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
```commandline
$ ansible-doc -t connection -l | grep control
community.docker.nsenter       execute on host running controller container
local                          execute on controller      
```
Наиболее очевидный к использованию - "local".
### 10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
```commandline
$ cat inventory/prod.yml 
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: docker
  local:
    hosts:
      dm:
        ansible_connection: local
```
### 11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.
```commandline
$ ansible-playbook -i inventory/prod.yml site.yml --ask-vault-pass
Vault password: 
...
TASK [Print fact] ****************************************************************************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [dm] => {
    "msg": "all default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
```
### 12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.
