# Версия Python
FROM python:3.13-slim

# 1. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/root/.local/bin:$PATH"

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем проект
COPY . .

# 6. Открываем порт
EXPOSE 8000

# 7. Команда запуска
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]