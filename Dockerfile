# Используем последнюю версию операционной системы Alpine, на основе которой будет создан контейнер
FROM alpine:latest

# Устанавливаем список пакетов python3, ImageMagick,
# библиотек для поддержки форматов JPEG, PNG, WEBP, TIFF, Ghostscript для работы с PDF
RUN apk add --no-cache python3 python3-dev py3-pip build-base \
    imagemagick imagemagick-dev \
    libjpeg-turbo-dev libpng-dev libwebp-dev tiff-dev \
    ghostscript

# Устанавливаем рабочую директорию в /app/
WORKDIR /app/

# Создаем виртуальное окружение в /app/venv
RUN python3 -m venv /app/venv

# Устанавливаем переменную среды PATH для использования виртуального окружения
ENV PATH="/app/venv/bin:$PATH"

# Копируем все файлы и папки из текущего рабочего каталога внутрь контейнера в папку /app
COPY . /app

# Обновляем пакетный менеджр и устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Открываем порт 80
EXPOSE 80

# Запуск файла main.py с использованием Python 3 по указанному пути
CMD ["python3", "/app/main.py"]
