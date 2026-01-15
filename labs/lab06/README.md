<div align="center">
<h1><a id="intro">Лабораторная работа №6</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Шмаков_И._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Салют :wave:,<br>
Данная лабораторная работа посвещена изучению аудита безопасности `Docker` при использовании `Docker Bench Security`. Мы рассмотрим как с ним работать. Мы разберем как проверить конфигурации безопасности и выявить их не корректность, как произвести чекап с `CIS Docker Benchmark v1.6.0`.

***

## Задание

✅ 1. Необходимо установить `Docker Engine` для Linux

```bash
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo usermod -aG docker "$USER"

$ sudo systemctl start docker
$ docker pull docker/docker-bench-security
```

✅ 2. Проверьте работу докера и сделать скрипт `audit.sh` исполняемым
✅ 3. Развернуть уязвимое приложение как отдельные стенды

```bash
$ docker compose up -d # основной web, app, postgres
$ docker-compose -f dvulnerable-app.yml up -d # поверх для vulnerable-web, debug-shell
    -f # file
    up # создает и поднимает файлы из compose
    -d # фоновый режим
```

✅ 4. Запустите скрипт из `venv` и проанализируйте то, что вывело на терминале и что вывело при конвертировании

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install openpyxl odfpy
$ ./audit.sh
$ deactivate # или $ deactivate 2>/dev/null || true
```
 
✅ 5. Проведите анализ уязвимостей, опишите их причину возникновения

Host Configuration
``` bash

Нет отдельного раздела (partition) под контейнеры → риск смешивания данных ОС и Docker-данных, сложнее контролировать заполнение диска, возможен DoS по диску.
В отчёте: 1.1 WARN

Не настроен аудит (auditd) для Docker daemon и критичных директорий/юнитов → операции с контейнерами и конфигурацией Docker не логируются, затруднено расследование инцидентов.
В отчёте: 1.5–1.10 WARN

```
Docker daemon configuration

```bash
Не ограничен сетевой трафик между контейнерами на default bridge → возможен lateral movement между контейнерами при компрометации одного из них.
В отчёте: 2.1 WARN

Не включена поддержка user namespaces → процессы в контейнерах работают с UID хоста, повышается риск container escape.
В отчёте: 2.8 WARN

Не используется механизм авторизации Docker API (authorization plugins) → отсутствует контроль и фильтрация Docker-команд.
В отчёте: 2.11 WARN

Не настроено централизованное и удалённое логирование Docker → при компрометации хоста или контейнеров логи могут быть утеряны.
В отчёте: 2.12 WARN

Не включён режим live-restore → при перезапуске Docker daemon контейнеры будут остановлены, возможна потеря доступности сервисов.
В отчёте: 2.14 WARN

Не отключён userland proxy → расширяется поверхность атаки сетевого стека Docker.
В отчёте: 2.15 WARN

Контейнеры не ограничены от получения новых привилегий по умолчанию → повышается риск повышения привилегий внутри контейнеров.
В отчёте: 2.18 WARN

```
Container Images and Build Files

```bash
Не включён Docker Content Trust → отсутствует проверка подписей образов, возможны supply-chain атаки.
В отчёте: 4.5 WARN

В образах отсутствует HEALTHCHECK → Docker не может определить фактическое состояние контейнеров, возможна «тихая» деградация сервисов.
В отчёте: 4.6 WARN


```

Container Runtime

```bash
Контейнер vulnerable-web запущен с добавлением всех Linux capabilities (CapAdd=ALL) → контейнер получает расширенные права, возможен выход на уровень ядра.
В отчёте: 5.3 WARN

Контейнер vulnerable-web запущен в privileged-режиме → контейнер фактически не изолирован от хоста, риск полного захвата системы.
В отчёте: 5.4 WARN

Контейнер использует сетевой режим host → отсутствует сетевая изоляция, возможен перехват и подмена сетевого трафика хоста.
В отчёте: 5.9 WARN

Для контейнера не заданы лимиты CPU и памяти → возможен отказ в обслуживании (DoS) за счёт исчерпания ресурсов хоста.
В отчёте: 5.10–5.11 WARN

Корневая файловая система контейнера доступна на запись → злоумышленник может закрепиться внутри контейнера (persistence).
В отчёте: 5.12 WARN

Контейнер разделяет PID namespace с хостом → возможен доступ к процессам хоста и атаки через ptrace.
В отчёте: 5.15 WARN

Отключён seccomp-профиль по умолчанию → контейнеру доступны опасные системные вызовы ядра.
В отчёте: 5.21 WARN

Docker socket (/var/run/docker.sock) смонтирован внутрь контейнера → контейнер получает полный контроль над Docker daemon и хостом.
В отчёте: 5.31 WARN

Отсутствует HEALTHCHECK на уровне runtime → невозможно автоматически определить неработоспособное состояние контейнера.
В отчёте: 5.26 WARN
```


✅ 6. Опишите влияния уязвимостей, их сценарий атаки

Host Configuration

```bash
Сценарий атаки:
Атакующий получает доступ к контейнеру или пользователю из группы docker → отсутствует аудит Docker-файлов и daemon → изменения конфигурации и запуск вредоносных контейнеров остаются незамеченными → инцидент сложно обнаружить и расследовать.

Итог:
Скрытая компрометация Docker-хост.
```
Docker daemon configuration

```bash
Сценарий атаки:
Атакующий компрометирует один контейнер → отсутствуют user namespaces и ограничения сетевого взаимодействия → атакующий перемещается между контейнерами и использует UID хоста → расширяет зону компрометации.

Итог:
Lateral movement, повышение привилегий.
```
Container Images and Build Files
```bash
Сценарий атаки:
Используется неподписанный или скомпрометированный base-image → вредоносный код запускается внутри контейнера → отсутствует HEALTHCHECK → отказ или компрометация сервиса не обнаруживается автоматически.

Итог:
Supply-chain атака, деградация сервиса.
```

Container Runtime
```bash
Сценарий атаки:
Атакующий получает RCE внутри vulnerable-web → контейнер запущен с privileged, host network, pid: host, cap_add: ALL → атакующий взаимодействует с процессами и сетью хоста → получает root-доступ к ОС.

Итог:
Полный захват Docker-хоста.
```

✅ 7. Оцените риски ИБ и предложите меры для их снижения: 
> - Следует разобрать `.yaml` описав, что в них считается не безопасным и почему
> - Опишите сценарии реализации рисков CR, DL
> - Предложили исправленные `.yaml`

vulnerable-app.yml

```bash
Небезопасный элемент: privileged: true

Описание: Контейнер запускается в привилегированном режиме без изоляции от хоста.
Риск: CR — полный захват хоста при компрометации контейнера.
Мера снижения: Убрать privileged, использовать минимальные capabilities (cap_drop: ALL).

Небезопасный элемент: network_mode: host

Описание: Контейнер использует сетевой стек хоста без изоляции.
Риск: CR — lateral movement, перехват сетевого трафика хоста.
Мера снижения: Использовать bridge-сеть и явное пробрасывание портов.

Небезопасный элемент: pid: host

Описание: Контейнер видит и может взаимодействовать с процессами хоста.
Риск: CR — вмешательство в процессы ОС, эскалация привилегий.
Мера снижения: Убрать pid: host.

Небезопасный элемент: user: "0:0"

Описание: Контейнер запускается от root-пользователя.
Риск: CR — повышение привилегий внутри контейнера.
Мера снижения: Использовать непривилегированного пользователя.

Небезопасный элемент: /var/run/docker.sock

Описание: Docker socket смонтирован внутрь контейнера.
Риск: CR — полный контроль Docker daemon и хоста.
Мера снижения: Убрать монтирование docker.sock, использовать API-прокси с авторизацией.

Небезопасный элемент: /:/hostroot:rw

Описание: Корневая файловая система хоста доступна на запись.
Риск: CR — изменение системных файлов хоста.
Мера снижения: Убрать монтирование /, использовать изолированные volume.

Небезопасный элемент: cap_add: ALL

Описание: Контейнеру доступны все Linux-capabilities.
Риск: CR — обход механизмов изоляции контейнеров.
Мера снижения: Использовать cap_drop: ALL.

Небезопасный элемент: apparmor: unconfined, seccomp: unconfined

Описание: Отключены профили безопасности.
Риск: CR — доступ к опасным системным вызовам ядра.
Мера снижения: Использовать профили AppArmor и seccomp по умолчанию.

Небезопасный элемент: Секреты в environment

Описание: Учётные данные и секреты хранятся в открытом виде.
Риск: CR — утечка данных и компрометация БД.
Мера снижения: Использовать Docker secrets или внешний vault.

```
docker-compose.yml

```bash

Небезопасный элемент: Пароли БД в environment

Описание: Пароли передаются через переменные окружения.
Риск: CR — утечка учётных данных БД.
Мера снижения: Использовать secrets или переменные из защищённого хранилища.

Небезопасный элемент: DEBUG=true

Описание: Приложение работает в режиме отладки.
Риск: CR — утечка служебной информации и stack trace.
Мера снижения: Отключить debug-режим в production.

Небезопасный элемент: RW volume ./app:/app:rw

Описание: Исходный код доступен на запись из контейнера.
Риск: CR — внедрение вредоносного кода и persistence.
Мера снижения: Использовать :ro или собирать код в образ.

Небезопасный элемент: Отсутствие лимитов ресурсов

Описание: Контейнеры не ограничены по CPU и памяти.
Риск: DL — отказ в обслуживании из-за исчерпания ресурсов хоста.
Мера снижения: Задать cpus и memory limits.

Небезопасный элемент: Отсутствие HEALTHCHECK

Описание: Docker не контролирует фактическое состояние сервиса.
Риск: DL — деградация сервиса без автоматического обнаружения.
Мера снижения: Добавить HEALTHCHECK в образ или compose.
```

✅ 8. Сделайте анализ уязвимостей из сгенерированных файлов .odt, .xslx и опишите их в отчете. Файлы конвертируются в эти директории

```bash
"├── json/          (Trivy JSON outputs)"
"├── text/          (CIS audit text outputs)"
"├── xlsx/          (Excel spreadsheets)"
"└── odt/           (OpenDocument Text files)"

docker/docker-bench-security:latest: 3 Critical уязвимости (пакеты musl, musl-utils, libseccomp) — признак устаревшей базы в образе bench (сканер тоже контейнер). Инструменты аудита надо периодически обновлять/пересобирать, иначе они сами несут CVE.

postgres:16-alpine: 4 High + 8 Medium (по stdlib v1.24.6 и т.п.). Базовый образ содержит пакеты/компоненты, требующие обновления (правильно: pin версии, регулярный rebuild, использовать патченные теги, CI-скан).

nginx:alpine: 1 Medium (пакет c-ares). "c-ares: c-ares: Denial of Service due to query termination after maximum attempts"

python:3.11-alpine: 1 Medium (уязвимость в pip). "Title": "pip: pip missing checks on symbolic link extraction"
```

✅ 9. Подготовьте отчет `gist`.
✅ 10. Почистите кеш от `venv` и остановите уязвимостей приложение, почистите контейнера

```bash
$ rm -rf venv
$ docker-compose -f demo-vulnerable-app.yml down
$ docker system prune -f
```
 
***

## Troobleshooting

- Права для исполнения скрипта

```bash
$ chmod +x xxx.sh # разрешение прав при permission denied
```

- На macOS/AArch64 docker-bench-security может не запускаться из‑за ограничений Docker Desktop и это работает для Linux‑VM. На Mac используем Trivy‑скан и разбор конфигурации compose‑файлов.

***

## Links

- [Docker](https://docs.docker.com/)
- [Docker Engine security](https://docs.docker.com/engine/security/)
- [Docker Bench for Security](https://github.com/docker/docker-bench-security)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Trivy: Container Security Scanner](https://aquasecurity.github.io/trivy/)
- [Markdown](https://stackedit.io)
- [Gist](https://gist.github.com)
- [GitHub Docs](https://docs.github.com/en)
- [GitHub CLI](https://cli.github.com)

Copyright (c) 2025 Elijah S Shmakov

![Logo](../../assets/logotype/logo.jpg)
