<div align="center">
<h1><a id="intro">Лабораторная работа №5</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Шмаков_И._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Салют :wave:,<br>
Данная лабораторная работа посвещена изучению Docker и как с ним работать. Эта лабораторная работа послужит подпоркой для старта в выявлении и определении уязвимостей на уровне сканирования контейнеров при сборке приложений. 

Для сдачи данной работы также будет требоваться ответить на дополнительыне вопросы по описанным темам.

***

## Задание

✅ 1. Поставьте `Docker` и `buildkit`

```bash
$ brew install buildkit
$ brew install docker
```

✅ 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker run --rm -it hello-appsec-world

$ docker save -o hello.tar hello-appsec-world
$ docker load -i hello.tar
$ docker load -i image.tar
```
✅ 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
✅ 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 

> Пример анализа по текущему `Dockerfile` в репозитории

```dockerfile
# Этап 1: сборка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /hello
# Копируем файл с зависимостями
COPY requirements.txt . 
# Устанавливаем зависимости в отдельную директорию wheelhouse для кеширования
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# Этап 2: запускаемый образ
FROM python:3.11-slim
WORKDIR /hello
# Копируем файл с зависимостями
COPY --from=builder /wheels /wheels # Копируем собранные wheel-пакеты
COPY requirements.txt . 
# Устанавливаем зависимости из wheel-пакетов
RUN pip install --no-index --find-links=/wheels -r requirements.txt
# Копируем исходный код приложения
COPY hello.py .

# Переменные окружения для улучшенной работы Python
ENV PYTHONUNBUFFERED=1
# Запускаем приложение
CMD ["python", "hello.py"] 
```

✅ 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker save -o hello_ypur_project.tar hello-appsec-world

$ docker load -i hello_ypur_project.tar
$ docker run hello-appsec-world

$ docker load -i image.tar
$ docker run hello-appsec-world
```

✅ 6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате:

```
flask==2.2.3
requests==2.28.1
```

✅ 7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.
✅ 8. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ docker login
$ docker tag hello-appsec-world yourusername/hello-appsec-world
$ docker push yourusername/hello-appsec-world
$ docker inspect yourusername/hello-appsec-world
$ docker container create --name first hello-appsec-world # выпишите id контейнера

$ docker image pull geminishkv/hello-appsec-world
$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world

```
 

✅ 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
 $ docker container run -it ubuntu /bin/bash
```
 
✅ 10. Выведите оба контейнера first и second на терминал
✅ 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
$ docker-compose up --build
```
✅ 12. Откройте соседнее окно терминала и и выведите на терминале

```bash 
$ open -a "Google Chrome" http://localhost:8000
```

✅ 13. Остановите работу `docker-compose`.

```bash 
$ docker ps -a
$ docker ps -q
$ docker images

$ docker ps -q | xargs docker stop
$ docker-compose down
```
✅ 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
✅ 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
✅ 16. Подготовьте отчет `gist`.
 

***

## Выполнение

✅ 1. Поставьте `Docker` и `buildkit`

```bash
$ brew install buildkit
$ brew install docker
```

✅ 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```bash
$ docker buildx build -t hellow-appsec-world . # -t задаёт имя (тег) образа

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker buildx build -t hello-appsec-world .
[+] Building 11.0s (13/13) FINISHED docker:default

$ docker run hello-appsec-world

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker run hello-appsec-world
hello appsec world

$ docker run --rm -it hello-appsec-world # # --rm удаляет контейнер после завершения, -it — интерактивный TTY

$ docker save -o hello.tar hello-appsec-world #экспортируем образ в файл 
$ docker load -i hello.tar # импортирует Docker-образ из tar-архива
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker load -i hello.tar
Loaded image: hello-appsec-world:latest


$ docker load -i image.tar 

```
✅ 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
``` bash 
FROM python:3.11-slim AS builder
#Рабочая директория внутри контейнера
WORKDIR /hello
# Копируем файл зависимостей
COPY requirements.txt .
# Обновляем pip и собираем wheel-пакеты зависимост>
RUN pip install --upgrade pip && pip wheel --wheel>

FROM python:3.11-slim
WORKDIR /hello
# Копируем заранее собранные wheel-пакеты
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r>
# Копируем исходный код приложения
COPY hello.py .
# Нужно для логирования в Docker
ENV PYTHONUNBUFFERED=1
# Команда запуска контейнера
CMD ["python", "hello.py"]

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ git commit -m "DF with comments" 

```
✅ 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 
``` bash 
#file from lab02

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker run hello-appsec-world
pygame 2.6.1 (SDL 2.28.4, Python 3.11.14)
Hello from the pygame community. https://www.pygame.org/contribute.html
/usr/local/lib/python3.11/site-packages/pygame/sysfont.py:221: UserWarning: 'fc-list' is missing, system fonts cannot be loaded on your platform
  warnings.warn(
^CTraceback (most recent call last):
  File "/app/app.py", line 20, in <module>
    for event in pygame.event.get():
                 ^^^^^^^^^^^^^^^^^^
KeyboardInterrupt

#new file
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ cat app.py     
import platform
import sys
import time

print("Hello appsec world")
print(f"Python version: {sys.version}")
print(f"OS: {platform.system()} {platform.release()}")

for i in range(3):
    print(f"Working... step {i+1}")
    time.sleep(1)

print("Application finished successfully")

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker run hello-appsec-world              
Hello appsec world
Python version: 3.11.14 (main, Jan 13 2026, 03:12:14) [GCC 14.2.0]
OS: Linux 6.11.2-amd64
Working... step 1
Working... step 2
Working... step 3
Application finished successfully

```

✅ 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker save -o hello_ypur_project.tar hello-appsec-world
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker save -o hello_ypur_project.tar hello-appsec-world
                                                   
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ ls -l hello_ypur_project.tar 
-rw------- 1 tigo tigo 191031296 Jan 14 15:57 hello_ypur_project.tar  

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ sha256sum hello_ypur_project.tar  | tee /tmp/hash_my.txt  
b0ba78ac0a31cdee11c758a3c91aa2c60f6a3d0050ab384c9468e544003bb004  hello_ypur_project.tar

```

✅ 6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате:

```bash
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ cat requirements.txt
pygame==2.5.2

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ git add requirements.txt 
                                                   
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ git commit -m "add dependency"


```

✅ 7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.

✅ 8. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ docker login
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker login -u tigoananikyan

Password: 
WARNING! Your password will be stored unencrypted in /home/tigo/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credential-stores

Login Succeeded


$ docker tag hello-appsec-world yourusername/hello-appsec-world
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker tag hello-appsec-world tigoananikyan/hello-appsec-world

$ docker push yourusername/hello-appsec-world
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker push tigoananikyan/hello-appsec-world

Using default tag: latest
The push refers to repository [docker.io/tigoananikyan/hello-appsec-world]
eb46f507d655: Pushed 
b40e21cb0c88: Pushed 
732bca761039: Pushed 
9f5c77361625: Pushed 
5cf3d0ce54d0: Pushed 
49d74831a287: Mounted from library/python 
5d89b1d5fc98: Mounted from library/python 
523062ea36b5: Mounted from library/python 
e50a58335e13: Mounted from library/python 
latest: digest: sha256:ffbba9c9b1e39e5da5b13d86eadc4fb11b83122675da7c360e2903949ea34a92 size: 2203
    
$ docker inspect yourusername/hello-appsec-world
──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker inspect tigoananikyan/hello-appsec-world 

[
    {
        "Id": "sha256:9f6feb54047a8f0dd1123e905124a2f613448a3808c7d6b998db4acce5d092de",
        "RepoTags": [
            "hello-appsec-world:latest",
            "hellow-appsec-world:latest",
            "tigoananikyan/hello-appsec-world:latest"
        ],


$ docker container create --name first hello-appsec-world # выпишите id контейнера
                                                   
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker container create --name first hello-appsec-world

7690f105aee854ba3d5b08586b42d73b856509fa1a2b0f191106d16aaf9a1dce

$ docker image pull geminishkv/hello-appsec-world
                                                   
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker image pull geminishkv/hello-appsec-world 

Using default tag: latest
Error response from daemon: pull access denied for geminishkv/hello-appsec-world, repository does not exist or may require 'docker login': denied: requested access to the resource is denied

$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world

```
 
✅ 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
 $ docker container run -it ubuntu /bin/bash

┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker container run -it ubuntu /bin/bash

Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
20043066d3d5: Pull complete 
Digest: sha256:c35e29c9450151419d9448b0fd75374fec4fff364a27f176fb458d472dfc9e54
Status: Downloaded newer image for ubuntu:latest
root@28e09b316ae0:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.1   4588  3920 pts/0    Ss   21:33   0:00 /bin/bash
root           9  0.0  0.1   7888  4064 pts/0    R+   21:34   0:00 ps aux
root@28e09b316ae0:/# whoami
root


```
 
✅ 10. Выведите оба контейнера first и second на терминал
```bash
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05/source]
└─$ docker ps -a | grep -E "first|second"
1ea0cf95c68b   hello-appsec-world   "python app.py"     15 seconds ago      Created                                    second
7690f105aee8   hello-appsec-world   "python app.py"     10 minutes ago      Created                                    first

```
✅ 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
$ docker-compose up --build
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05]
└─$ docker-compose up --build 
server-1  |  * Serving Flask app 'app'
server-1  |  * Debug mode: off
server-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
server-1  |  * Running on all addresses (0.0.0.0)
server-1  |  * Running on http://127.0.0.1:8000
server-1  |  * Running on http://172.18.0.2:8000
server-1  | Press CTRL+C to quit
server-1  | 172.18.0.3 - - [14/Jan/2026 21:41:46] "GET / HTTP/1.1" 200 -
client-1  | 
client-1  |     <html>                                                           
client-1  |     <head><title>Colorful Output</title></head>                      
client-1  |     <body style="font-family: monospace; font-size: 24px;">          
                                                                                 
client-1  |     <span style="color:red">h</span><span style="color:green">e</span><span style="color:yellow">l</span><span style="color:blue">l</span><span style="color:purple">o</span><span style="color:red"> </span><span style="color:green">a</span><span style="color:yellow">p</span><span style="color:blue">p</span><span style="color:purple">s</span><span style="color:red">e</span><span style="color:green">c</span><span style="color:yellow"> </span><span style="color:blue">w</span><span style="color:purple">o</span><span style="color:red">r</span><span style="color:green">l</span><span style="color:yellow">d</span> 
```

✅ 12. Откройте соседнее окно терминала и и выведите на терминале

```bash 
$ open -a "Google Chrome" http://localhost:8000

┌──(tigo㉿tigo)-[~]
└─$ curl -I http://localhost:8000
HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.14
Date: Wed, 14 Jan 2026 21:44:17 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 761
Connection: close

```

✅ 13. Остановите работу `docker-compose`.

```bash 
$ docker ps -a
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05]
└─$ docker ps -a    
CONTAINER ID   IMAGE                COMMAND              CREATED             STATUS                           PORTS                                       NAMES
aada9520c776   lab05-client         "python client.py"   3 minutes ago       Exited (0) 26 seconds ago                                                    lab05-client-1
4e28486ca35d   lab05-server         "python app.py"      3 minutes ago       Up 3 minutes                     0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   lab05-server-1

$ docker ps -q
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05]
└─$ docker ps -q
4e28486ca35d

$ docker images
$ docker ps -q | xargs docker stop
$ docker-compose down
┌──(tigo㉿tigo)-[~/course_labs/labs/lab05]
└─$ docker-compose down
WARN[0000] /home/tigo/course_labs/labs/lab05/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 3/3
 ✔ Container lab05-client-1  Removed          0.0s 
 ✔ Container lab05-server-1  Removed          0.0s 
 ✔ Network lab05_app_net     Removed          0.3s 
```
✅ 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
```bash 
version: "3.8"

networks:
  app_net:

services:
  server:
    build: ./server
    ports:
      - "8000:8000"
    networks:
      - app_net
    command: python app.py
    restart: unless-stopped

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 10s
      timeout: 5s
      retries: 5

  client:
    build: ./client
    depends_on:
      server:
        condition: service_healthy
    networks:
      - app_net
    command: python client.py
    restart: on-failure


┌──(tigo㉿tigo)-[~/course_labs/labs/lab05]
└─$ curl http://localhost:8000

    <html>
    <head><title>Colorful Output</title></head>
    <body style="font-family: monospace; font-size: 24px;">
    <span style="color:red">h</span><span style="color:green">e</span><span style="color:yellow">l</span><span style="color:blue">l</span><span style="color:purple">o</span><span style="color:red"> </span><span style="color:green">a</span><span style="color:yellow">p</span><span style="color:blue">p</span><span style="color:purple">s</span><span style="color:red">e</span><span style="color:green">c</span><span style="color:yellow"> </span><span style="color:blue">w</span><span style="color:purple">o</span><span style="color:red">r</span><span style="color:green">l</span><span style="color:yellow">d</span>
    </body>
    </html>

```
✅ 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
✅ 16. Подготовьте отчет `gist`.
