# 6.4. PostgreSQL - Дмитрий Щербаков

## Задача 1

### Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
```commandline
root@dmhome:/home/dimka/PSQL# mkdir data
root@dmhome:/home/dimka/PSQL# docker run -d --name dmshch-postgres -e POSTGRES_PASSWORD=gfhjkm -e PGDATA=/var/lib/postgresql/data/pgdata -v /home/dimka/Docker/PSQL/data:/var/lib/postgresql/data postgres:13
Unable to find image 'postgres:13' locally
13: Pulling from library/postgres
5eb5b503b376: Already exists 
daa0467a6c48: Already exists 
7cf625de49ef: Already exists 
bb8afcc973b2: Already exists 
c74bf40d29ee: Already exists 
2ceaf201bb22: Already exists 
1255f255c0eb: Already exists 
12a9879c7aa1: Already exists 
0052b4855bef: Pull complete 
e1392be26b85: Pull complete 
9154b308134e: Pull complete 
7e0447003684: Pull complete 
3d7ffb6e96a5: Pull complete 
Digest: sha256:8b8ff4fcdc9442d8a1d38bd1a77acbdfbc8a04afda9c19df47383cb2d08fc04b
Status: Downloaded newer image for postgres:13
0643c98d59b7c070c1d6fc0540ad6e1c2885a7ff91b24486597c731739ab3891
root@dmhome:/home/dimka/PSQL# docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS      NAMES
0643c98d59b7   postgres:13   "docker-entrypoint.s…"   39 seconds ago   Up 35 seconds   5432/tcp   dmshch-postgres
```
### Подключитесь к БД PostgreSQL используя `psql`.
```commandline
root@dmhome:/home/dimka/PSQL# docker exec -it dmshch-postgres psql -U postgres
psql (13.6 (Debian 13.6-1.pgdg110+1))
Type "help" for help.
```
### Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.
### **Найдите и приведите** управляющие команды для:
### - вывода списка БД
```commandline
  \l[+]   [PATTERN]      list databases
```
### - подключения к БД
```commandline
  \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}
                         connect to new database (currently "postgres")
```
### - вывода списка таблиц
```commandline
  \d[S+]                 list tables, views, and sequences
```
### - вывода описания содержимого таблиц
```commandline
  \d[S+]  NAME           describe table, view, sequence, or index
```
### - выхода из psql
```commandline
  \q                     quit psql
```

## Задача 2

### Используя `psql` создайте БД `test_database`.
```commandline
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
```
### Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).
### Восстановите бэкап БД в `test_database`.
```commandline
# cat test_dump.sql | docker exec -i dmshch-postgres psql -U postgres test_database 
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE
```
### Перейдите в управляющую консоль `psql` внутри контейнера.
```commandline
# docker exec -it dmshch-postgres psql -U postgres test_database
psql (13.6 (Debian 13.6-1.pgdg110+1))
Type "help" for help.
```
### Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
```commandline
test_database=# ANALYZE VERBOSE orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```
### Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` с наибольшим средним значением размера элементов в байтах.
### **Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.
```commandline
test_database=# select attname,avg_width from pg_stats where tablename='orders' order by avg_width desc limit 1;
 attname | avg_width 
---------+-----------
 title   |        16
(1 row)
```

## Задача 3

### Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
### Предложите SQL-транзакцию для проведения данной операции.
Текст транзакции может выглядеть следующим образом:
```commandline
BEGIN;
CREATE TABLE orders_1 ( CHECK ( price > 499 )) INHERITS ( orders );
CREATE TABLE orders_2 ( CHECK ( price <= 499)) INHERITS ( orders );

CREATE OR REPLACE FUNCTION price_insert_trigger()
RETURNS TRIGGER AS $$
BEGIN
IF ( NEW.price > 499 ) THEN INSERT INTO orders_1 VALUES (NEW.*);
ELSE INSERT INTO orders_2 VALUES (NEW.*);
END IF;
RETURN NULL;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER insert_orders BEFORE INSERT ON orders FOR EACH ROW EXECUTE FUNCTION price_insert_trigger();
WITH x AS (DELETE FROM ONLY orders WHERE price>499 RETURNING *) INSERT INTO orders_1 SELECT * FROM x;
WITH x AS (DELETE FROM ONLY orders WHERE price<=499 RETURNING *) INSERT INTO orders_2 SELECT * FROM x;
TRUNCATE ONLY orders;
COMMIT;
```
По результатам выполнения можем видеть следующее:
```commandline
test_database=# select * from orders;
 id |        title         | price 
----+----------------------+-------
  2 | My little database   |   500
  6 | WAL never lies       |   900
  8 | Dbiezdmin            |   501
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(8 rows)

test_database=# select * from only orders;
 id | title | price 
----+-------+-------
(0 rows)

test_database=# select * from orders_1;
 id |       title        | price 
----+--------------------+-------
  2 | My little database |   500
  6 | WAL never lies     |   900
  8 | Dbiezdmin          |   501
(3 rows)

test_database=# select * from orders_2;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  7 | Me and my bash-pet   |   499
(5 rows)

test_database=# \d+ orders;
                                                       Table "public.orders"
 Column |         Type          | Collation | Nullable |              Default               | Storage  | Stats target | Description 
--------+-----------------------+-----------+----------+------------------------------------+----------+--------------+-------------
 id     | integer               |           | not null | nextval('orders_id_seq'::regclass) | plain    |              | 
 title  | character varying(80) |           | not null |                                    | extended |              | 
 price  | integer               |           |          | 0                                  | plain    |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Triggers:
    insert_orders BEFORE INSERT ON orders FOR EACH ROW EXECUTE FUNCTION price_insert_trigger()
Child tables: orders_1,
              orders_2
Access method: heap
```
### Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?
Да. Как вариант, можно было создать функцию, обеспечивающую шардирование с автоматическим созданием партиций. Либо можно использовать декларативное партицирование на этапе создания таблицы.  

## Задача 4

### Используя утилиту `pg_dump` создайте бекап БД `test_database`.
```commandline
root@dmhome:/home/dimka/PSQL# docker exec -i dmshch-postgres pg_dump -U postgres test_database > test_db.dump_bck
root@dmhome:/home/dimka/PSQL# ls -lh ./test_db.dump 
-rw-r--r-- 1 root root 4,1K фев 28 11:54 ./test_db.dump
```
[Файл бэкапа](test_db.dump_bck)
### Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?
В разделе `CREATE TABLE public.orders` в файле бэкапа следует дополнить описание столбца `title` параметром `UNIQUE`:
```commandline
root@dmhome:/home/dimka/PSQL# diff test_db.dump test_db.dump_bck 
47c47
<     title character varying(80) NOT NULL UNIQUE,
---
>     title character varying(80) NOT NULL,
```
[Откорректированный файл бэкапа](test_db.dump)
