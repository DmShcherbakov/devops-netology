# 3.2. Работа в терминале, лекция 2 - Дмитрий Щербаков

### 1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.
```commandline
$ type -t cp
file
```
Данная команда имеет тип "файл", и вызывает программу, входящую в парет coreutils:
```commandline
$ dpkg -S /bin/cp
coreutils: /bin/cp
```

### 2. Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l? man grep поможет в ответе на этот вопрос. Ознакомьтесь с документом о других подобных некорректных вариантах использования pipe.
Для вывода количества строк, содержащих совпадение, используется параметр "-c":
```commandline
vagrant@vagrant:~$ grep grub /etc/default/grub | wc -l
5
vagrant@vagrant:~$ grep -c grub /etc/default/grub 
5
```

### 3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?
Это процесс init (в случае ubuntu 20.04 - подсистема инициализации и управления службами Systemd):
```commandline
vagrant@vagrant:~$ ps aux | head -2
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  1.1 167468 11120 ?        Ss   Nov13   0:01 /sbin/init
vagrant@vagrant:~$ cat /proc/1/status | head -1
Name:	systemd
```

### 4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?
Перенаправление, в общем виде, будет выглядеть как: `ls 2>/dev/pts/номер_терминала`:

### 5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.
Да, получится. Например, при использовании команды `$ cat /var/log/syslog | grep CRON > ~/cron.log` содержимое файла /var/log/syslog, будут передано на stdin команды grep, а результат ее работы (stdout) будет направлен в файл cron.log, расположенный в домашнем каталоге текущего пользователя:
```commandline
vagrant@vagrant:~$ cat /var/log/syslog | grep CRON > ~/cron.log
vagrant@vagrant:~$ cat ~/cron.log
Nov 14 00:17:01 vagrant CRON[12755]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 01:17:02 vagrant CRON[12765]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 02:17:01 vagrant CRON[12792]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 03:10:01 vagrant CRON[12801]: (root) CMD (test -e /run/systemd/system || SERVICE_MODE=1 /sbin/e2scrub_all -A -r)
Nov 14 03:17:01 vagrant CRON[12817]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 03:30:01 vagrant CRON[12823]: (root) CMD (test -e /run/systemd/system || SERVICE_MODE=1 /usr/lib/x86_64-linux-gnu/e2fsprogs/e2scrub_all_cron)
Nov 14 04:17:01 vagrant CRON[12852]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 05:17:01 vagrant CRON[12864]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 06:17:01 vagrant CRON[12873]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
Nov 14 06:25:01 vagrant CRON[12878]: (root) CMD (test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily ))
Nov 14 06:47:01 vagrant CRON[12943]: (root) CMD (test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly ))
Nov 14 07:17:01 vagrant CRON[12962]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
```

### 6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?
В случае, если консоль запущена (кто-то на нее залогинен), то перенаправление осуществляется тем же путем, что и в вопросе 4:
```commandline
vagrant@vagrant:~$ echo "Task 6" 1>/dev/tty1
```
При этом в консоли отображается перенаправленная строка.

### 7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?
При выполнении команды `bash 5>1&` для текущей сессии создается дополнительный дескриптор 5 со стандартным входом, и его stdout перенаправляется в стандартный вывод текущего терминала. Соответственно, команда `echo netology > /proc/$$/fd/5` из той же консоли приведет к выводу на экран строки "netology":
```commandline
vagrant@vagrant:~$ ls -l /proc/$$/fd/
total 0
lrwx------ 1 vagrant vagrant 64 Nov 13 20:26 0 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 13 20:26 1 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 13 20:26 2 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 14 07:38 255 -> /dev/pts/0
vagrant@vagrant:~$ bash 5>&1
vagrant@vagrant:~$ ls -l /proc/$$/fd
total 0
lrwx------ 1 vagrant vagrant 64 Nov 14 08:38 0 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 14 08:38 1 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 14 08:38 2 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 14 08:38 255 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Nov 14 08:38 5 -> /dev/pts/0
vagrant@vagrant:~$ echo netology > /proc/$$/fd/5
netology
```

# 8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.
