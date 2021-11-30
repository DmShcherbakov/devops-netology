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
Для распознавания соседей по сетевому интерфейсу существуют такие протоколы, как lldp или cdp. В операционной системе Linux для этого есть пакет lldpd. Запустив сервис, можно увидеть, информацию о соседях. Например:
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
    MgmtIP:       192.168.255.196
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
