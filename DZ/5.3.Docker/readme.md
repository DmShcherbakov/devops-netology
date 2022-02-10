# 5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера - Дмитрий Щербаков

## Задача 1
### Сценарий выполения задачи:
### - создайте свой репозиторий на https://hub.docker.com;
### - выберете любой образ, который содержит веб-сервер Nginx;
### - создайте свой fork образа;
### - реализуйте функциональность: запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
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
### Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

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

### Посмотрите на сценарий ниже и ответьте на вопрос:
### "Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

###Детально опишите и обоснуйте свой выбор.

№ |Сценарий|Ответ
---|---|---
1.|- Высоконагруженное монолитное java веб-приложение|не подходит
2.|- Nodejs веб-приложение;|подходит
3.|- Мобильное приложение c версиями для Android и iOS;|не подходит
4.|- Шина данных на базе Apache Kafka;|подходит
5.|- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;|допустимо
6.|- Мониторинг-стек на базе Prometheus и Grafana;|подходит
7.|- MongoDB, как основное хранилище данных для java-приложения;|допустимо
8.|- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.|подходит

1. Docker, как дополнительный слой виртуализации, увеличивает накладные расходы на вычислительные ресурсы. Кроме того, вносятся дополнительные задержки как при работе с сетью, так и с другими подсистемами. Кроме того, идеология Docker подразумевает разделение систем на микросервисы, чтобы запускать каждый в изолированной среде. Поэтому, для высоконагруженных мололитных приложений docker подходит не лучшим образом.
2. Существует достаточно примеров реализации node.js-приложений на базе Docker.
3. Docker не предназначен для приложений с графическим интерфейсом (хотя при желании возможно реализовать тот или иной функционал), поэтому использование его для Andoid b iOS не является распространенной практикой.
4. С учетом того, что Apache Kafka по сути своей является распределенной горизонтально масштабируемой системой, использование Docker для ее функционирования вполне оправдано.
5. В зависимости от того, как много логов генерирует веб-приложение (и со скольки хостов оно их генерирует), нагрузка на дисковую систему может сильно варьироваться. В том случае, когда поток данных действительно большой, наличие дополнительной абстракции в лице Docker может оказать критическое влияние на производительность операций ввода-вывода при работе с дисковой подсистемой. В таком случае, от использования Docker лучше воздержаться.  
6. В данном случае, речь идет уже не о логах, а об обмене информацией по сети. Как правило, трафик систем мониторинга довольно скромный, равно как и потребности систем отрисовки графиков.
7. Ввиду того, что MongoDB горизонтально масштабируема, использование Docker вполне оправдано, однако следует ориентироваться на объемы обрабатываемых данных. В случае больших массивов значений, можно, как указывалось ранее, оказаться перед проблемой ввода-вывода.
8. С учетом того, что процесс взаимодействия с выделенным Gitlab для CI/CD и Docker Registry является спорадическим, даже в случае больших объемов хранимых данных, проблем это вызывать не должно. Кроме того, GitLab хорошо поддерживает Docker.

## Задача 3
### - Запустите первый контейнер из образа centos c любым тэгом в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
### - Запустите второй контейнер из образа debian в фоновом режиме, подключив папку /data из текущей рабочей директории на хостовой машине в /data контейнера;
### - Подключитесь к первому контейнеру с помощью docker exec и создайте текстовый файл любого содержания в /data;
### - Добавьте еще один файл в папку /data на хостовой машине;
### - Подключитесь во второй контейнер и отобразите листинг и содержание файлов в /data контейнера.

```commandline
17:48:32 dim@dm:~/Docker$ mkdir data
17:49:41 dim@dm:~/Docker$ docker run -d -it --volume /home/dim/Docker/data/:/data centos /bin/bash
Unable to find image 'centos:latest' locally
latest: Pulling from library/centos
a1d0c7532777: Pull complete 
Digest: sha256:a27fd8080b517143cbbbab9dfb7c8571c40d67d534bbdee55bd6c473f432b177
Status: Downloaded newer image for centos:latest
3f5f6652a2126c80d085a2f4e6d8103db775440eb80c36f07098b4be2ba3f19d
17:50:11 dim@dm:~/Docker$ docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS         PORTS     NAMES
3f5f6652a212   centos    "/bin/bash"   6 seconds ago   Up 4 seconds             condescending_bose
17:50:16 dim@dm:~/Docker$ docker run -d -it --volume /home/dim/Docker/data/:/data debian /bin/bash
Unable to find image 'debian:latest' locally
latest: Pulling from library/debian
0c6b8ff8c37e: Pull complete 
Digest: sha256:fb45fd4e25abe55a656ca69a7bef70e62099b8bb42a279a5e0ea4ae1ab410e0d
Status: Downloaded newer image for debian:latest
5fb17fef22df5f9213b26ff221e857097da19378a49cc0c58675dc21a68af2a1
17:50:48 dim@dm:~/Docker$ docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
5fb17fef22df   debian    "/bin/bash"   16 seconds ago   Up 14 seconds             silly_elgamal
3f5f6652a212   centos    "/bin/bash"   53 seconds ago   Up 51 seconds             condescending_bose
17:51:03 dim@dm:~/Docker$ docker exec -it condescending_bose /bin/bash
[root@3f5f6652a212 /]# echo "Netology" > /data/centos.txt
[root@3f5f6652a212 /]# cat /data/centos.txt 
Netology
[root@3f5f6652a212 /]# exit
exit
17:52:23 dim@dm:~/Docker$ echo "Netology again" > /home/dim/Docker/data/host.txt
17:52:55 dim@dm:~/Docker$ docker exec -it silly_elgamal /bin/bash
root@5fb17fef22df:/# cat /data/*
Netology
Netology again
root@5fb17fef22df:/# ls /data/ 
centos.txt  host.txt
root@5fb17fef22df:/# grep Netology /data/*
/data/centos.txt:Netology
/data/host.txt:Netology again
```

## Задача 4 (*)
### Воспроизвести практическую часть лекции самостоятельно.
### Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.
```commandline
$ docker build -t dmshch/ansible:2.9.24 .
Sending build context to Docker daemon   2.56kB
Step 1/5 : FROM alpine:3.14
3.14: Pulling from library/alpine
97518928ae5f: Pull complete 
Digest: sha256:635f0aa53d99017b38d1a0aa5b2082f7812b03e3cdb299103fe77b5c8a07f1d2
Status: Downloaded newer image for alpine:3.14
 ---> 0a97eee8041e
...
Successfully built b240ed7d63f0
Successfully tagged dmshch/ansible:2.9.24
$ docker push dmshch/ansible:2.9.24
The push refers to repository [docker.io/dmshch/ansible]
f2c64b043fbe: Pushed 
a2fe0cf657ae: Pushed 
1a058d5342cc: Mounted from library/alpine 
2.9.24: digest: sha256:0538f1fedba95b9b3ca9f9c8f0ec484c6696d1b6e488c422074b61efaa3472da size: 947
```
<code>[Ссылка на репозиторий](https://hub.docker.com/r/dmshch/ansible)

