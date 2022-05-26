# 6.5. Elasticsearch - Дмитрий Щербаков

## Задача 1
### Используя докер образ centos:7 как базовый и документацию по установке и запуску Elastcisearch:
### - составьте Dockerfile-манифест для elasticsearch
### - соберите docker-образ и сделайте push в ваш docker.io репозиторий
### - запустите контейнер из получившегося образа и выполните запрос пути / c хост-машины
### Требования к elasticsearch.yml:
### - данные path должны сохраняться в /var/lib
### - имя ноды должно быть netology_test
### В ответе приведите:
### - текст Dockerfile манифеста
### - ссылку на образ в репозитории dockerhub
### - ответ elasticsearch на запрос пути / в json виде

### - текст Dockerfile манифеста
```commandline
# cat Dockerfile 
FROM centos:7
LABEL maintainer="dmshch@gmail.com"
RUN useradd elastic
RUN chmod 777 /var/lib/
USER elastic
WORKDIR /home/elastic/
ENV ES_JAVA_OPTS="-Xms1g -Xmx1g"
COPY ./elasticsearch-8.2.1-linux-x86_64.tar.gz ./
RUN tar -xzf elasticsearch-8.2.1-linux-x86_64.tar.gz
WORKDIR /home/elastic/elasticsearch-8.2.1
COPY --chown=elastic:elastic ./elasticsearch.yml ./config/
CMD ./bin/elasticsearch -d
EXPOSE 9200
```

### - ссылку на образ в репозитории dockerhub
https://hub.docker.com/layers/220922699/dmshch/netology/elasticsearch-v1/images/sha256-bf1fcf5405bf69b758e2c15f8eb600261067a024f30f2241d195c7a57340566b?context=repo
(docker pull dmshch/netology:elasticsearch-v1)

### - ответ elasticsearch на запрос пути / в json виде
```commandline
$ curl http://127.0.0.1:9200
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "H6KjRe9FQg6JkNsYr9yW2Q",
  "version" : {
    "number" : "8.2.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "db223507a0bd08f8e84a93e329764cc39b0043b9",
    "build_date" : "2022-05-19T16:34:08.043347449Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

## Задача 2
### Ознакомтесь с документацией и добавьте в elasticsearch 3 индекса, в соответствии с таблицей:
|Имя|	Количество реплик|	Количество шард|
|---|---|---|
|ind-1|	0|	1|
|ind-2|	1|	2|
|ind-3|	2|	4|
```commandline
dimka@dmhome:~$ curl -X PUT "localhost:9200/ind-1?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "index": {
>       "number_of_shards": 1,  
>       "number_of_replicas": 0 
>     }
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
dimka@dmhome:~$ curl -X PUT "localhost:9200/ind-2?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "index": {
>       "number_of_shards": 2,  
>       "number_of_replicas": 1 
>     }
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
dimka@dmhome:~$ curl -X PUT "localhost:9200/ind-3?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "index": {
>       "number_of_shards": 4,  
>       "number_of_replicas": 2 
>     }
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
```

### Получите список индексов и их статусов, используя API и приведите в ответе на задание.
```commandline
$ curl -X GET http://127.0.0.1:9200/_cat/indices?pretty
yellow open ind-2 _Vzc1FnmRz6atdg6HvqVjQ 2 1 0 0 450b 450b
green  open ind-1 Q1rN3e2cRXaIOdu4--Ak7w 1 0 0 0 225b 225b
yellow open ind-3 YyH7Ej1ySSm96wrEIM1fXA 4 2 0 0 900b 900b

```
### Получите состояние кластера elasticsearch, используя API.
```commandline
$ curl -X GET http://127.0.0.1:9200/_cluster/health?pretty
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 8,
  "active_shards" : 8,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 44.44444444444444
}
```
### Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
У нас в "кластере" находится только одна нода, при этом для двух индексов (ind-2 и ind-3) указано ненулевое количество реплик. Таким образом, реплики для шард двух индексов находятся в состоянии "UNASSIGNED":
```commandline
$ curl -X GET http://127.0.0.1:9200/_cat/shards?pretty
.geoip_databases 0 p STARTED           127.0.0.1 netology_test
ind-2            0 p STARTED    0 225b 127.0.0.1 netology_test
ind-2            0 r UNASSIGNED                  
ind-2            1 p STARTED    0 225b 127.0.0.1 netology_test
ind-2            1 r UNASSIGNED                  
ind-1            0 p STARTED    0 225b 127.0.0.1 netology_test
ind-3            0 p STARTED    0 225b 127.0.0.1 netology_test
ind-3            0 r UNASSIGNED                  
ind-3            0 r UNASSIGNED                  
ind-3            1 p STARTED    0 225b 127.0.0.1 netology_test
ind-3            1 r UNASSIGNED                  
ind-3            1 r UNASSIGNED                  
ind-3            2 p STARTED    0 225b 127.0.0.1 netology_test
ind-3            2 r UNASSIGNED                  
ind-3            2 r UNASSIGNED                  
ind-3            3 p STARTED    0 225b 127.0.0.1 netology_test
ind-3            3 r UNASSIGNED                  
ind-3            3 r UNASSIGNED              
```
### Удалите все индексы.
```commandline
dimka@dmhome:~$ curl -X DELETE http://127.0.0.1:9200/ind-1?pretty
{
  "acknowledged" : true
}
dimka@dmhome:~$ curl -X DELETE http://127.0.0.1:9200/ind-2?pretty
{
  "acknowledged" : true
}
dimka@dmhome:~$ curl -X DELETE http://127.0.0.1:9200/ind-3?pretty
{
  "acknowledged" : true
}
dimka@dmhome:~$ curl -X GET http://127.0.0.1:9200/_all?pretty
{ }
```

## Задача 3
### Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.
```commandline
# docker exec e4c1bdcbda7e tree -d /home/elastic
# docker exec e4c1bdcbda7e ls -l /home/elastic/elasticsearch-8.2.1
total 896
-rw-r--r--  1 elastic elastic   3860 May 19 16:33 LICENSE.txt
-rw-r--r--  1 elastic elastic 873453 May 19 16:38 NOTICE.txt
-rw-r--r--  1 elastic elastic   2710 May 19 16:33 README.asciidoc
drwxr-xr-x  2 elastic elastic   4096 May 19 16:41 bin
drwxr-xr-x  1 elastic elastic   4096 May 25 13:30 config
drwxr-xr-x  8 elastic elastic   4096 May 19 16:41 jdk
drwxr-xr-x  4 elastic elastic   4096 May 19 16:41 lib
drwxr-xr-x  1 elastic elastic   4096 May 26 01:31 logs
drwxr-xr-x 65 elastic elastic   4096 May 19 16:41 modules
drwxr-xr-x  2 elastic elastic   4096 May 19 16:38 plugins
drwxr-xr-x  2 elastic elastic   4096 May 26 07:42 snapshots
```
### Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
### Приведите в ответе запрос API и результат вызова API для создания репозитория.
```commandline
$ curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "snapshots"
  }
}
'
{
  "acknowledged" : true
}
```
### Создайте индекс test с 0 реплик и 1 шардом и приведите в ответе список индексов.
```commandline
dimka@dmhome:~$ curl -X PUT "localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "index": {
>       "number_of_shards": 1,  
>       "number_of_replicas": 0 
>     }
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}
dimka@dmhome:~$ curl -X GET http://127.0.0.1:9200/_all?pretty
{
  "test" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test",
        "creation_date" : "1653552892016",
        "number_of_replicas" : "0",
        "uuid" : "H5kMXVqsQp2IcPhEQSDIPg",
        "version" : {
          "created" : "8020199"
        }
      }
    }
  }
}
```
### Создайте snapshot состояния кластера elasticsearch.
```commandline
dimka@dmhome:~$ curl -X PUT "http://127.0.0.1:9200/_snapshot/netology_backup/mybackup?pretty"
{
  "accepted" : true
}
```
### Приведите в ответе список файлов в директории со snapshotами.
```commandline
$ ls -l snapshots/snapshots/
total 36
-rw-rw-r-- 1 elastic elastic   855 May 26 08:19 index-0
-rw-rw-r-- 1 elastic elastic     8 May 26 08:19 index.latest
drwxrwxr-x 4 elastic elastic  4096 May 26 08:19 indices
-rw-rw-r-- 1 elastic elastic 18276 May 26 08:19 meta-aLc5IKWCSjmTLkjgqGWHmw.dat
-rw-rw-r-- 1 elastic elastic   362 May 26 08:19 snap-aLc5IKWCSjmTLkjgqGWHmw.dat
```
### Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.
```commandline
dimka@dmhome:~$ curl -X DELETE http://127.0.0.1:9200/test?pretty
{
  "acknowledged" : true
}
dimka@dmhome:~$ curl -X PUT "localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 1,  
      "number_of_replicas": 0 
    }
  }
}
'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
dimka@dmhome:~$ curl -X GET http://127.0.0.1:9200/_all?pretty
{
  "test-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test-2",
        "creation_date" : "1653554053093",
        "number_of_replicas" : "0",
        "uuid" : "MfAVTQv-SQKdzLUQbPP42Q",
        "version" : {
          "created" : "8020199"
        }
      }
    }
  }
}

```
### Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.
### Приведите в ответе запрос к API восстановления и итоговый список индексов.
```commandline
dimka@dmhome:~$ curl -X POST http://127.0.0.1:9200/_snapshot/netology_backup/mybackup/_restore?pretty
{
  "accepted" : true
}
dimka@dmhome:~$ curl -X GET http://127.0.0.1:9200/_all?pretty
{
  "test" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test",
        "creation_date" : "1653553918053",
        "number_of_replicas" : "0",
        "uuid" : "JYVnd3SsSk-de4bmdGxw9Q",
        "version" : {
          "created" : "8020199"
        }
      }
    }
  },
  "test-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test-2",
        "creation_date" : "1653554053093",
        "number_of_replicas" : "0",
        "uuid" : "MfAVTQv-SQKdzLUQbPP42Q",
        "version" : {
          "created" : "8020199"
        }
      }
    }
  }
}
```
