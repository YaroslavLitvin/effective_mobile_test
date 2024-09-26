# Используем официальный образ Nginx в качестве базового
FROM nginx:latest

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем статические файлы приложения в контейнер
COPY /app/static /usr/share/nginx/html

# Копируем файл конфигурации для FastAPI в контейнер
COPY fastapi.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80 для доступа к Nginx
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
