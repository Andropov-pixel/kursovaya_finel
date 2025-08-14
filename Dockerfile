# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код в контейнер
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Открываем порт для сервера
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]