# 3.4. Операционные системы, лекция 2 - Дмитрий Щербаков

### 1. На лекции мы познакомились с node_exporter. В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter:
### - поместите его в автозагрузку,
### - предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron),
### - удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

```commandline
vagrant@vagrant:~$ wget https://github.com/prometheus/node_exporter/releases/download/v1.3.0/node_exporter-1.3.0.linux-amd64.tar.gz
--2021-11-24 16:31:44--  https://github.com/prometheus/node_exporter/releases/download/v1.3.0/node_exporter-1.3.0.linux-amd64.tar.gz
Resolving github.com (github.com)... 140.82.121.4
Connecting to github.com (github.com)|140.82.121.4|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/9524057/f9ad431c-bedd-4b4e-8d3c-c9c8f8279da6?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20211124%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211124T163014Z&X-Amz-Expires=300&X-Amz-Signature=c6df00aa98c727f2dd8fd82aa3683ba453510937edbf15f6f22441a84455b032&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=9524057&response-content-disposition=attachment%3B%20filename%3Dnode_exporter-1.3.0.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream [following]
--2021-11-24 16:31:44--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/9524057/f9ad431c-bedd-4b4e-8d3c-c9c8f8279da6?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20211124%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211124T163014Z&X-Amz-Expires=300&X-Amz-Signature=c6df00aa98c727f2dd8fd82aa3683ba453510937edbf15f6f22441a84455b032&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=9524057&response-content-disposition=attachment%3B%20filename%3Dnode_exporter-1.3.0.linux-amd64.tar.gz&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.109.133, 185.199.110.133, 185.199.111.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.109.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 9030402 (8.6M) [application/octet-stream]
Saving to: ‘node_exporter-1.3.0.linux-amd64.tar.gz’

node_exporter-1.3.0.linux-amd64.tar.gz                      100%[========================================================================================================================================>]   8.61M  11.4MB/s    in 0.8s    

2021-11-24 16:31:46 (11.4 MB/s) - ‘node_exporter-1.3.0.linux-amd64.tar.gz’ saved [9030402/9030402]

vagrant@vagrant:~$ tar -zxf node_exporter-1.3.0.linux-amd64.tar.gz 
vagrant@vagrant:~$ sudo mv node_exporter-1.3.0.linux-amd64/node_exporter /usr/local/bin/
vagrant@vagrant:~$ sudo useradd --no-create-home --shell /bin/false nodeuser
vagrant@vagrant:~$ cat /lib/systemd/system/node_exporter.service 
[Unit]
Description=Node Exporter Service
After=network.target

[Service]
User=nodeuser
Group=nodeuser
Type=simple
ExecStart=/usr/local/bin/node_exporter $OPTIONS
EnvironmentFile=/etc/node_exporter/node_exporter.conf
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target

vagrant@vagrant:~$ sudo systemctl start node_exporter
vagrant@vagrant:~$ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter Service
     Loaded: loaded (/lib/systemd/system/node_exporter.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-11-24 16:45:43 UTC; 4s ago
   Main PID: 13205 (node_exporter)
      Tasks: 4 (limit: 1071)
     Memory: 2.3M
     CGroup: /system.slice/node_exporter.service
             └─13205 /usr/local/bin/node_exporter

Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=thermal_zone
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=time
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=timex
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=udp_queues
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=uname
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=vmstat
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=xfs
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:115 level=info collector=zfs
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.274Z caller=node_exporter.go:199 level=info msg="Listening on" address=:9100
Nov 24 16:45:43 vagrant node_exporter[13205]: ts=2021-11-24T16:45:43.275Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
vagrant@vagrant:~$ sudo systemctl enable node_exporter
Created symlink /etc/systemd/system/multi-user.target.wants/node_exporter.service → /lib/systemd/system/node_exporter.service.
vagrant@vagrant:~$ systemctl list-unit-files --state enabled | grep node_exporter
node_exporter.service                  enabled enabled  

```
Сервис запущен и добавлен в автозагрузку. Порт отвечает. С хост-системы можем видеть (порт 9123 перенаправляется на порт 9100 виртуальной системы - `  config.vm.network "forwarded_port", guest: 9100, host: 9123
`):
```commandline
dimka@dmhome:~$ lynx -dump 127.0.0.1:9123
                                 Node Exporter

   [1]Metrics

Ссылки

   1. http://127.0.0.1:9123/metrics

```

### 2. Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.
Я бы выбрал следующие опции для базового мониторинга:
- **CPU**:
      --collector.perf.cpus=""   List of CPUs from which perf metrics should be
                                 collected
- **памяти**:
      --collector.meminfo        Enable the meminfo collector (default:
                                 enabled).
- **диску**:
      --collector.diskstats      Enable the diskstats collector (default:
                                 enabled).
- **сети**:
      --collector.netstat.fields="^(.*_(InErrors|InErrs)|Ip_Forwarding|Ip(6|Ext)_(InOctets|OutOctets)|Icmp6?_(InMsgs|OutMsgs)|TcpExt_(Listen.*|Syncookies.*|TCPSynRetrans|TCPTimeouts)|Tcp_(ActiveOpens|InSegs|OutSegs|OutRsts|PassiveOpens|RetransSegs|CurrEstab)|Udp6?_(InDatagrams|OutDatagrams|NoPorts|RcvbufErrors|SndbufErrors))$"  
                                 Regexp of fields to return for netstat
                                 collector.

### 3. Установите в свою виртуальную машину Netdata. Воспользуйтесь готовыми пакетами для установки (sudo apt install -y netdata). После успешной установки:

* в конфигурационном файле /etc/netdata/netdata.conf в секции [web] замените значение с localhost на bind to = 0.0.0.0,
* добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте vagrant reload:
```commandline
config.vm.network "forwarded_port", guest: 19999, host: 19999
```
### После успешной перезагрузки в браузере на своем ПК (не в виртуальной машине) вы должны суметь зайти на localhost:19999. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.
```commandline
vagrant@vagrant:~$ sudo apt install -y netdata
...
vagrant@vagrant:~$ dpkg -l | grep netdata
ii  netdata                              1.19.0-3ubuntu1                   all          real-time performance monitoring (metapackage)
ii  netdata-core                         1.19.0-3ubuntu1                   amd64        real-time performance monitoring (core)
ii  netdata-plugins-bash                 1.19.0-3ubuntu1                   all          real-time performance monitoring (bash plugins)
ii  netdata-plugins-nodejs               1.19.0-3ubuntu1                   all          real-time performance monitoring (nodejs plugins)
ii  netdata-plugins-python               1.19.0-3ubuntu1                   all          real-time performance monitoring (python plugins)
ii  netdata-web                          1.19.0-3ubuntu1                   all          real-time performance monitoring (web)
vagrant@vagrant:~$ cat /etc/netdata/netdata.conf | grep bind | grep -v ^#
	bind socket to IP = 0.0.0.0
```
На хост системе:
```commandline
dimka@dmhome:~/Nextcloud/Обмен/Netology_DZ/vagrant$ cat Vagrantfile | grep 19999
  config.vm.network "forwarded_port", guest: 19999, host: 19999
dimka@dmhome:~/Nextcloud/Обмен/Netology_DZ/vagrant$ vagrant reload
==> default: Attempting graceful shutdown of VM...
...
==> default: Forwarding ports...
    default: 9100 (guest) => 9123 (host) (adapter 1)
    default: 19999 (guest) => 19999 (host) (adapter 1)
    default: 22 (guest) => 2200 (host) (adapter 1)
...
==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
==> default: flag to force provisioning. Provisioners marked to run always will still run.
```
После чего в браузере можно наблюдать следующее:
![Вид страницы в браузере](netdata.png)

### 4. Можно ли по выводу dmesg понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?
Да, можно:
```commandline
vagrant@vagrant:~$ dmesg | grep -i virt
[    0.000000] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[    0.001497] CPU MTRRs all blank - virtualized system.
[    0.037099] Booting paravirtualized kernel on KVM
[    0.172502] Performance Events: PMU not available due to virtualization, using software events only.
[    3.159523] systemd[1]: Detected virtualization oracle.
vagrant@vagrant:~$ dmesg | grep -i hyper
[    0.000000] Hypervisor detected: KVM

```
На обычной хост системе, в моем случае (с той же Ubuntu 20.04), вывод данных команд пуст.

### 5. Как настроен sysctl fs.nr_open на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (ulimit --help)?
Значение параметра по-умолчанию можно посмотреть следующими способами:
```commandline
vagrant@vagrant:~$ sysctl -n fs.nr_open
1048576
vagrant@vagrant:~$ cat /proc/sys/fs/nr_open 
1048576
```
Этот параметр определяет максимальное количество открытых файловых дескрипторов. 