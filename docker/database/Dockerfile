# Используем официальный образ PostgreSQL в качестве базового
FROM postgres:latest

# Устанавливаем переменные окружения для конфигурации базы данных
ENV POSTGRES_USER=${DB_USER}
ENV POSTGRES_PASSWORD=${DB_PASS}
ENV POSTGRES_DB=${DB_NAME}
ENV PGPORT=${DB_PORT}

# Устанавливаем команду запуска контейнера
CMD ["postgres"]
