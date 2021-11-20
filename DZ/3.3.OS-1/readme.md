# 3.3. Операционные системы, лекция 1 - Дмитрий Щербаков

### 1. Какой системный вызов делает команда cd? В прошлом ДЗ мы выяснили, что cd не является самостоятельной программой, это shell builtin, поэтому запустить strace непосредственно на cd не получится. Тем не менее, вы можете запустить strace на /bin/bash -c 'cd /tmp'. В этом случае вы увидите полный список системных вызовов, которые делает сам bash при старте. Вам нужно найти тот единственный, который относится именно к cd. Обратите внимание, что strace выдаёт результат своей работы в поток stderr, а не в stdout.
Команда cd осуществляет системный вызов chdir:
```commandline
vagrant@vagrant:~$ strace /bin/bash -c 'cd /tmp' 2>&1 | grep chdir
chdir("/tmp")                           = 0
```
Воспользовавшись справкой, полученной командой `man 2 chdir`, можно узнать следующее:
```commandline
DESCRIPTION
       chdir() changes the current working directory of the calling process to the directory specified in path.
```

### 2. Попробуйте использовать команду file на объекты разных типов на файловой системе. Например:
```commandline
vagrant@netology1:~$ file /dev/tty
/dev/tty: character special (5/0)
vagrant@netology1:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@netology1:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64
```
### Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.
Все представленные команды осуществляют последовательный поиск файла `magic.mgc` сначала в домашнем каталоге текущего пользователя (.magic.mgc), потом в каталоге `/etc/`, а затем в папке `/usr/share/misc/`, где они его и находят:
```commandline
vagrant@vagrant:~$ strace file /bin/bash 2>&1 | grep magic.mgc
stat("/home/vagrant/.magic.mgc", 0x7ffcb5b89230) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
vagrant@vagrant:~$ strace file /dev/tty 2>&1 | grep magic.mgc
stat("/home/vagrant/.magic.mgc", 0x7ffcf6bcfe90) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
vagrant@vagrant:~$ strace file /dev/sda 2>&1 | grep magic.mgc
stat("/home/vagrant/.magic.mgc", 0x7ffc9a7634b0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
vagrant@vagrant:~$ strace file /bin/bash 2>&1 | grep magic.mgc
stat("/home/vagrant/.magic.mgc", 0x7ffe4d711f70) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
```

### 3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).
При открытии файла для записи в него журналов, система назначает ему выделенный файловый дескриптор, связанный с текущим процессом. Зная ID процесса, при помощи команды lsof мы можем узнать какой дескриптор сопоставлен интересующему нас файлу (`lsof -p <PID>`), после чего осуществить перенаправление в целевой файл (`cat /proc/<PID>/fd/<descr> > path_to_file`).
Для очистки содержимого файла с целью высвобождения дискового пространства можно воспользоваться "пустым" перенаправлением:
```commandline
vagrant@vagrant:~$ du -sh date.log 
4.0K	date.log
vagrant@vagrant:~$ > date.log 
vagrant@vagrant:~$ du -sh date.log 
0	date.log
```

### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?
Согласно официальной позиции, процесс-зомби — дочерний процесс, завершивший своё выполнение, но ещё присутствующий в списке процессов операционной системы, чтобы дать родительскому процессу считать код завершения.
Зомби не занимают памяти (как процессы-сироты), но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.
Зомби-процесс существует до тех пор, пока родительский процесс не прочитает его статус с помощью системного вызова wait(), в результате чего запись в таблице процессов будет освобождена.
На странице 28 презентации к лекции так же говорится о том, что зомби - это уже **завершивший** свою работу дочерний процесс, поэтому говорить о расходовании ресурсов было бы странным.

С другой стороны, в интернете часто встречаются жалобы на то, что зомби-процесс "отъедает" память. Вероятно, это связано с подменой понятий.

### 5. В iovisor BCC есть утилита opensnoop:
```
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
```
### На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.
В первую секунду было зафиксировано обращение только к файлу `/var/run/utmp`:
```commandline
vagrant@vagrant:~$ sudo opensnoop-bpfcc -d 1
PID    COMM               FD ERR PATH
794    vminfo              4   0 /var/run/utmp
```

### 6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.
Каманда `uname -a` использует системный вызов `uname`:
```commandline
vagrant@vagrant:~$ strace uname -a 2>&1 | grep uname
execve("/usr/bin/uname", ["uname", "-a"], 0x7ffc08f3c498 /* 33 vars */) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
```
Вызвав руководство с помощью команды `man 2 uname`, в разделе "NOTES" можем найти следующее:
"Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}."
Соответственно, данные, представляемые командой `uname -a`, можно получить в указанных файлах:
```commandline
vagrant@vagrant:~$ uname -a
Linux vagrant 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
vagrant@vagrant:~$ 
vagrant@vagrant:~$ for i in ostype hostname osrelease version domainname; do cat /proc/sys/kernel/$i | tr '\n' ' '; done
Linux vagrant 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 (none) 
```
Если требуется узнать только версию ядра и релиз ОС, то количество аргументов можно сократить:
```commandline
vagrant@vagrant:~$ for i in osrelease version; do cat /proc/sys/kernel/$i ; done
5.4.0-80-generic
#90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021
```
***
*Также можно почерпнуть требуемую информацию из файла `/proc/version`*

### 7. Чем отличается последовательность команд через ; и через && в bash? Например:
```commandline
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```
### Есть ли смысл использовать в bash &&, если применить set -e?
При использовании точки с запятой, команды выполняются последовательно, вне зависимости от степени успешности ихх выполнения. С другой стороны, при разделении команд с помощью `&&`, команда справа от данного разделителя будет исполнена только в том случае, если выполнение команды слева закончилось успешно.
Применение опции `set -e` (errexit), в случае, если какая-то из команд возвратила код ошибки (non-zero status), приведет к завершению работы текущей оболочки (соответственно, дальнейшая часть скрипта просто не будет обработана). Это может оказаться полезным, например, для предотвращения зависания в цикле.

### 8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?
По данным справки:
```commandline
      -e  Exit immediately if a command exits with a non-zero status.
      -u  Treat unset variables as an error when substituting.
      -x  Print commands and their arguments as they are executed.
      pipefail     the return value of a pipeline is the status of
                   the last command to exit with a non-zero status,
                   or zero if no command exited with a non-zero status
```
Таким образом:
- параметр -e указывает оболочке выйти, если команда дает ненулевой статус выхода. Проще говоря, оболочка завершает работу при сбое команды;
- опция -u обрабатывает неустановленные или неопределенные переменные, за исключением специальных параметров, таких как подстановочные знаки (*) или «@», как ошибки во время раскрытия параметра;
- опция -x печатает команды и их аргументы во время выполнения;
- опция pipeline возвращает статус последней команды, завершившейся ошибкой (non-zero status), или ноль, если команды, завершившиеся с ошибкой, отсутствуют. 

Директива `set -e` не работает при работе с конвейерными командами. Когда вы запускаете сценарий, он возвращает ошибку, но продолжает выполнять следующую команду. Чтобы преодолеть это препятствие, можно воспользоваться конструкцией `set -eo pipefail`, на этот раз сценарий завершается и не выполняет следующую строку.

### 9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).
1. При использовании опции `stat`, как указано в задании, наиболее встречающийся статус можно посчитать следующим образом:
```commandline
vagrant@vagrant:~$ ps -eo stat | cut -c 1 | sort | uniq -c | sort -r -n $1
     60 S
     48 I
      1 R
```
2. Альтернативно, можно воспользоваться параметром `state`, который выводит статус процесса одним символом:
```commandline
vagrant@vagrant:~$ ps -eo state | sort | uniq -c | sort -r -n $1
     59 S
     48 I
      1 R
```
Наиболее распространенными являются процессы, ожидающие событий (прерываемый сон), отмеченные символом S.
За ними по распространенности следуют фоновые потоки ядра, отмеченные символом I.
Один процесс отображен со статусом "запущенный" (или стоит в очереди на запуск), отмечен буквой R.

Дополнительные символы в статусе процессов означают:
```commandline
               <    high-priority (not nice to other users)
               N    low-priority (nice to other users)
               L    has pages locked into memory (for real-time and custom IO)
               s    is a session leader
               l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
               +    is in the foreground process group
```
