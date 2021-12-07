# 3.8. Компьютерные сети, лекция 3 - Дмитрий Щербаков
### 1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```commandline
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```

Результат:
```commandline
route-views>show ip route 94.124.179.173    
Routing entry for 94.124.178.0/23
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 3d03h ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 3d03h ago
      Route metric is 0, traffic share count is 1
      AS Hops 2
      Route tag 6939
      MPLS label: none
route-views>show ip route 94.124.179.173 255.255.255.255
% Subnet not in table
route-views>show bgp 94.124.179.173 255.255.255.255     
% Network not in table
route-views>show bgp 94.124.179.173                
BGP routing table entry for 94.124.178.0/23, version 1393673220
Paths: (24 available, best #6, table default)
  Not advertised to any peer
  Refresh Epoch 1
  4901 6079 3257 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    162.250.137.254 from 162.250.137.254 (162.250.137.254)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 65000:10100 65000:10300 65000:10400
      path 7FE0E01555E8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 3
  3303 31500 42065, (aggregated by 65500 185.26.72.1)
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 3303:1004 3303:1006 3303:1030 3303:1031 3303:3054 52005:65032
      path 7FE18057DA68 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3356 31500 31500 31500 31500 31500 31500 31500 42065, (aggregated by 65500 185.26.72.1)
    4.68.4.46 from 4.68.4.46 (4.69.184.201)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      Community: 3356:2 3356:22 3356:100 3356:123 3356:507 3356:903 3356:2111 31500:10 31500:812 31500:5555 31500:5561 31500:5800 31500:5815 31500:5836 31500:5860 31500:5880 65000:47541 65000:47542 65531:1273
      path 7FE054D83328 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7018 6762 31500 42065, (aggregated by 65500 185.26.72.1)
    12.0.1.63 from 12.0.1.63 (12.0.1.63)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 7018:5000 7018:37232
      path 7FE135262398 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3549 3356 31500 31500 31500 31500 31500 31500 31500 42065, (aggregated by 65500 185.26.72.1)
    208.51.134.254 from 208.51.134.254 (67.16.168.191)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      Community: 3356:2 3356:22 3356:100 3356:123 3356:507 3356:903 3356:2111 3549:2581 3549:30840 31500:10 31500:812 31500:5555 31500:5561 31500:5800 31500:5815 31500:5836 31500:5860 31500:5880
      path 7FE123EBA6B0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  6939 42065, (aggregated by 65500 185.26.72.1)
    64.71.137.241 from 64.71.137.241 (216.218.252.164)
      Origin IGP, localpref 100, valid, external, atomic-aggregate, best
      path 7FE0C11A6C30 RPKI State not found
      rx pathid: 0, tx pathid: 0x0
  Refresh Epoch 1
  3257 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    89.149.178.10 from 89.149.178.10 (213.200.83.26)
      Origin IGP, metric 10, localpref 100, valid, external, atomic-aggregate
      Community: 3257:8052 3257:30244 3257:50001 3257:54900 3257:54901
      path 7FE0D31728C8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3267 31500 42065, (aggregated by 65500 185.26.72.1)
    194.85.40.15 from 194.85.40.15 (185.141.126.1)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      path 7FE17A547428 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7660 2516 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    203.181.248.168 from 203.181.248.168 (203.181.248.168)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 2516:1030 7660:9003
      path 7FE013317088 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  57866 6830 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    37.139.139.17 from 37.139.139.17 (37.139.139.17)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      Community: 1273:12752 6830:17000 6830:17473 6830:33122 17152:1 31500:10 31500:812 31500:5555 31500:5561 31500:5800 31500:5815 31500:5836 31500:5860 31500:5880 57866:501 65000:47541 65000:47542 65531:1273
      path 7FE0D202EB18 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3333 31500 42065, (aggregated by 65500 185.26.72.1)
    193.0.0.56 from 193.0.0.56 (193.0.0.56)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE01FDFE070 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  49788 12552 31500 42065, (aggregated by 65500 185.26.72.1)
    91.218.184.60 from 91.218.184.60 (91.218.184.60)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 12552:12000 12552:12100 12552:12101 12552:22000
      Extended Community: 0x43:100:1
      path 7FE0AE4CA128 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20912 3257 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    212.66.96.126 from 212.66.96.126 (212.66.96.126)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 3257:8070 3257:30352 3257:50001 3257:53900 3257:53902 20912:65004
      path 7FE102616368 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  8283 31500 42065, (aggregated by 65500 185.26.72.1)
    94.142.247.3 from 94.142.247.3 (94.142.247.3)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      Community: 8283:1 8283:101
      unknown transitive attribute: flag 0xE0 type 0x20 length 0x18
        value 0000 205B 0000 0000 0000 0001 0000 205B
              0000 0005 0000 0001 
      path 7FE16F8FEFE8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1221 4637 31500 42065, (aggregated by 65500 185.26.72.1)
    203.62.252.83 from 203.62.252.83 (203.62.252.83)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE12F72EE80 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  852 3257 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    154.11.12.212 from 154.11.12.212 (96.1.209.43)
      Origin IGP, metric 0, localpref 100, valid, external, atomic-aggregate
      path 7FE0FBA032B8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  2497 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    202.232.0.2 from 202.232.0.2 (58.138.96.254)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE11787EF60 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20130 6939 42065, (aggregated by 65500 185.26.72.1)
    140.192.8.16 from 140.192.8.16 (140.192.8.16)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE11939D8B0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  701 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    137.39.3.55 from 137.39.3.55 (137.39.3.55)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE0CE3F9C30 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  53767 14315 6453 6762 31500 42065, (aggregated by 65500 185.26.72.1)
    162.251.163.2 from 162.251.163.2 (162.251.162.3)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 14315:5000 53767:5000
      path 7FE15503B490 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  101 3356 31500 31500 31500 31500 31500 31500 31500 42065, (aggregated by 65500 185.26.72.1)
    209.124.176.223 from 209.124.176.223 (209.124.176.223)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 101:20100 101:20110 101:22100 3356:2 3356:22 3356:100 3356:123 3356:507 3356:903 3356:2111 31500:10 31500:812 31500:5555 31500:5561 31500:5800 31500:5815 31500:5836 31500:5860 31500:5880 65000:47541 65000:47542 65531:1273
      Extended Community: RT:101:22100
      path 7FE0B7D1F5E0 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  19214 3257 1273 31500 42065, (aggregated by 65500 185.26.72.1)
    208.74.64.40 from 208.74.64.40 (208.74.64.40)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      Community: 3257:8044 3257:30398 3257:50002 3257:51200 3257:51201
      path 7FE15D4FB458 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3561 3910 3356 31500 31500 31500 31500 31500 31500 31500 42065, (aggregated by 65500 185.26.72.1)
    206.24.210.80 from 206.24.210.80 (206.24.210.80)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE110379CC8 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1351 6939 42065, (aggregated by 65500 185.26.72.1)
    132.198.255.253 from 132.198.255.253 (132.198.255.253)
      Origin IGP, localpref 100, valid, external, atomic-aggregate
      path 7FE029622AD0 RPKI State not found
      rx pathid: 0, tx pathid: 0
```

### 2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.
```commandline
root@vagrant:~# lsmod | grep dummy
dummy                  16384  0
root@vagrant:~# ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
eth0             UP             08:00:27:73:60:cf <BROADCAST,MULTICAST,UP,LOWER_UP> 
eth1             UP             08:00:27:e3:0f:ac <BROADCAST,MULTICAST,UP,LOWER_UP> 
root@vagrant:~# ip link add dummy0 type dummy
root@vagrant:~# ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
eth0             UP             08:00:27:73:60:cf <BROADCAST,MULTICAST,UP,LOWER_UP> 
eth1             UP             08:00:27:e3:0f:ac <BROADCAST,MULTICAST,UP,LOWER_UP> 
dummy0           DOWN           c2:b3:a2:8a:16:11 <BROADCAST,NOARP> 
root@vagrant:~# ip addr add 10.12.45.56/32 dev dummy0
root@vagrant:~# ip link set dummy0 up
root@vagrant:~# ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
eth0             UP             08:00:27:73:60:cf <BROADCAST,MULTICAST,UP,LOWER_UP> 
eth1             UP             08:00:27:e3:0f:ac <BROADCAST,MULTICAST,UP,LOWER_UP> 
dummy0           UNKNOWN        c2:b3:a2:8a:16:11 <BROADCAST,NOARP,UP,LOWER_UP> 
root@vagrant:~# ip -br addr 
lo               UNKNOWN        127.0.0.1/8 ::1/128 
eth0             UP             10.0.2.15/24 fe80::a00:27ff:fe73:60cf/64 
eth1             UP             10.12.34.61/24 fe80::a00:27ff:fee3:fac/64 
dummy0           UNKNOWN        10.12.45.56/32 fe80::c0b3:a2ff:fe8a:1611/64 
root@vagrant:~# ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
default via 10.12.34.239 dev eth1 proto dhcp src 10.12.34.61 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
10.12.34.0/24 dev eth1 proto kernel scope link src 10.12.34.61 
10.12.34.254 dev eth1 proto dhcp scope link src 10.12.34.61 metric 100 
root@vagrant:~# ip route add 10.2.2.0/24 via 10.12.34.30
root@vagrant:~# ip route add 10.2.3.0/24 via 10.12.34.254
root@vagrant:~# ip route 
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
default via 10.12.34.239 dev eth1 proto dhcp src 10.12.34.61 metric 100 
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100 
10.2.2.0/24 via 10.12.34.30 dev eth1 
10.2.3.0/24 via 10.12.34.254 dev eth1 
10.12.34.0/24 dev eth1 proto kernel scope link src 10.12.34.61 
10.12.34.254 dev eth1 proto dhcp scope link src 10.12.34.61 metric 100 
```

### 3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.
Список открытых TCP-портов:
```commandline
root@vagrant:~# ss -t -a -p -n
State               Recv-Q              Send-Q                             Local Address:Port                             Peer Address:Port               Process                                                                 
LISTEN              0                   4096                                     0.0.0.0:111                                   0.0.0.0:*                   users:(("rpcbind",pid=563,fd=4),("systemd",pid=1,fd=112))              
LISTEN              0                   4096                               127.0.0.53%lo:53                                    0.0.0.0:*                   users:(("systemd-resolve",pid=566,fd=13))                              
LISTEN              0                   128                                      0.0.0.0:22                                    0.0.0.0:*                   users:(("sshd",pid=806,fd=3))                                          
ESTAB               0                   0                                      10.0.2.15:22                                   10.0.2.2:52854               users:(("sshd",pid=1159,fd=4),("sshd",pid=1119,fd=4))                  
LISTEN              0                   4096                                        [::]:111                                      [::]:*                   users:(("rpcbind",pid=563,fd=6),("systemd",pid=1,fd=114))              
LISTEN              0                   128                                         [::]:22                                       [::]:*                   users:(("sshd",pid=806,fd=4))                                          
```
Здесь:
* 111 порт (sunrpc) используется процессом "rpcbind" (определяет адрес, по которому следует отправлять запросы удаленного вызова процедур);
* 53 порт (domain) используется локальной службой разрешения имен "systemd-resolve";
* 22 порт (ssh) слушает (LISTEN) ssh-сервер. Статус ESTAB(LISHED) указывает на установленное ssh-соединение.

Стандартное назначение портов можно посмотреть в файле `/etc/services`.

### 4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?
Список открытых UDP-портов:
```commandline
root@vagrant:~# ss -u -a -p -n
State               Recv-Q              Send-Q                              Local Address:Port                             Peer Address:Port              Process                                                                 
UNCONN              0                   0                                   127.0.0.53%lo:53                                    0.0.0.0:*                  users:(("systemd-resolve",pid=566,fd=12))                              
UNCONN              0                   0                                  10.0.2.15%eth0:68                                    0.0.0.0:*                  users:(("systemd-network",pid=1065,fd=21))                             
UNCONN              0                   0                                10.12.26.61%eth1:68                                    0.0.0.0:*                  users:(("systemd-network",pid=1065,fd=17))                             
UNCONN              0                   0                                         0.0.0.0:111                                   0.0.0.0:*                  users:(("rpcbind",pid=563,fd=5),("systemd",pid=1,fd=113))              
UNCONN              0                   0                                            [::]:111                                      [::]:*                  users:(("rpcbind",pid=563,fd=7),("systemd",pid=1,fd=115))              
```
Здесь:
* 53 порт (domain) используется локальной службой разрешения имен "systemd-resolve";
* 68 порт (bootpc) используется на стороне клиента для автоматической настройки сетевых параметров по протоколу BOOTP, используется подсистемой "systemd-network";
* 111 порт (sunrpc) используется процессом "rpcbind" (определяет адрес, по которому следует отправлять запросы удаленного вызова процедур).

### 5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.
