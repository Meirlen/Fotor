# Используем базовый образ с Python
FROM python:3.10-slim

# Устанавливаем необходимые зависимости для Chrome и других утилит
RUN apt-get update && apt-get install -y wget unzip curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome и ChromeDriver
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb

# Копируем файлы проекта в контейнер
WORKDIR /app
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Устанавливаем рабочую директорию и команду запуска
CMD ["python3", "main.py"]
