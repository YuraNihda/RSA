# Базовий образ Ubuntu
FROM ubuntu:22.04

# Встановлюємо оновлення та необхідні пакети
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean

# Встановлюємо Flask через pip
RUN pip3 install flask

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо локальні файли в контейнер
COPY project /app

# Виставляємо порт, який буде слухати Flask
EXPOSE 5000

# Встановлюємо команду запуску
CMD ["python3", "app.py"]
