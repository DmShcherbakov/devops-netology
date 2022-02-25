# 6.3. MySQL - Дмитрий Щербаков

## Задача 1

### Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
```commandline
root@dmhome:/home/dimka/Docker/MySQL# docker run --name dmshch-mysql -v /home/dimka/Docker/MySQL/data/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=gfhjkm -d mysql:8
cfdda03d4ab76956708113c3319dce25453c8a66d607c9401135c82a18c68a1b
root@dmhome:/home/dimka/Docker/MySQL# docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                 NAMES
cfdda03d4ab7   mysql:8   "docker-entrypoint.s…"   5 seconds ago   Up 4 seconds   3306/tcp, 33060/tcp   dmshch-mysql
root@dmhome:/home/dimka/Docker/MySQL# docker exec -it dmshch-mysql mysql --version
mysql  Ver 8.0.28 for Linux on x86_64 (MySQL Community Server - GPL)
root@dmhome:/home/dimka/Docker/MySQL# ls data/
 auto.cnf     ca.pem            client-key.pem      '#ib_16384_1.dblwr'   ib_logfile0   ibtmp1          mysql       performance_schema   public_key.pem    server-key.pem   undo_001
 ca-key.pem   client-cert.pem  '#ib_16384_0.dblwr'   ibdata1              ib_logfile1  '#innodb_temp'   mysql.ibd   private_key.pem      server-cert.pem   sys              undo_002
```
### Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и восстановитесь из него.
```commandline
root@dmhome:/home/dimka/Docker/MySQL# docker exec -it dmshch-mysql bash
root@cfdda03d4ab7:/# mysql -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE test_db;
Query OK, 1 row affected (0.06 sec)

mysql> \q
Bye
root@cfdda03d4ab7:/# mysql -p test_db < /var/lib/mysql/test_dump.sql 
Enter password: 
mysql> SELECT * FROM orders;
+----+-----------------------+-------+
| id | title                 | price |
+----+-----------------------+-------+
|  1 | War and Peace         |   100 |
|  2 | My little pony        |   500 |
|  3 | Adventure mysql times |   300 |
|  4 | Server gravity falls  |   300 |
|  5 | Log gossips           |   123 |
+----+-----------------------+-------+
5 rows in set (0.00 sec)
```
### Перейдите в управляющую консоль `mysql` внутри контейнера.
### Используя команду `\h` получите список управляющих команд.
### Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.
```commandline
mysql> status
--------------
mysql  Ver 8.0.28 for Linux on x86_64 (MySQL Community Server - GPL)
...
Server version:		8.0.28 MySQL Community Server - GPL
...
```
### Подключитесь к восстановленной БД и получите список таблиц из этой БД.
```commandline
root@cfdda03d4ab7:/# mysql -p test_db
Enter password: 
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW TABLES;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0.00 sec)
```
### **Приведите в ответе** количество записей с `price` > 300.
```commandline
mysql> SELECT COUNT(*) FROM orders WHERE price>300;
+----------+
| COUNT(*) |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)
```
### В следующих заданиях мы будем продолжать работу с данным контейнером.

## Задача 2
### Создайте пользователя test в БД c паролем test-pass, используя:
### - плагин авторизации mysql_native_password
### - срок истечения пароля - 180 дней
### - количество попыток авторизации - 3
### - максимальное количество запросов в час - 100
### - аттрибуты пользователя:
###     - Фамилия "Pretty"
###     - Имя "James"
```commandline
mysql> CREATE USER 'test'@'%' IDENTIFIED WITH mysql_native_password BY 'test-pass' PASSWORD EXPIRE INTERVAL 180 DAY FAILED_LOGIN_ATTEMPTS 3 ATTRIBUTE '{"fname": "James", "lname": "Pretty"}';
Query OK, 0 rows affected (0.04 sec)

mysql> ALTER USER 'test'@'%' WITH MAX_QUERIES_PER_HOUR 100;
Query OK, 0 rows affected (0.04 sec)

mysql> SELECT user,plugin,password_lifetime,User_attributes,max_questions FROM mysql.user WHERE user='test';
+------+-----------------------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------+---------------+
| user | plugin                | password_lifetime | User_attributes                                                                                                                     | max_questions |
+------+-----------------------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------+---------------+
| test | mysql_native_password |               180 | {"metadata": {"fname": "James", "lname": "Pretty"}, "Password_locking": {"failed_login_attempts": 3, "password_lock_time_days": 0}} |           300 |
+------+-----------------------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------+---------------+
1 row in set (0.00 sec)
```
### Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
```commandline
mysql> GRANT SELECT ON test_db.* TO 'test'@'%';
Query OK, 0 rows affected (0.04 sec)
```
### Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и **приведите в ответе к задаче**.
```commandline
mysql> select * from INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER='test';
+------+------+---------------------------------------+
| USER | HOST | ATTRIBUTE                             |
+------+------+---------------------------------------+
| test | %    | {"fname": "James", "lname": "Pretty"} |
+------+------+---------------------------------------+
1 row in set (0.00 sec)
```

## Задача 3

### Установите профилирование `SET profiling = 1`.
### Изучите вывод профилирования команд `SHOW PROFILES;`.

### Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

### Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
### - на `MyISAM`
### - на `InnoDB`

