# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем nmap и утилиты Redis
RUN apt-get update && apt-get install -y \
    nmap \
    redis-tools \
 && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Uvicorn для ASGI
RUN pip install "uvicorn[standard]"


# Открываем порт 8000
EXPOSE 8000

# Запуск через ASGI / Uvicorn
CMD ["uvicorn", "NetScope.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
