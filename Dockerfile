# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем пакеты и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


# Устанавливаем необходимые зависимости для запуска ChromeDriver
RUN apt-get update && apt-get install -y \
    xvfb \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы в рабочую директорию
COPY . /app

# Устанавливаем зависимости (если у вас есть requirements.txt)
# COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Если нет файла requirements.txt, можно установить зависимости прямо в Dockerfile, например:
# RUN pip install --no-cache-dir some_dependency another_dependency

# set display port to avoid crash
ENV DISPLAY=:99

# Указываем команду для запуска вашего приложения
CMD ["python", "main.py"]
