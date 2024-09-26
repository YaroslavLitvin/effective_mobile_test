# Используем официальный образ Python в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Устанавливаем netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Копируем скрипт ожидания доступности БД
COPY docker/app/wait_for_db.sh /usr/local/bin/wait_for_db.sh

# Делаем скрипт
RUN chmod +x /usr/local/bin/wait_for_db.sh

# Запуск скрипта ожидания доступности БД
ENV DB_HOST=database

# Ждем полного запуска контейнера с БД
# Выполняем миграцию базы данных перед запуском приложения
# Устанавливаем команду запуска приложения
CMD ["/usr/local/bin/wait_for_db.sh"]
