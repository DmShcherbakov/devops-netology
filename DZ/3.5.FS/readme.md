# 3.5. Файловые системы - Дмитрий Щербаков

### 1. Узнайте о sparse (разряженных) файлах.
Материал изучен.

### 2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
Нет, не могут. Все жесткие ссылки указывают на одну и ту же inode, свойства которой содержат, кроме прочего, права доступа и владельца.

### 3. Сделайте vagrant destroy на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:
```commandline
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provider :virtualbox do |vb|
    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
  end
end
```
### Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.
После выполнения указанных манипуляций и запуска, в виртуальной машине имеем:
```commandline
vagrant@vagrant:~$ lsblk 
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
sdc                    8:32   0  2.5G  0 disk 
```

### 4. Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
```commandline
vagrant@vagrant:~$ sudo fdisk /dev/sdb

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 
First sector (2048-5242879, default 2048): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G

Created a new partition 1 of type 'Linux' and of size 2 GiB.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 
First sector (4196352-5242879, default 4196352): 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879): 

Created a new partition 2 of type 'Linux' and of size 511 MiB.

Command (m for help): p
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x7c9f99e5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux

Command (m for help): wq
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.

vagrant@vagrant:~$ sudo fdisk -l /dev/sdb
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x7c9f99e5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```

### 5. Используя sfdisk, перенесите данную таблицу разделов на второй диск.
```commandline
vagrant@vagrant:~$ sudo fdisk -l /dev/sdc
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb > parts.lst
vagrant@vagrant:~$ sudo sfdisk /dev/sdc < parts.lst 
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new DOS disklabel with disk identifier 0x7c9f99e5.
/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
/dev/sdc3: Done.

New situation:
Disklabel type: dos
Disk identifier: 0x7c9f99e5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
vagrant@vagrant:~$ sudo fdisk -l /dev/sdc
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x7c9f99e5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux
```

### 6. Соберите mdadm RAID1 на паре разделов 2 Гб.
```commandline
vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md0 -l 1 -n 2 /dev/sd{b,c}1
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 2094080K
Continue creating array? yes
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.

vagrant@vagrant:~$ cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid1 sdc1[1] sdb1[0]
      2094080 blocks super 1.2 [2/2] [UU]
      
unused devices: <none>
```

### 7. Соберите mdadm RAID0 на второй паре маленьких разделов.
```commandline
vagrant@vagrant:~$ sudo mdadm --create --verbose /dev/md1 -l 0 -n 2 /dev/sd{b,c}2
mdadm: chunk size defaults to 512K
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
vagrant@vagrant:~$ cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md1 : active raid0 sdc2[1] sdb2[0]
      1042432 blocks super 1.2 512k chunks
      
md0 : active raid1 sdc1[1] sdb1[0]
      2094080 blocks super 1.2 [2/2] [UU]
      
unused devices: <none>
```

### 8. Создайте 2 независимых PV на получившихся md-устройствах.
```commandline
root@vagrant:~# pvdisplay 
  --- Physical volume ---
  PV Name               /dev/sda5
  VG Name               vgvagrant
  PV Size               <63.50 GiB / not usable 0   
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              16255
  Free PE               0
  Allocated PE          16255
  PV UUID               Mx3LcA-uMnN-h9yB-gC2w-qm7w-skx0-OsTz9z
   
root@vagrant:~# pvcreate /dev/md0
  Physical volume "/dev/md0" successfully created.
root@vagrant:~# pvcreate /dev/md1
  Physical volume "/dev/md1" successfully created.
root@vagrant:~# pvdisplay 
  --- Physical volume ---
  PV Name               /dev/sda5
  VG Name               vgvagrant
  PV Size               <63.50 GiB / not usable 0   
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              16255
  Free PE               0
  Allocated PE          16255
  PV UUID               Mx3LcA-uMnN-h9yB-gC2w-qm7w-skx0-OsTz9z
   
  "/dev/md0" is a new physical volume of "<2.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/md0
  VG Name               
  PV Size               <2.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               NYZvh5-AUb4-3K1O-Osew-zliJ-HGv0-tSrqxm
   
  "/dev/md1" is a new physical volume of "1018.00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/md1
  VG Name               
  PV Size               1018.00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               GTY0Fy-C7RY-6GKY-Cknr-p6Wl-O9NC-xZeq9W
```

### 9. Создайте общую volume-group на этих двух PV.
```commandline
root@vagrant:~# vgdisplay 
  --- Volume group ---
  VG Name               vgvagrant
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <63.50 GiB
  PE Size               4.00 MiB
  Total PE              16255
  Alloc PE / Size       16255 / <63.50 GiB
  Free  PE / Size       0 / 0   
  VG UUID               PaBfZ0-3I0c-iIdl-uXKt-JL4K-f4tT-kzfcyE
   
root@vagrant:~# vgcreate netology_dz /dev/md0 /dev/md1
  Volume group "netology_dz" successfully created
root@vagrant:~# vgdisplay 
  --- Volume group ---
  VG Name               vgvagrant
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <63.50 GiB
  PE Size               4.00 MiB
  Total PE              16255
  Alloc PE / Size       16255 / <63.50 GiB
  Free  PE / Size       0 / 0   
  VG UUID               PaBfZ0-3I0c-iIdl-uXKt-JL4K-f4tT-kzfcyE
   
  --- Volume group ---
  VG Name               netology_dz
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               <2.99 GiB
  PE Size               4.00 MiB
  Total PE              765
  Alloc PE / Size       0 / 0   
  Free  PE / Size       765 / <2.99 GiB
  VG UUID               YrN7X1-2q8K-29sY-iZfX-55cD-ss08-ej8vn0
```

### 10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
```commandline
root@vagrant:~# lvcreate -L100 -n ndz_lv netology_dz /dev/md1 
  Logical volume "ndz_lv" created.
root@vagrant:~# lvdisplay 
  --- Logical volume ---
  LV Path                /dev/vgvagrant/root
  LV Name                root
  VG Name                vgvagrant
  LV UUID                ybvP3g-N4gJ-FMMr-WfRk-Ermg-cftw-In20VW
  LV Write Access        read/write
  LV Creation host, time vagrant, 2021-07-28 17:45:53 +0000
  LV Status              available
  # open                 1
  LV Size                <62.54 GiB
  Current LE             16010
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
  --- Logical volume ---
  LV Path                /dev/vgvagrant/swap_1
  LV Name                swap_1
  VG Name                vgvagrant
  LV UUID                GoQVTk-fU79-pbTZ-vX0W-9DbL-p7OI-XCSHPj
  LV Write Access        read/write
  LV Creation host, time vagrant, 2021-07-28 17:45:53 +0000
  LV Status              available
  # open                 2
  LV Size                980.00 MiB
  Current LE             245
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
   
  --- Logical volume ---
  LV Path                /dev/netology_dz/ndz_lv
  LV Name                ndz_lv
  VG Name                netology_dz
  LV UUID                z1Xn2E-8GF6-GnXf-iK3s-Mxf8-5Ofy-ACTvn1
  LV Write Access        read/write
  LV Creation host, time vagrant, 2021-11-27 12:26:58 +0000
  LV Status              available
  # open                 0
  LV Size                100.00 MiB
  Current LE             25
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     4096
  Block device           253:2
  
root@vagrant:~# lsblk 
NAME                     MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                        8:0    0   64G  0 disk  
├─sda1                     8:1    0  512M  0 part  /boot/efi
├─sda2                     8:2    0    1K  0 part  
└─sda5                     8:5    0 63.5G  0 part  
  ├─vgvagrant-root       253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1     253:1    0  980M  0 lvm   [SWAP]
sdb                        8:16   0  2.5G  0 disk  
├─sdb1                     8:17   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
└─sdb2                     8:18   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
    └─netology_dz-ndz_lv 253:2    0  100M  0 lvm   
sdc                        8:32   0  2.5G  0 disk  
├─sdc1                     8:33   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
└─sdc2                     8:34   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
    └─netology_dz-ndz_lv 253:2    0  100M  0 lvm 
```

### 11. Создайте mkfs.ext4 ФС на получившемся LV.
```commandline
root@vagrant:~# mkfs.ext4 /dev/netology_dz/ndz_lv 
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```

### 12. Смонтируйте этот раздел в любую директорию, например, /tmp/new
```commandline
root@vagrant:~# mkdir /tmp/new
root@vagrant:~# mount /dev/netology_dz/ndz_lv /tmp/new/
root@vagrant:~# mount | grep tmp/new
/dev/mapper/netology_dz-ndz_lv on /tmp/new type ext4 (rw,relatime,stripe=256)
root@vagrant:~# ls /tmp/new/
lost+found
```

### 13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.
```commandline
root@vagrant:~# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2021-11-27 12:35:08--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22616192 (22M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz                                            100%[========================================================================================================================================>]  21.57M  10.4MB/s    in 2.1s    

2021-11-27 12:35:11 (10.4 MB/s) - ‘/tmp/new/test.gz’ saved [22616192/22616192]

root@vagrant:~# ls /tmp/new/
lost+found  test.gz
```

### 14. Прикрепите вывод `lsblk`.
```commandline
root@vagrant:~# lsblk 
NAME                     MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                        8:0    0   64G  0 disk  
├─sda1                     8:1    0  512M  0 part  /boot/efi
├─sda2                     8:2    0    1K  0 part  
└─sda5                     8:5    0 63.5G  0 part  
  ├─vgvagrant-root       253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1     253:1    0  980M  0 lvm   [SWAP]
sdb                        8:16   0  2.5G  0 disk  
├─sdb1                     8:17   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
└─sdb2                     8:18   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
    └─netology_dz-ndz_lv 253:2    0  100M  0 lvm   /tmp/new
sdc                        8:32   0  2.5G  0 disk  
├─sdc1                     8:33   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
└─sdc2                     8:34   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
    └─netology_dz-ndz_lv 253:2    0  100M  0 lvm   /tmp/new
```

### 15. Протестируйте целостность файла:
```commandline
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~# echo $?
0
```
В моем случае, вывод аналогичен:
```commandline
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~# echo $?
0
```

### 16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.
```commandline
root@vagrant:~# pvmove -n ndz_lv /dev/md1 /dev/md0 
  /dev/md1: Moved: 12.00%
  /dev/md1: Moved: 100.00%
root@vagrant:~# lsblk 
NAME                     MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                        8:0    0   64G  0 disk  
├─sda1                     8:1    0  512M  0 part  /boot/efi
├─sda2                     8:2    0    1K  0 part  
└─sda5                     8:5    0 63.5G  0 part  
  ├─vgvagrant-root       253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1     253:1    0  980M  0 lvm   [SWAP]
sdb                        8:16   0  2.5G  0 disk  
├─sdb1                     8:17   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
│   └─netology_dz-ndz_lv 253:2    0  100M  0 lvm   /tmp/new
└─sdb2                     8:18   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
sdc                        8:32   0  2.5G  0 disk  
├─sdc1                     8:33   0    2G  0 part  
│ └─md0                    9:0    0    2G  0 raid1 
│   └─netology_dz-ndz_lv 253:2    0  100M  0 lvm   /tmp/new
└─sdc2                     8:34   0  511M  0 part  
  └─md1                    9:1    0 1018M  0 raid0 
root@vagrant:~# ls /tmp/new/
lost+found  test.gz
```

### 17. Сделайте --fail на устройство в вашем RAID1 md.
```commandline
root@vagrant:~# cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md1 : active raid0 sdc2[1] sdb2[0]
      1042432 blocks super 1.2 512k chunks
      
md0 : active raid1 sdc1[1] sdb1[0]
      2094080 blocks super 1.2 [2/2] [UU]
      
unused devices: <none>
root@vagrant:~# mdadm /dev/md0 --fail /dev/sdc1 
mdadm: set /dev/sdc1 faulty in /dev/md0
root@vagrant:~# cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md1 : active raid0 sdc2[1] sdb2[0]
      1042432 blocks super 1.2 512k chunks
      
md0 : active raid1 sdc1[1](F) sdb1[0]
      2094080 blocks super 1.2 [2/1] [U_]
      
unused devices: <none>
```

### 18. Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии.
```commandline
root@vagrant:~# dmesg | tail -2
[ 6223.118021] md/raid1:md0: Disk failure on sdc1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.
```

### 19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:
```commandline
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~# echo $?
0
```
Мой вывод соответствует указанному в примере:
```commandline
root@vagrant:~# gzip -t /tmp/new/test.gz
root@vagrant:~#  echo $?
0
```

### 20. Погасите тестовый хост, vagrant destroy.
```commandline
root@vagrant:~# poweroff
Connection to 127.0.0.1 closed by remote host.
Connection to 127.0.0.1 closed.
dimka@dmhome:~/Nextcloud/Обмен/Netology_DZ/vagr_file$ vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Destroying VM and associated drives...
```
