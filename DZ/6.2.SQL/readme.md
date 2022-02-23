# 6.2. SQL - Дмитрий Щербаков

## Задача 1

### Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, в который будут складываться данные БД и бэкапы.
### Приведите получившуюся команду или docker-compose манифест.
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker run -d --name dmshch-postgres -e POSTGRES_PASSWORD=gfhjkm -e PGDATA=/var/lib/postgresql/data/pgdata -v /home/dimka/Docker/SQL/data:/var/lib/postgresql/data -v /home/dimka/Docker/SQL/backup/:/var/lib/postgresql/backup postgres:12
05d0874b4dad501d97a30ea669cf69c465d1300a3298a828d98294da71abf1f9
root@dmhome:/home/dimka/Docker/SQL# docker exec -it dmshch-postgres psql --version
psql (PostgreSQL) 12.10 (Debian 12.10-1.pgdg110+1)
root@dmhome:/home/dimka/Docker/SQL# ls data/pgdata/
base    pg_commit_ts  pg_hba.conf    pg_logical    pg_notify    pg_serial     pg_stat      pg_subtrans  pg_twophase  pg_wal   postgresql.auto.conf  postmaster.opts
global  pg_dynshmem   pg_ident.conf  pg_multixact  pg_replslot  pg_snapshots  pg_stat_tmp  pg_tblspc    PG_VERSION   pg_xact  postgresql.conf       postmaster.pid
```

## Задача 2

### В БД из задачи 1:
### - создайте пользователя test-admin-user и БД test_db
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker exec -it dmshch-postgres psql -U postgres
psql (12.10 (Debian 12.10-1.pgdg110+1))
Type "help" for help.

postgres=# CREATE USER "test-admin-user" WITH PASSWORD 'Password';
CREATE ROLE
postgres=# CREATE DATABASE test_db;
CREATE DATABASE
```
### - в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
```commandline
postgres=# \connect test_db
You are now connected to database "test_db" as user "postgres".
test_db=# CREATE TABLE orders (id serial primary key, наименование varchar(255), цена integer);
CREATE TABLE
test_db=# CREATE TABLE clients (id serial primary key, фамилия varchar(255), "страна проживания" varchar(30), заказ integer, FOREIGN KEY (заказ) REFERENCES orders (id));
CREATE TABLE
```
### - предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
```commandline
test_db=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "test-admin-user";
GRANT
```
### - создайте пользователя test-simple-user
```commandline
test_db=# CREATE USER "test-simple-user" WITH PASSWORD 'SimplePassword';
CREATE ROLE
```
### - предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db
```commandline
test_db=# GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO "test-simple-user";
GRANT
```
### Таблица orders:
### - id (serial primary key)
### - наименование (string)
### - цена (integer)

### Таблица clients:
### - id (serial primary key)
### - фамилия (string)
### - страна проживания (string, index)
### - заказ (foreign key orders)

### Приведите:
### - итоговый список БД после выполнения пунктов выше,
```commandline
test_db=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)
```
### - описание таблиц (describe)
```commandline
test_db=# \d orders;
                                       Table "public.orders"
    Column    |          Type          | Collation | Nullable |              Default               
--------------+------------------------+-----------+----------+------------------------------------
 id           | integer                |           | not null | nextval('orders_id_seq'::regclass)
 наименование | character varying(255) |           |          | 
 цена         | integer                |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)

test_db=# \d clients;
                                         Table "public.clients"
      Column       |          Type          | Collation | Nullable |               Default               
-------------------+------------------------+-----------+----------+-------------------------------------
 id                | integer                |           | not null | nextval('clients_id_seq'::regclass)
 фамилия           | character varying(255) |           |          | 
 страна проживания | character varying(30)  |           |          | 
 заказ             | integer                |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "clients_заказ_fkey" FOREIGN KEY ("заказ") REFERENCES orders(id)
```
### - SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

### - список пользователей с правами над таблицами test_db
```commandline
test_db=# \dp
                                           Access privileges
 Schema |      Name      |   Type   |         Access privileges          | Column privileges | Policies 
--------+----------------+----------+------------------------------------+-------------------+----------
 public | clients        | table    | postgres=arwdDxt/postgres         +|                   | 
        |                |          | "test-admin-user"=arwdDxt/postgres+|                   | 
        |                |          | "test-simple-user"=arwd/postgres   |                   | 
 public | clients_id_seq | sequence |                                    |                   | 
 public | orders         | table    | postgres=arwdDxt/postgres         +|                   | 
        |                |          | "test-admin-user"=arwdDxt/postgres+|                   | 
        |                |          | "test-simple-user"=arwd/postgres   |                   | 
 public | orders_id_seq  | sequence |                                    |                   | 
(4 rows)
```

## Задача 3

### Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

### Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

### Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

```commandline
test_db=# INSERT INTO orders ("наименование","цена") VALUES ('Шоколад',10), ('Принтер',3000), ('Книга',500), ('Монитор',7000), ('Гитара',4000);
INSERT 0 5
test_db=# SELECT * FROM orders;
 id | наименование | цена 
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)

test_db=# INSERT INTO clients ("фамилия","страна проживания") VALUES ('Иванов Иван Иванович','USA'), ('Петров Петр Петрович','Canada'), ('Иоганн Себастьян Бах','Japan'), ('Ронни Джеймс Дио','Russia'), ('Ritchie Blackmore','Russia');
INSERT 0 5
test_db=# SELECT * FROM clients;
 id |       фамилия        | страна проживания | заказ 
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |      
  2 | Петров Петр Петрович | Canada            |      
  3 | Иоганн Себастьян Бах | Japan             |      
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |      
(5 rows)
```
### Используя SQL синтаксис:
### - вычислите количество записей для каждой таблицы
### - приведите в ответе:
### *- запросы*
### *- результаты их выполнения.*
```commandline
test_db=# SELECT COUNT(*) FROM orders;
 count 
-------
     5
(1 row)

test_db=# SELECT COUNT(*) FROM clients;
 count 
-------
     5
(1 row)
```

## Задача 4

### Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

### Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.
```commandline
test_db=# select * from orders;
 id | наименование | цена 
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)

test_db=# UPDATE clients SET "заказ" = 3 WHERE "фамилия" = 'Иванов Иван Иванович';
UPDATE 1
test_db=# UPDATE clients SET "заказ" = 4 WHERE "фамилия" = 'Петров Петр Петрович';
UPDATE 1
test_db=# UPDATE clients SET "заказ" = 5 WHERE "фамилия" = 'Иоганн Себастьян Бах';
UPDATE 1
test_db=# SELECT clients.фамилия AS ФИО,orders.наименование FROM clients,orders WHERE clients.заказ=orders.id;
         ФИО          | наименование 
----------------------+--------------
 Иванов Иван Иванович | Книга
 Петров Петр Петрович | Монитор
 Иоганн Себастьян Бах | Гитара
(3 rows)
```
Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
```commandline
test_db=# SELECT фамилия FROM clients WHERE заказ IS NOT NULL;
       фамилия        
----------------------
 Иванов Иван Иванович
 Петров Петр Петрович
 Иоганн Себастьян Бах
(3 rows)
```

## Задача 5

### Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 (используя директиву EXPLAIN).
### Приведите получившийся результат и объясните что значат полученные значения.
```commandline
test_db=# EXPLAIN SELECT фамилия FROM clients WHERE заказ IS NOT NULL;
                         QUERY PLAN                         
------------------------------------------------------------
 Seq Scan on clients  (cost=0.00..11.20 rows=119 width=516)
   Filter: ("заказ" IS NOT NULL)
(2 rows)
```
Здесь:
- "Seq Scan on clients" означает, что будет производиться последовательное сканирование таблицы "clients";
- cost=0.00..11.20 - оценочное время запуска запроса (приблизительная "стоимость" запуска, время до начала этапа вывода) и приблизительная общая стоимость, вычисляемая в в предположении, что план выполнится до конца, и данные будут возвращены;
- rows=119 - ожидаемое число строк;
- width=516 - ожидаемый размер строк;
- Filter: ("заказ" IS NOT NULL) - применение фильтра к плану на основе условия WHERE.

При использовании параметра ANALYZE, можно увидеть данные, полученные путем реального выполнения запроса:
```commandline
test_db=# EXPLAIN ANALYZE SELECT фамилия FROM clients WHERE заказ IS NOT NULL;
                                              QUERY PLAN                                              
------------------------------------------------------------------------------------------------------
 Seq Scan on clients  (cost=0.00..11.20 rows=119 width=516) (actual time=0.014..0.016 rows=3 loops=1)
   Filter: ("заказ" IS NOT NULL)
   Rows Removed by Filter: 2
 Planning Time: 0.057 ms
 Execution Time: 0.034 ms
(5 rows)
```
Здесь видно, реальное время, затраченное на получение первой строки и всех строк составляют, соответственно, 0.014 и 0.016мс, результатом работы является выборка из трех строк, план выполнен в один проход.\
Количество отфильтрованных строк (Rows Removed by Filter) - 2;\
Время планирования - 0.057мс;\
Время выполнения - 0.034мс.

## Задача 6

### Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker exec -it dmshch-postgres bash
root@05d0874b4dad:/# pg_dump -U postgres test_db > /var/lib/postgresql/backup/test_db.dump
root@05d0874b4dad:/# ls -l /var/lib/postgresql/backup/test_db.dump 
-rw-r--r-- 1 root root 5602 Feb 23 13:44 /var/lib/postgresql/backup/test_db.dump
```
### Остановите контейнер с PostgreSQL (но не удаляйте volumes).
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker stop dmshch-postgres
dmshch-postgres
root@dmhome:/home/dimka/Docker/SQL# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
### Поднимите новый пустой контейнер с PostgreSQL.
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker run -d --name dmshch-postgres-bck -e POSTGRES_PASSWORD=gfhjkm -e PGDATA=/var/lib/postgresql/data/pgdata -v /home/dimka/Docker/SQL/backup/:/var/lib/postgresql/backup postgres:12
ff450cc2ba164618436435edcfc255820b2d01f309f1db4b665612a9a5705b3e
```
### Восстановите БД test_db в новом контейнере.
```commandline
root@dmhome:/home/dimka/Docker/SQL# docker exec -it dmshch-postgres-bck bash
root@ff450cc2ba16:/# psql -U postgres
psql (12.10 (Debian 12.10-1.pgdg110+1))
Type "help" for help.

postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)

postgres=# CREATE DATABASES test_db;
ERROR:  syntax error at or near "DATABASES"
LINE 1: CREATE DATABASES test_db;
               ^
postgres=# CREATE DATABASE test_db;
CREATE DATABASE
postgres=# CREATE USER "test-admin-user";
CREATE ROLE
postgres=# CREATE USER "test-simple-user";
CREATE ROLE
postgres=# \q
root@ff450cc2ba16:/# psql -U postgres test_db < /var/lib/postgresql/backup/test_db.dump 
SET
...
GRANT
root@ff450cc2ba16:/# psql -U postgres
psql (12.10 (Debian 12.10-1.pgdg110+1))
Type "help" for help.

postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

postgres=# \c test_db
You are now connected to database "test_db" as user "postgres".
test_db=# select * from orders;
 id | наименование | цена 
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)

test_db=# select * from clients;
 id |       фамилия        | страна проживания | заказ 
----+----------------------+-------------------+-------
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |      
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(5 rows)

```
### Приведите список операций, который вы применяли для бэкапа данных и восстановления.
