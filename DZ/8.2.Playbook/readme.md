# 08.02 Работа с Playbook - Дмитрий Щербаков

## Подготовка к выполнению

### 1. (Необязательно) Изучите, что такое [clickhouse](https://www.youtube.com/watch?v=fjTNS2zkeBs) и [vector](https://www.youtube.com/watch?v=CgEhyffisLY)
### 2. Создайте свой собственный (или используйте старый) публичный репозиторий на github с произвольным именем.
```commandline
$ git remote -v
origin	git@github.com:DmShcherbakov/ansible-8.2 (fetch)
origin	git@github.com:DmShcherbakov/ansible-8.2 (push)
```
### 3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
```commandline
$ git commit
[main 8c91b44] Playbook added
 4 files changed, 6118 insertions(+)
 create mode 100644 playbook/.gitignore
 create mode 100644 playbook/group_vars/clickhouse/vars.yml
 create mode 100644 playbook/inventory/prod.yml
 create mode 100644 playbook/site.yml
$ git push
Перечисление объектов: 11, готово.
Подсчет объектов: 100% (11/11), готово.
При сжатии изменений используется до 4 потоков
Сжатие объектов: 100% (7/7), готово.
Запись объектов: 100% (10/10), 32.89 КиБ | 2.19 МиБ/с, готово.
Всего 10 (изменения 3), повторно использовано 0 (изменения 0)
remote: Resolving deltas: 100% (3/3), done.
To github.com:DmShcherbakov/ansible-8.2
   0138ab8..8c91b44  main -> main
```
### 4. Подготовьте хосты в соответствии с группами из предподготовленного playbook.
```commandline
$ docker run -d -t --name clickhouse-01 --privileged=true pycontribs/centos:7 /usr/sbin/init
c0742ac5bab6b949d52359b53bc314fb200805a91043be85b9d8c9f761474c92
```

## Основная часть

### 1. Приготовьте свой собственный inventory файл `prod.yml`.
```commandline
$ cat prod.yml 
---
clickhouse:
  hosts:
    clickhouse-01:
      ansible_host: clickhouse-01
      ansible_connection: docker

```
### 2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает [vector](https://vector.dev).
### 3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.
### 4. Tasks должны: скачать нужной версии дистрибутив, выполнить распаковку в выбранную директорию, установить vector.
```commandline
- name: Install Vector
  hosts: clickhouse
  tasks:
    - name: Get and extract archive
      ansible.builtin.unarchive:
        src: "https://packages.timber.io/vector/{{ vector_version }}/vector-{{ vector_version }}-x86_64-unknown-linux-musl.tar.gz"
        dest: "/tmp"
        remote_src: yes
    - block:
      - name: User create
        ansible.builtin.user:
          name: vector
      - name: Create a working directory
        ansible.builtin.file:
          path: "/var/lib/vector"
          state: directory
          mode: '0755'
          owner: vector
          group: vector
      - name: Create a config directory
        ansible.builtin.file:
          path: "/etc/vector"
          state: directory
          mode: '0755'
      - name: Program Copying
        ansible.builtin.copy:
          src: "/tmp/vector-x86_64-unknown-linux-musl/bin/vector"
          dest: "/usr/bin/vector"
          mode: 755
          remote_src: yes
      - name: Config Copying
        ansible.builtin.copy:
          src: "/tmp/vector-x86_64-unknown-linux-musl/config/vector.toml"
          dest: "/etc/vector/vector.toml"
          remote_src: yes
      - name: Service file Copying
        ansible.builtin.copy:
          src: "/tmp/vector-x86_64-unknown-linux-musl/etc/systemd/vector.service"
          dest: "/etc/systemd/system/vector.service"
          remote_src: yes
      notify: Start Vector service
  handlers:
    - name: Start Vector service
      become: true
      ansible.builtin.service:
        name: vector
        state: restarted
```
### 5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.
```commandline
$ ansible-lint site.yml
WARNING  Overriding detected file kind 'yaml' with 'playbook' for given positional argument: site.yml
```
### 6. Попробуйте запустить playbook на этом окружении с флагом `--check`.
```commandline
$ ansible-playbook site.yml -i inventory/prod.yml --check

PLAY [Install Clickhouse] ********************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 0, "gid": 0, "group": "root", "item": "clickhouse-common-static", "mode": "01204", "msg": "Request failed", "owner": "root", "response": "HTTP Error 404: Not Found", "size": 246310036, "state": "file", "status_code": 404, "uid": 0, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Install clickhouse packages] ***********************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Create database] ***********************************************************************************************************************************************************************************************************
skipping: [clickhouse-01]

PLAY [Get and Install Vector] ****************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get and extract archive] ***************************************************************************************************************************************************************************************************
skipping: [clickhouse-01]

TASK [User create] ***************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Create a working directory] ************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Create a config directory] *************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Program Copying] ***********************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Config Copying] ************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Service file Copying] ******************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

PLAY RECAP ***********************************************************************************************************************************************************************************************************************
clickhouse-01              : ok=10   changed=0    unreachable=0    failed=0    skipped=2    rescued=1    ignored=0   
```
### 7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.
### 8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.
### 9. Подготовьте README.md файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.
### 10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-02-playbook` на фиксирующий коммит, в ответ предоставьте ссылку на него.
[Ссылка на репозиторий](https://github.com/DmShcherbakov/ansible-8.2)
