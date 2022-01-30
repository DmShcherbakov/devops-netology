# 5.2. Применение принципов IaaC в работе с виртуальными машинами - Дмитрий Щербаков
## Задача 1
## - Опишите своими словами основные преимущества применения на практике IaaC паттернов.
Основными преимуществами применения IaaC-паттернов являются возможность строгого (и описанного) определения состава и характеристик развертываемой инфраструктуры, ускорение процесса развертывания на неограниченном количестве площадок за счет его унификации, снижение вероятности возникновения отличий в конфигурации инфраструктуры на разных площадках (устранение "дрейфа" конфигураций), обеспечение быстрой адаптации инфраструктуры к новым требованиям.   
## - Какой из принципов IaaC является основополагающим?
Основополагающим принципом IaaC является "идемпотентность", т.е. способность системы обеспечить от установки к установке предсказуемый и идентичный другим развертываниям, выполненным на базе той же конфигурации, результат.

## Задача 2
## - Чем Ansible выгодно отличается от других систем управление конфигурациями?
Ansible для своей работы использует ssh, поэтому не требует установки дополнительных агентов.
## - Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?
Применительно к разным ситуациям, у разных методов есть свои недостатки и преимущества.
В принципе, метод **Push** кажется мне более удобным и "осязаемым", т.к. в данном случае изменения принудительно распространяются на объекты в момент применения конфигурации. С другой стороны, наличие временного зазора, свойственного, как правило, методу **Pull**, дает возможность прервать и откатить некорректные изменения до того, как они успели примениться на всех узлах. Сравнивать же эти методы по критерию именно надежности, как мне видится, проблематично. Суть у них одна - изменения поступают на целевую систему, разница только в инициаторе.

## Задача 3
## Установить на личный компьютер:
## - VirtualBox
## - Vagrant
## - Ansible
## *Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*
```commandline
dim@dm:~$ dpkg -l | grep  "virtualbox "
ii  virtualbox                                    6.1.26-dfsg-3~ubuntu1.20.04.2         amd64        x86 virtualization solution - base binaries
dim@dm:~$ vagrant --version
Vagrant 2.2.6
dim@dm:~$ ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/dim/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
```

## Задача 4
## Воспроизвести практическую часть лекции самостоятельно.
## - Создать виртуальную машину.
## - Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды `docker ps`
```commandline
dim@dm:~/Netology/vag/vagrant$ vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
...
PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

dim@dm:~/Netology/vag/vagrant$ vagrant ssh
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 System information disabled due to load higher than 1.0


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Sun Jan 30 14:52:32 2022 from 10.0.2.2
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
