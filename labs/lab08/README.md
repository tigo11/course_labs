<div align="center">
<h1><a id="intro">Лабораторная работа №8</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Шмаков_И._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Салют :wave:,<br>
Данная лабораторная работа посвящена динамическому анализу безопасности web‑приложений DAST с использованием OWASP ZAP. Вы развернёте уязвимое приложение в Docker, проведете ручное тестирование по инструкции для понимания принципа и логики работы, далее выполните автоматическое сканирование, проанализируете отчёт и опишете уязвимости как и каким образом они реализуются. Аналогично вы проанализируете риски ИБ и предложите меры защиты, внесете необходимые исправления.

***

***

## Задание

✅ 1. Разверните и подготовьте окружение для уязвимого приложения

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt && vulnerable-app/requirements.txt 
```

✅ 2. Запустите уязвимое приложение

```bash
$ docker-compose up -d --build  # http://localhost:8080

┌──(venv)─(tigo㉿tigo)-[~/course_labs/labs/lab08]
└─$ docker-compose up -d --build

[+] Building 10.0s (12/12) FINISHED docker:default
[+] Running 3/3
 ✔ vulnerable-app                  Built      0.0s 
 ✔ Network lab08-net               Created    0.1s 
 ✔ Container lab08-vulnerable-app  Started    0.3s 
   
```

✅ 3. Проверьте доступность приложения

```bash
$ curl -i http://localhost:8080

┌──(tigo㉿tigo)-[~]
└─$ curl -i http://localhost:8080 
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.11.14
Date: Wed, 14 Jan 2026 22:35:20 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 625
Set-Cookie: session=guest-session-id; Path=/
Connection: close


    <h1>Vulnerable DAST Demo App</h1>
    <p>Пример уязвимого приложения для лабораторной по DAST.</p>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (зависит от cookie)</a></li>
      <li><a href="/admin">«Админка» без нормальной авторизации</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>

```

✅ 4. Проведите ручное исследование уязвимостей и опишите почему такое происходит, каким образом реализуются уязвимости и дайте им определение


✅ 4.1. `/echo` - проверить отражение параметра  `msg`  в `HTML` и использовать `payload` вида  `<script>alert('XSS')</script>` зафиксировав его поведение

```bash
http://localhost:8080/echo?msg=<script>alert('hack with XSS')</script>

# На дисплее вывелось сообщение
```

✅ 4.2. `/search` - проверить обычный запрос  `?username=admin` и использовать строку  `?username=admin' OR '1'='1` зафиксировав его поведение описав признак SQLi

```bash
http://localhost:8080/search?username=admin' OR '1'='1

Поиск пользователя

Запрос: SELECT id, username, role FROM users WHERE username = 'admin'

    3 – admin (admin)

Попробуйте, например: ?username=admin' OR '1'='1

http://localhost:8080/search?username=admin' OR '1'='1

Поиск пользователя

Запрос: SELECT id, username, role FROM users WHERE username = 'admin' OR '1'='1'

    3 – admin (admin)
    4 – user (user)

Попробуйте, например: ?username=admin' OR '1'='1
```

✅ 4.3. `/login` - войти под  `admin`  и  `user` проверив логику на открытые пароли и простые SQL‑запросы
```bash
http://localhost:8080/login
admin
admin123

Добро пожаловать, admin (admin)!
На главную

user
user123
Добро пожаловать, user (user)!
На главную
```
✅ 4.4. `/profile` - изменить `cookie  role`  на  `admin`  через `DevTools` → `Application` → `Cookies` и обновить  `/profile` (возможно создать `cookie`
меняем role на admin

✅ 4.5. `/admin` -  проверить, что доступ запрещён без `cookie  role=admin` и далее подделать `cookie`, что «админка» открывается путем изменения через `DevTools`. **Подсказка:** доступ завязан на значение cookie, без подписи/ токена/ серверной проверки.
```bash
Admin panel

Секретные настройки приложения (демо).

    DEBUG: true
    FEATURE_FLAG: experimental_mode

```
✅ 4.6. `/files/` - просмотрите `directory listing` и откройте один из файлов убедившись, что оно выводится

```bash
http://localhost:8080/files/

Files under /files/

    secret.txt

Пример directory listing без ограничений.

http://localhost:8080/files/secret.txt
SECRET_TOKEN=123456
```

✅ 5. Доработайте по пп 4 лабораторную работу развив их содержимое, которое может выводиться (мин 1 пример)
``` bash
http://localhost:8080/echo?msg=<img src=x onerror=alert('xss')>

изображение x не существует, браузер вызывает обработчик onerror, в результате чего выполняется JavaScript-код alert('xss')

admin' OR '1'='1

В параметре username передаётся SQL-выражение
SELECT id, username, role FROM users WHERE username = '' OR 1=1 --'
Условие OR 1=1 всегда истинно
В результате сервер возвращает все записи из таблицы users


```
✅ 6. Поставьте `OWASP ZAP` и стяните образ конкртеной версии для него

```bash
$ brew install --cask zap
$ docker pull ghcr.io/zaproxy/zaproxy:stable
```

✅ 7. Задайте переменные окружения для работы скриптов

```bash
$ export ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable
$ TARGET_URL="${TARGET_URL:-http://host.docker.internal:8080}"
```

✅ 8. Запустите скрипт автоматического сканирования DAST `OWASP ZAP`

```bash
$ ./zap_scan.sh
```

✅ 9. Изучите сгенерированные отчеты в `dast/reports` и опишите риски ИБ для них, без сценариев, так как ранее вы видели часть из их реализации
```bash
1. Content Security Policy (CSP) Header Not Set — Medium

Риск ИБ:
Повышается вероятность эксплуатации XSS-уязвимостей, так как браузер не ограничивает выполнение внедрённого JavaScript-кода.

2. Missing Anti-clickjacking Header — Medium

Риск ИБ:
Приложение может быть встроено во фрейм злоумышленника, что позволяет проводить clickjacking-атаки и вынуждать пользователя выполнять нежелательные действия.

3. Source Code Disclosure – SQL — Medium

Риск ИБ:
Раскрытие структуры БД и логики запросов упрощает эксплуатацию SQL-инъекций и анализ приложения злоумышленником.

4. Cookie No HttpOnly Flag — Low

Риск ИБ:
При успешной XSS-атаке JavaScript может получить доступ к cookie и похитить сессионные данные.

5. Cookie without SameSite Attribute — Low

Риск ИБ:
Повышается риск CSRF-атак, так как cookie отправляется при кросс-сайтовых запросах.

6. Missing Security Headers (X-Content-Type-Options, Permissions-Policy и др.) — Low

Риск ИБ:
Браузер может интерпретировать контент небезопасным образом, что увеличивает поверхность атаки.

7. Server Leaks Version Information — Low

Риск ИБ:
Упрощает fingerprinting сервера и подбор известных уязвимостей.

8. Information Disclosure – Sensitive Data in URL — Informational

Риск ИБ:
Чувствительные данные могут попасть в логи, историю браузера или прокси-серверы.

```

✅ 10. Внесите исправления по данному отчету `DAST` для `vulnerable-app/app.py`
```bash
Исправил

1) Reflected XSS в /echo
2) SQL Injection в /search и /login
3) CSP проблема “Failure to Define Directive with No Fallback”
4) “Insufficient Site Isolation Against Spectre” (COOP/COEP/CORP)
5) риск утечки через shared cache
6) Directory Listing + чтение любых файлов в /files/
7) Cookie security
8) Утечка лишнего через debug
9) Базовые security headers

Low: 1 
Info: 3

```

✅ 11. Делайте все необходимые коммиты по шагам и отправляйте изменения в удалённый репозиторий
✅ 12. Подготовьте отчет `gist`.
✅ 14. Почистите кеш от `venv` и остановите уязвимое приложение

```bash
$ deactivate
$ rm -rf venv
$ docker-compose -f docker-compose.yml down
$ docker system prune -f
```
