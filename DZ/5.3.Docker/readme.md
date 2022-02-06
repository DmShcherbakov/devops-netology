# 5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера - Дмитрий Щербаков

## Задача 1
## Сценарий выполения задачи:
## - создайте свой репозиторий на https://hub.docker.com;
## - выберете любой образ, который содержит веб-сервер Nginx;
## - создайте свой fork образа;
## - реализуйте функциональность: запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```commandline
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
# Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

```commandline
dim@dm:~/docker$ cat Dockerfile 
FROM nginx
MAINTAINER Dmitriy Shcherbakov <dmshch@gmail.com>
COPY ./index.html /usr/share/nginx/html/
EXPOSE 80

dim@dm:~/docker$ cat index.html 
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>

dim@dm:~/docker$ docker build . -t dmshch:v1
Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM nginx
 ---> c316d5a335a5
Step 2/4 : MAINTAINER Dmitriy Shcherbakov <dmshch@gmail.com>
 ---> Running in 51837c295710
Removing intermediate container 51837c295710
 ---> 521b15ce89d4
Step 3/4 : COPY ./index.html /usr/share/nginx/html/
 ---> 5f830ec06849
Step 4/4 : EXPOSE 80
 ---> Running in 7705c713b6fc
Removing intermediate container 7705c713b6fc
 ---> 4a691ae26ef8
Successfully built 4a691ae26ef8
Successfully tagged dmshch:v1

dim@dm:~/docker$ docker run -p 8050:80 -d dmshch:v1 
3ed5b335e98610a96ec4083678c88b721434f9a8d0c79fa390d874ea50a35bfd
dim@dm:~/docker$ docker ps
CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS                                   NAMES
3ed5b335e986   dmshch:v1   "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   0.0.0.0:8050->80/tcp, :::8050->80/tcp   loving_feynman
dim@dm:~/docker$  lynx --dump localhost:8050
   Hey, Netology

                             I’m DevOps Engineer!
dim@dm:~/docker$ docker tag dmshch:v1 dmshch/netology:nginx-v1
dim@dm:~/docker$ docker push  dmshch/netology:nginx-v1
The push refers to repository [docker.io/dmshch/netology]
7f78679dda2f: Pushed 
762b147902c0: Pushed 
235e04e3592a: Pushed 
6173b6fa63db: Pushed 
9a94c4a55fe4: Pushed 
9a3a6af98e18: Pushed 
7d0ebbe3f5d2: Pushed 
nginx-v1: digest: sha256:f1ae8e011c6509a6ebd91fb2fbeb7136168c9070b66dbe648f108fe279e7f989 size: 1777
```
<code>[Ссылка на репозиторий](https://hub.docker.com/r/dmshch/netology)

## Задача 2

##Посмотрите на сценарий ниже и ответьте на вопрос:
##"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

##Детально опишите и обоснуйте свой выбор.

№ |Сценарий|Ответ
---|---|---
1.|- Высоконагруженное монолитное java веб-приложение|не подходит
2.|- Nodejs веб-приложение;|подходит
3.|- Мобильное приложение c версиями для Android и iOS;|не подходит
4.|- Шина данных на базе Apache Kafka;|подходит
5.|- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;|
6.|- Мониторинг-стек на базе Prometheus и Grafana;|подходит
7.|- MongoDB, как основное хранилище данных для java-приложения;|
8.|- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.|

1. Docker, как дополнительный слой виртуализации, увеличивает накладные расходы на вычислительные ресурсы. Кроме того, вносятся дополнительные задержки как при работе с сетью, так и с другими подсистемами. Кроме того, идеология Docker подразумевает разделение систем на микросервисы, чтобы запускать каждый в изолированной среде. Поэтому, для высоконагруженных мололитных приложений docker подходит не лучшим образом.
2. Существует достаточно примеров реализации node.js-приложений на базе Docker.
3. Docker не предназначен для приложений с графическим интерфейсом (хотя при желании возможно реализовать тот или иной функционал), поэтому использование его для Andoid b iOS не является распространенной практикой.
4. 