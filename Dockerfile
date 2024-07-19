# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \

# Устанавливаем Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get install -y google-chrome-stable

# Получаем последнюю версию ChromeDriver, соответствующую версии Chrome
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+') && \
    CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"

# Устанавливаем ChromeDriver
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/
RUN rm /tmp/chromedriver.zip

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
