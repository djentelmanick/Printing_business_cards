# Printing business cards

Данный проект создан для автоматизации подготовки визиток для печати

## Установка

1. Клонировать репозиторий:

   ```bash
   git clone https://git.miem.hse.ru/nvpliasov/printing_business_cards.git
   ```
   
2. Перейти в директорию проекта:

    ```bash
    cd ваш_проект
    ```

3. Cоздайте виртуальное окружение

    ```bash
    python3 -m venv venv
    ```

4. Активируйте виртуальное окружение

    - Unix

    ```bash
    source venv/bin/activate
    ```

    - Windows

    ```
    venv\Scripts\activate
    ```

5. Установить зависимости:

   ```bash
    pip install -r requirements.txt
   ```

## Использование

### config.py

В src/config.py можно настроить дополнительные параметры:
- DPI
- Отступ до визитки от края листа
- Вылет под обрез с одной стороны
- Длину, ширину и цвет маркера для резки

### Запуск
```bash
python main.py
```

## Роуты

      - /
      Единственный роут, на котором происоходит загрузка данных на сервер и получение pdf файла для печати

## Деплой

1. Откройте Docker Desktop.
2. Перейдите в каталог, содержащий ваш файл docker-compose.yml.
3. Выполните следующую команду для запуска контейнера, описанного в файле docker-compose.yml:

    ```bash
    docker-compose up --build
    ```
