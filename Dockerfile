# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \

# Устанавливаем Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Скачиваем и устанавливаем ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


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
