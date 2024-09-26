#!/usr/bin/env bash

host="${DB_HOST}"  # Получаем значение переменной окружения DB_HOST
port="${DB_PORT}"  # Получаем значение переменной окружения DB_PORT

until nc -z "$host" "$port"; do
  >&2 echo "Waiting for $host:$port to be available..."
  sleep 1
done

>&2 echo "$host:$port is available - executing command"

alembic upgrade head

python -m app.main