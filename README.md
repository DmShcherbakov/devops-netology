# 3.2. Работа в терминале, лекция 2 - Дмитрий Щербаков

### 1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.
```commandline
vagrant@vagrant:~$ type -a cd
cd is a shell builtin
```
Данная команда является встроенной в shell. Она не имеет запускаемого файла, ее функционал описан в мануале bash в разделе "SHELL BUILTIN COMMANDS".

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
vagrant@vagrant:~$ cat /proc/1/cmdline 
/sbin/init 
```

### 4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?
Перенаправление, в общем виде, будет выглядеть как: `ls 2>/dev/pts/номер_терминала` (или /dev/ttyX, если мы говорим о TTY).

### 5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.
Да, получится. Например, при использовании команды `$ wc -l < /etc/hosts > ~/hosts.cnt` содержимое файла /etc/hosts будет передано на stdin команды wc -l, а результат ее работы (stdout) будет направлен в файл hosts.cnt, расположенный в домашнем каталоге текущего пользователя:
```commandline
vagrant@vagrant:~$ wc -l < /etc/hosts > ~/hosts.cnt
vagrant@vagrant:~$ cat ~/hosts.cnt 
7
vagrant@vagrant:~$ cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	vagrant.vm	vagrant

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

### 6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?
В случае, если консоль запущена (кто-то на нее залогинен), то перенаправление осуществляется тем же путем, что и в вопросе 4:
```commandline
vagrant@vagrant:~$ echo "Task 6" 1>/dev/tty1
```
При этом в консоли отображается перенаправленная строка.

### 7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?
При выполнении команды `bash 5>&1` для текущей сессии создается дополнительный дескриптор 5 со стандартным входом, и его stdout перенаправляется в стандартный вывод текущего терминала. Соответственно, команда `echo netology > /proc/$$/fd/5` из той же консоли приведет к выводу на экран строки "netology":
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

### 8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.
Да, получится. Пример:
```commandline
vagrant@vagrant:~$ grep ntp /etc/* 3>&1 1>&2 2>&3 | grep Permiss  >errors.txt 
/etc/services:nntp		119/tcp		readnews untp	# USENET News Transfer Protocol
/etc/services:ntp		123/udp				# Network Time Protocol
/etc/services:nntps		563/tcp		snntp		# NNTP over SSL
vagrant@vagrant:~$ cat errors.txt 
grep: /etc/at.deny: Permission denied
grep: /etc/gshadow: Permission denied
grep: /etc/gshadow-: Permission denied
grep: /etc/multipath: Permission denied
grep: /etc/shadow: Permission denied
grep: /etc/shadow-: Permission denied
grep: /etc/sudoers: Permission denied
```

### 9. Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?
Данная команда отобразит переменные окружения текущего сеанса на момент его запуска. Те же данные можно получить, воспользовавшись командой printenv:
```commandline
vagrant@vagrant:~$ cat /proc/$$/environ 
SHELL=/bin/bashLANGUAGE=en_US:LC_ADDRESS=C.UTF-8LC_NAME=C.UTF-8LC_MONETARY=C.UTF-8PWD=/home/vagrantLOGNAME=vagrantXDG_SESSION_TYPE=ttyMOTD_SHOWN=pamHOME=/home/vagrantLANG=C.UTF-8LC_PAPER=C.UTF-8LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:SSH_CONNECTION=10.0.2.2 50820 10.0.2.15 22LESSCLOSE=/usr/bin/lesspipe %s %sXDG_SESSION_CLASS=userTERM=xterm-256colorLC_IDENTIFICATION=C.UTF-8LESSOPEN=| /usr/bin/lesspipe %sUSER=vagrantSHLVL=1LC_TELEPHONE=C.UTF-8LC_MEASUREMENT=C.UTF-8XDG_SESSION_ID=4XDG_RUNTIME_DIR=/run/user/1000SSH_CLIENT=10.0.2.2 50820 22LC_TIME=C.UTF-8XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktopPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/binDBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/busSSH_TTY=/dev/pts/0LC_NUMERIC=C.UTF-8_=/usr/bin/bashvagrant@vagrant:~$ 
vagrant@vagrant:~$ printenv 
SHELL=/bin/bash
LANGUAGE=en_US:
LC_ADDRESS=C.UTF-8
LC_NAME=C.UTF-8
LC_MONETARY=C.UTF-8
PWD=/home/vagrant
LOGNAME=vagrant
XDG_SESSION_TYPE=tty
MOTD_SHOWN=pam
HOME=/home/vagrant
LC_PAPER=C.UTF-8
LANG=C.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:
SSH_CONNECTION=10.0.2.2 50820 10.0.2.15 22
LESSCLOSE=/usr/bin/lesspipe %s %s
XDG_SESSION_CLASS=user
LC_IDENTIFICATION=C.UTF-8
TERM=xterm-256color
LESSOPEN=| /usr/bin/lesspipe %s
USER=vagrant
SHLVL=2
LC_TELEPHONE=C.UTF-8
LC_MEASUREMENT=C.UTF-8
XDG_SESSION_ID=4
XDG_RUNTIME_DIR=/run/user/1000
SSH_CLIENT=10.0.2.2 50820 22
LC_TIME=C.UTF-8
XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
SSH_TTY=/dev/pts/0
LC_NUMERIC=C.UTF-8
_=/usr/bin/printenv
```

### 10. Используя man, опишите что доступно по адресам /proc/\<PID\>/cmdline, /proc/\<PID\>/exe.
С помощью команды `man proc` выясняем, что:
```commandline
       /proc/[pid]/cmdline
              This read-only file holds the complete command line for the process, unless the process is a zombie.  In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters.  The com‐
              mand-line arguments appear in this file as a set of strings separated by null bytes ('\0'), with a further null byte after the last string.
```
в файле cmdline содержится информация о команде, с помощью которой был запущен процесс. В нашем случае, `/proc/$$/cmdline` указывает на bash, который задан в качестве пользовательского шелла; 

```commandline
       /proc/[pid]/exe
              Under  Linux  2.2  and later, this file is a symbolic link containing the actual pathname of the executed command.  This symbolic link can be dereferenced normally; attempting to open it will open the executable.  You
              can even type /proc/[pid]/exe to run another copy of the same executable that is being run by process [pid].  If the pathname has been unlinked, the symbolic link will contain the string '(deleted)'  appended  to  the
              original pathname.  In a multithreaded process, the contents of this symbolic link are not available if the main thread has already terminated (typically by calling pthread_exit(3)).

              Permission to dereference or read (readlink(2)) this symbolic link is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2).

              Under Linux 2.0 and earlier, /proc/[pid]/exe is a pointer to the binary which was executed, and appears as a symbolic link.  A readlink(2) call on this file under Linux 2.0 returns a string in the format:

                  [device]:inode

              For example, [0301]:1502 would be inode 1502 on device major 03 (IDE, MFM, etc. drives) minor 01 (first partition on the first drive).

              find(1) with the -inum option can be used to locate the file.
```
данный файл содержит символическую ссылку на выполняемую команду (и далее по тексту). В нашем случае это, опять же, bash:
```commandline
$ ls -l /proc/$$/exe 
lrwxrwxrwx 1 vagrant vagrant 0 Nov 15 16:46 /proc/14576/exe -> /usr/bin/bash
```

### 11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo.
В моем случае, это sse:
```commandline
vagrant@vagrant:~$ cat /proc/cpuinfo | sed 's/ /\n/g' | grep sse | sort | uniq
misalignsse
sse
sse2
sse4_1
sse4_2
sse4a
ssse3
```

### 12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:
```
vagrant@netology1:~$ ssh localhost 'tty'
not a tty
```
### Почитайте, почему так происходит, и как изменить поведение.
Для того, чтобы команда отработала, необходимо запустить ssh с опцией "-t", использование которой инициирует создание псевдо терминала, который в обычном режиме не создается:
```commandline
vagrant@vagrant:~$ ssh -t localhost 'tty'
/dev/pts/3
Connection to localhost closed.
```

### 13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии.
Для начала, следует присвоить значение "0" параметру ядра kernel.yama.ptrace_scope.
После этого, процесс переноса процесса в "скрин" будет выглядеть следующим образом:

Текущий терминал (выход из watch осуществляется по Ctrl+z):
```commandline
vagrant@vagrant:~$ cat /proc/sys/kernel/yama/ptrace_scope 
0
vagrant@vagrant:~$ watch -n 1 date

[1]+  Stopped                 watch -n 1 date
vagrant@vagrant:~$ bg
[1]+ watch -n 1 date &

[1]+  Stopped                 watch -n 1 date
vagrant@vagrant:~$ jobs -l
[1]+  2003 Stopped (tty output)    watch -n 1 date
vagrant@vagrant:~$ disown watch
bash: warning: deleting stopped job 1 with process group 2003
```
Далее, заходим в "скрин" `vagrant@vagrant:~$ screen -S reptyr`, в котором осуществляем подключение:
```commandline
vagrant@vagrant:~$ reptyr 2003
```
После этого на экране отображается вывод даты. Можем осуществить отключение от "скрина" комбинацией Ctrl+A-D. 

### 14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.
Команда `tee` читает данные со стандартного ввода и передает их на стандартный вывод.
В данном примере, при вызове `sudo echo string > /root/new_file` sudo повышает привилегии при выполнении команды echo, а перенаправлении записи в файл производится уже с правами текущего пользователя.
Когда же мы используем конструкцию `echo string | sudo tee /root/new_file`, то здесь sudo применяется к tee, поэтому полученная на входе строка может быть записана в каталог /root с повышенными привелегиями.
