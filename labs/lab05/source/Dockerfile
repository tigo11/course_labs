FROM python:3.11-slim AS builder
#Рабочая директория внутри контейнера
WORKDIR /app
# Копируем файл зависимостей
COPY requirements.txt .
# Обновляем pip и собираем wheel-пакеты зависимостей
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.11-slim 
WORKDIR /app
# Копируем заранее собранные wheel-пакеты
COPY --from=builder /wheels /wheels 
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt
# Копируем исходный код приложения
COPY app.py .
# Нужно для логирования в Docker
ENV PYTHONUNBUFFERED=1
# Команда запуска контейнера
CMD ["python", "app.py"]
