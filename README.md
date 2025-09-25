# 🛒 Интернет-магазин продуктов — API на Django REST Framework

REST API для интернет-магазина продуктов с функционалом категорий, подкатегорий, продуктов и корзины.
Реализовано с использованием Django, Django REST Framework, JWT-авторизации и Swagger.

## 🚀 Возможности

- Категории и подкатегории (CRUD в админке, эндпоинт со списком + пагинация).
- Продукты (CRUD в админке, эндпоинт со списком + пагинация).
- Авторизация по токену.
- Корзина (для авторизованных пользователей):
  - добавление товара,
  - изменение количества,
  - удаление товара,
  - очистка корзины,
  - подсчет суммы и количества.
- Swagger-документация (`/api/schema/swagger-ui/`).
- Фикстуры для категорий/подкатегорий/продуктов.
- Автотесты (GET продуктов, POST корзина).

## 🔧 Настройки окружения

Проект использует файл `.env` для хранения секретных и конфиденциальных данных.
Создайте `.env` в корне проекта со следующим содержимым (пример):

```env
SECRET_KEY='example'
DEBUG=False
ALLOWED_HOSTS=*,0.0.0.0,localhost,127.0.0.1
DB_NAME=example
DB_USER=example
DB_PASSWORD=example
DB_HOST=db
DB_PORT=5432
CSRF_TRUSTED_ORIGINS=''
```

## ⚙️ Установка и запуск

### 1. С Docker (рекомендуется)

```bash
# Собрать и запустить контейнеры
docker-compose up --build -d

# Создать миграции
docker-compose exec web python manage.py makemigrations

# Применить миграции
docker-compose exec web python manage.py migrate

# Собрать статику и статические файлы
docker-compose exec web python manage.py collectstatic --noinput

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

# Загрузить фикстуры
docker-compose exec web python manage.py loaddata fixtures/categories fixtures/subcategories fixtures/products fixtures/product_images
```

### 1. Без Docker

```bash
# Создать виртуальное окружение и активировать его
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл с настройками

# Создать и применить миграции
python manage.py makemigrations
python manage.py migrate

# Собрать статику и статические файлы
python manage.py collectstatic --noinput

# Создать суперпользователя
python manage.py createsuperuser

# Загрузить фикстуры
python manage.py loaddata fixtures/categories fixtures/subcategories fixtures/products fixtures/product_images

# Запустить сервер
python manage.py runserver
```

## ✅ Тестирование

```bash
# Через Docker
docker-compose exec web pytest

# Локально
pytest
```
