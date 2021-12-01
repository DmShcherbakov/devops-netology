# 3.7. Компьютерные сети, лекция 2 - Дмитрий Щербаков
### 1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?
В ОС Ubuntu список интерфейсов можно получить следующими способами:
```commandline
$ ip -br link
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
enp4s0           UP             1c:6f:65:d1:96:e5 <BROADCAST,MULTICAST,UP,LOWER_UP> 
tun0             UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> 
$ ip -br a s
lo               UNKNOWN        127.0.0.1/8 ::1/128 
enp7s0           UP             192.168.0.101/24 
tun0             UNKNOWN        10.9.0.1 peer 10.9.0.2/32 fe80::c645:1784:b8bb:38a8/64 
$ ifconfig 
enp7s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.101  netmask 255.255.255.0  broadcast 192.168.0.255
        ether f0:2f:74:16:45:d9  txqueuelen 1000  (Ethernet)
        RX packets 133231192  bytes 51121397636 (51.1 GB)
        RX errors 0  dropped 29872  overruns 0  frame 0
        TX packets 191289793  bytes 252245659954 (252.2 GB)
        TX errors 64  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Локальная петля (Loopback))
        RX packets 49375437  bytes 20650957811 (20.6 GB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 49375437  bytes 20650957811 (20.6 GB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.9.0.1  netmask 255.255.255.255  destination 10.9.0.2
        inet6 fe80::c645:1784:b8bb:38a8  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 4643013  bytes 3690561015 (3.6 GB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4557377  bytes 1130453741 (1.1 GB)
        TX errors 0  dropped 151 overruns 0  carrier 0  collisions 0
$ dpkg -S `which ifconfig`
net-tools: /sbin/ifconfig
```
В последних версиях Linux для использования утилиты `ifconfig` необходимо устанавливать пакет net-tools.

В Windows список интерфейсов можно получить в том или ином виде следующими способами (не считая GUI):
```commandline
C:\Users\User>getmac

Физический адрес    Имя транспорта
=================== ==========================================================
44-1E-A1-D0-AF-06 \Device\Tcpip_{25C2AD66-B45F-41B9-A2BA-DB8C3B20806C}
E0-2A-82-FE-72-6D   Носитель отключен
AC-81-12-B9-95-5A   Носитель отключен
AA-15-0B-02-26-CF \Device\Tcpip_{476BD5F6-873D-433A-85A6-B5FB6FAE766A}
00-FF-18-99-EC-FF \Device\Tcpip_{1899ECFF-8197-4F24-9038-424F761A031E}
00-FF-7D-29-9E-B6   Носитель отключен
Н/Д                 Носитель отключен

C:\Users\User>netsh interface show interface

Состояние адм.  Состояние     Тип              Имя интерфейса
---------------------------------------------------------------------
Разрешен       Подключен      Выделенный       Подключение по локальной сети
Разрешен       Отключен       Выделенный       Подключение по локальной сети 2
Разрешен       Отключен       Выделенный       OpenVPN Wintun
Разрешен       Подключен      Выделенный       Ethernet
Разрешен       Отключен       Выделенный       Беспроводная сеть
Разрешен       Подключен      Выделенный       vEthernet (Default Switch)


C:\Users\User>ipconfig

Настройка протокола IP для Windows


Неизвестный адаптер OpenVPN Wintun:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер Ethernet Ethernet:

   DNS-суффикс подключения . . . . . : 
   IPv4-адрес. . . . . . . . . . . . : 10.12.26.31
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . : 10.12.26.254
...
```

### 2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?
Для распознавания соседей по сетевому интерфейсу существуют такие протоколы, как lldp или cdp. В операционной системе Linux для этого есть пакет lldpd. Запустив сервис, можно увидеть, информацию о соседях. Например (при включенной поддержке llpd на коммутаторе):
```commandline
$ lldpctl 
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------
Interface:    enp4s0, via: LLDP, RID: 1, Time: 0 day, 00:00:06
  Chassis:     
    ChassisID:    mac c8:f9:f9:81:a6:80
    SysName:      abc.def.ghi
    SysDescr:     Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE11, RELEASE SOFTWARE (fc3)
                  Technical Support: http://www.cisco.com/techsupport
                  Copyright (c) 1986-2016 by Cisco Systems, Inc.
                  Compiled Wed 17-Aug-16 13:46 by prod_rel_team
    MgmtIP:       192.168.123.123
    Capability:   Bridge, on
  Port:        
    PortID:       ifname Gi0/1
    PortDescr:    GigabitEthernet0/1
    TTL:          120
    PMD autoneg:  supported: yes, enabled: yes
      Adv:          10Base-T, HD: yes, FD: yes
      Adv:          100Base-TX, HD: yes, FD: yes
      Adv:          1000Base-T, HD: no, FD: yes
      MAU oper type: 1000BaseTFD - Four-pair Category 5 UTP, full duplex mode
  VLAN:         123, pvid: yes
-------------------------------------------------------------------------------
```
Со стороны коммутатора станция при этом отображается следующим образом:
```commandline
#sh lldp neighbors 
Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

Device ID           Local Intf     Hold-time  Capability      Port ID
dm                  Gi0/1          120        B,R             1c6f.65d1.96e5

Total entries displayed: 1
```

### 3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.
Для разделения L2 коммутатора на несколько виртуальных сетей служит технология VLAN (Virtual Local Area Network). Наиболее распространенный открытый стандарт данной технологии - IEEE 802.1q (есть также проприетарные решения, например Cisco ISL). При использовании VLAN, в состав кадра добавляется дополнительный тег, в котором содержится информация об используемом протоколе, идентификаторе сети (VLAN) и другая служебная информация (например, PCP для приоретизации трафика, CFI для индикации формата MAC-адреса).
Для использования vlan в Linux может потребоваться пакет `vlan`. Конкретно в моем дистрибутиве (Ubuntu 20.04.3 LTS), необходимый модуль входит в пакет linux-modules:
```commandline
root@dm:~# dpkg -l | grep -i vlan
root@dm:~# lsmod | grep 8021q
8021q                  32768  0
garp                   16384  1 8021q
mrp                    20480  1 8021q
root@dm:~# find /lib/ -name 8021q.ko
/lib/modules/5.4.0-91-generic/kernel/net/8021q/8021q.ko
/lib/modules/5.4.0-90-generic/kernel/net/8021q/8021q.ko
/lib/modules/5.3.0-18-generic/kernel/net/8021q/8021q.ko
root@dm:~# dpkg -S /lib/modules/5.4.0-91-generic/kernel/net/8021q/8021q.ko
linux-modules-5.4.0-91-generic: /lib/modules/5.4.0-91-generic/kernel/net/8021q/8021q.ko
```

В зависимости от того, какая система управления сетевыми соединениями используется, конфигурация может выглядеть следующим образом:
- NetworkManager:
```commandline
root@dm:/etc/NetworkManager/system-connections# cat Wired\ connection\ 1.nmconnection 
[connection]
id=Wired connection 1
uuid=ecd57f83-2726-315f-955a-0d8bfd0e4a2d
type=ethernet
autoconnect-priority=-999
interface-name=enp4s0
permissions=
timestamp=1571811285

[ethernet]
mac-address-blacklist=

[ipv4]
address1=10.12.26.123/24,10.12.26.254
dns=10.1.2.3;10.1.2.4;
dns-search=local;
method=manual

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
ip6-privacy=0
method=auto

[proxy]

root@dm:/etc/NetworkManager/system-connections# cat Vlan1000.nmconnection 
[connection]
id=Vlan1000
uuid=e59f567c-0205-4aa1-9c71-7289b70028cc
type=vlan
autoconnect=false
interface-name=Vlan1000
permissions=
timestamp=1636454530

[ethernet]
mac-address-blacklist=

[vlan]
egress-priority-map=
flags=1
id=1000
ingress-priority-map=
parent=enp4s0

[ipv4]
address1=192.168.123.123/24
dns-search=
method=auto

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
ip6-privacy=0
method=auto

[proxy]
root@dm:/etc/NetworkManager/system-connections# nmcli conn up Vlan1000
Соединение успешно активировано (адрес действующего D-Bus: /org/freedesktop/NetworkManager/ActiveConnection/6)
root@dm:/etc/NetworkManager/system-connections# ip -br a s
lo               UNKNOWN        127.0.0.1/8 ::1/128 
enp4s0           UP             10.12.26.123/24 fe80::1f6c:9cbf:e1b4:98a8/64 
...
Vlan1000@enp4s0    UP             192.168.123.123/24 fe80::2bbd:837c:c5c0:d05e/64 
```
- netplan (systemd-networkd):
```commandline
root@dm:~# cat /etc/netplan/01-network-manager-all.yaml
# Let NetworkManager manage all devices on this system
network:
    version: 2
    renderer: networkd
    ethernets:
        enp4s0:
            dhcp4: no
            addresses: [10.12.26.123/24]
            gateway4: 10.12.26.254
            mtu: 1500
            nameservers:
                addresses:
                    - 10.1.2.3
                    - 10.1.2.4
                search: [ local ]
    vlans: 
        Vlan1000:
            id: 1000
            link: enp4s0
            dhcp4: no
            addresses: [192.168.123.123/24]
root@dm:~# ip -br a s
lo               UNKNOWN        127.0.0.1/8 ::1/128 
enp4s0           UP             10.12.26.123/24 fe80::1e6f:65ff:fed1:96e5/64 
Vlan1000@enp4s0  UP             192.168.123.123/24 fe80::1e6f:65ff:fed1:96e5/64 
oot@dm:~# arp -an
? (192.168.123.100) в b8:af:67:04:6c:22 [ether] на Vlan1000
? (10.12.26.254) в a8:b4:56:7a:10:80 [ether] на enp4s0
? (192.168.123.200) в 00:50:56:8c:6b:d9 [ether] на Vlan1000
? (10.12.26.13) в 6c:f0:49:e5:a5:21 [ether] на enp4s0
```
Здесь мы можем видеть, что в ARP-таблице присутствуют записи на соответствующих интерфейсах.
В представленных примерах, на хосте настроены два интерфейса, из которых один работает с нетегированным трафиком (не привязан к VLAN ID), а второй - с пакетами, предназначенными для Vlan c идентификатором 1000.
На коммутаторе в этих целях кроме списка тегированных VLAN, передаваемых на порт, следует указать PVID (native vlan) - номер VLANа, который будет передаваться без тегов:
```commandline
#sh run int gi0/1
Building configuration...

Current configuration : 328 bytes
!
interface GigabitEthernet0/1
 description DM 
 switchport trunk native vlan 153
 switchport trunk allowed vlan 57,153,1000
 switchport mode trunk
 spanning-tree portfast
 spanning-tree bpdufilter enable
end
```

### 4.  Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.
Объединение сетевых карт в Linux можно осуществить с помощью драйвера bonding, он предоставляет методы для агрегирования нескольких сетевых интерфейсов в один логический. Поведение связанных интерфейсов зависит от режима. В общем случае, объединенные интерфейсы могут работать в режиме горячего резерва (отказоустойчивости) или в режиме балансировки нагрузки.

| Режим             | Описание| 
|:------------------|---------|
| balance-rr или 0  |Политика round-robin. Пакеты отправляются последовательно, начиная с первого доступного интерфейса и заканчивая последним. Эта политика применяется для балансировки нагрузки и отказоустойчивости|
| active-backup или 1 |	Политика активный-резервный. Только один сетевой интерфейс из объединённых будет активным. Другой интерфейс может стать активным, только в том случае, когда упадёт текущий активный интерфейс. При такой политике MAC адрес bond интерфейса виден снаружи только через один сетевой порт, во избежание появления проблем с коммутатором. Эта политика применяется для отказоустойчивости.|
balance-xor или 2 |Политика XOR. Передача распределяется между сетевыми картами используя формулу: [( «MAC адрес источника» XOR «MAC адрес назначения») по модулю «число интерфейсов»]. Получается одна и та же сетевая карта передаёт пакеты одним и тем же получателям. Опционально распределение передачи может быть основано и на политике «xmit_hash».  Политика XOR применяется для балансировки нагрузки и отказоустойчивости. 
 broadcast или 3 | Широковещательная политика. Передает всё на все сетевые интерфейсы. Эта политика применяется для отказоустойчивости.
 802.3ad или 4 | Политика агрегирования каналов по стандарту IEEE 802.3ad. Создаются агрегированные группы сетевых карт с одинаковой скоростью и дуплексом. При таком объединении передача задействует все каналы в активной агрегации, согласно стандарту IEEE 802.3ad. Выбор через какой интерфейс отправлять пакет определяется политикой, по умолчанию XOR политика, можно использовать «xmit_hash» политику. 
 balance-tlb или 5 | Политика адаптивной балансировки нагрузки передачи. Исходящий трафик распределяется в зависимости от загруженности каждой сетевой карты (определяется скоростью загрузки). Не требует дополнительной настройки на коммутаторе. Входящий трафик приходит на текущую сетевую карту. Если она выходит из строя, то другая сетевая карта берёт себе MAC адрес вышедшей из строя карты. 
 balance-alb или 6 | Политика адаптивной балансировки нагрузки. Включает в себя политику balance-tlb плюс осуществляет балансировку входящего трафика. Не требует дополнительной настройки на коммутаторе. Балансировка входящего трафика достигается путём ARP переговоров. Драйвер bonding перехватывает ARP ответы, отправляемые с локальных сетевых карт наружу, и переписывает MAC адрес источника на один из уникальных MAC адресов сетевой карты, участвующей в объединении. Таким образом различные пиры используют различные MAC адреса сервера. Балансировка входящего трафика распределяется последовательно (round-robin) между интерфейсами.

В качестве примера агрегации по протоколу LACP (IEEE 802.1ad) можно привести следующий конфиг:
```commandline
# cat /etc/netplan/00-installer-config.yaml 
# This is the network config written by 'subiquity'
network:
  bonds:
    bond0:
      addresses:
      - 10.12.1.189/24
      gateway4: 10.12.1.254
      interfaces:
      - eno1
      - eno2
      nameservers:
        addresses:
        - 10.1.2.3
        - 10.1.2.4
        search:
        - local
      parameters:
        mode: 802.3ad 
    bond1:
      addresses:
      - 10.13.0.189/24
      interfaces:
      - eno3
      - eno4
      nameservers:
        addresses: []
        search: []
      parameters:
        mode: 802.3ad
  ethernets:
    eno1: {}
    eno2: {}
    eno3: {}
    eno4: {}
    enx0a94ef5572b1:
      dhcp4: true
  version: 2
```
В данном примере на сервере с четырьмя сетевыми интерфейсами собраны два "бонда" по две сетевые карты. Со стороны коммутатора при этом настройка для агрегированного канала выглядит следующим образом:
```commandline
SWITCH#sh etherchannel 2 summary 
...
Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
2      Po2(SU)         LACP        Tw1/0/5(P)    Tw2/0/5(P)    

SWITCH#sh run int tw1/0/5
Building configuration...

Current configuration : 145 bytes
!
interface TwoGigabitEthernet1/0/5
 description bond0
 switchport access vlan 123
 channel-protocol lacp
 channel-group 2 mode active
end

dobro-new#sh run int tw2/0/5
Building configuration...

Current configuration : 145 bytes
!
interface TwoGigabitEthernet2/0/5
 description bond0
 switchport access vlan 123
 channel-protocol lacp
 channel-group 2 mode active
end

dobro-new#sh int po2
Port-channel2 is up, line protocol is up (connected) 
  Hardware is EtherChannel, address is 0c75.bd55.0705 (bia 0c75.bd55.0705)
  Description: bond0
  MTU 1500 bytes, BW 2000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
...
```

### 5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
В сети с маской /29 находится 8 адресов. Из них один - адрес сети, еще один - широковещательный адрес, оставшиеся 6 можно использовать для назначения хостам.

В сети /24 доступны 256 адресов (с 0 по 255), разделив на "емкость" сети /29, получим: `256/8=32`.

В качестве примеров сетей /29, пожно привести следующие:
```commandline
$ for i in {0,8,16,24}; do ipcalc 10.10.10.$i/29; done
Address:   10.10.10.0           00001010.00001010.00001010.00000 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.0/29        00001010.00001010.00001010.00000 000
HostMin:   10.10.10.1           00001010.00001010.00001010.00000 001
HostMax:   10.10.10.6           00001010.00001010.00001010.00000 110
Broadcast: 10.10.10.7           00001010.00001010.00001010.00000 111
Hosts/Net: 6                     Class A, Private Internet

Address:   10.10.10.8           00001010.00001010.00001010.00001 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.8/29        00001010.00001010.00001010.00001 000
HostMin:   10.10.10.9           00001010.00001010.00001010.00001 001
HostMax:   10.10.10.14          00001010.00001010.00001010.00001 110
Broadcast: 10.10.10.15          00001010.00001010.00001010.00001 111
Hosts/Net: 6                     Class A, Private Internet

Address:   10.10.10.16          00001010.00001010.00001010.00010 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.16/29       00001010.00001010.00001010.00010 000
HostMin:   10.10.10.17          00001010.00001010.00001010.00010 001
HostMax:   10.10.10.22          00001010.00001010.00001010.00010 110
Broadcast: 10.10.10.23          00001010.00001010.00001010.00010 111
Hosts/Net: 6                     Class A, Private Internet

Address:   10.10.10.24          00001010.00001010.00001010.00011 000
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   10.10.10.24/29       00001010.00001010.00001010.00011 000
HostMin:   10.10.10.25          00001010.00001010.00001010.00011 001
HostMax:   10.10.10.30          00001010.00001010.00001010.00011 110
Broadcast: 10.10.10.31          00001010.00001010.00001010.00011 111
Hosts/Net: 6                     Class A, Private Internet
```

### 6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.
В данном случае, можно воспользоваться диапазоном адресов 100.64.0.0/10. Для 40-50 хостов требуется маска /26 (255.255.255.192), содержащая 64 адреса (для 62 хостов).

### 7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?
Действие|В ОС Linux: | В ОС Windows:
---|---|---
посмотреть ARP-таблицу: | `arp` | `arp -a`
очистить ARP кеш полностью: | `sudo ip -s -s neigh flush all` | `netsh interface ip delete arpcache` или `arp -d *` с правами администратора
удалить только один нужный IP: | `sudo arp -d address` |  `arp -d address` с правами администратора

Пример работы в Linux:
```commandline
$ arp -n
Адрес HW-тип HW-адрес Флаги Маска Интерфейс
10.12.26.254             ether   a8:b4:56:7a:10:80   C                     enp4s0
10.12.26.32              ether   1c:1b:0d:e4:04:dd   C                     enp4s0
10.12.26.13              ether   6c:f0:49:e5:a5:21   C                     enp4s0

$ arp -d 10.12.26.32
SIOCDARP(dontpub): Операция не позволена
$ sudo arp -d 10.12.26.32
$ arp -n
Адрес HW-тип HW-адрес Флаги Маска Интерфейс
10.12.26.254             ether   a8:b4:56:7a:10:80   C                     enp4s0
10.12.26.13              ether   6c:f0:49:e5:a5:21   C                     enp4s0

$ sudo ip -s -s neigh flush all
10.12.26.254 dev enp4s0 lladdr a8:b4:56:7a:10:80 ref 1 used 681/0/681 probes 4 REACHABLE
10.12.26.13 dev enp4s0 lladdr 6c:f0:49:e5:a5:21 used 271/265/234 probes 1 STALE

*** Round 1, deleting 2 entries ***
*** Flush is complete after 1 round ***
14:56:21 dim@dm:~/Work_documents$ arp -n
Адрес HW-тип HW-адрес Флаги Маска Интерфейс
10.12.26.254             ether   a8:b4:56:7a:10:80   C                     enp4s0
```
