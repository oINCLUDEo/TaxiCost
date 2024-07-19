# Используем базовый образ Python
FROM python:3.9

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
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем версию ChromeDriver, совместимую с установленной версией Google Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $2}' | cut -d. -f1,2) && \
    echo "Detected Chrome version: $CHROME_VERSION" && \
    CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION) && \
    echo "Detected ChromeDriver version: $CHROME_DRIVER_VERSION" && \
    wget -q -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

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
