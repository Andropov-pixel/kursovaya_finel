# Используем официальный образ Nginx
FROM nginx:latest

# Создаем деректорию для статических фаилов
RUN mkdir -p /app/staticfiles

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.confa

# # Копируем статические файлы веб-сайта в директорию для обслуживания
# COPY html/ /usr/share/nginx/html/

# Открываем порт 80 для HTTP-трафика
EXPOSE 80