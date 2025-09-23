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

## ⚙️ Установка и запуск

```bash
# Собрать и запустить контейнеры
docker-compose up --build -d

# Создать миграции
docker-compose exec web python manage.py makemigrations

# Применить миграции
docker-compose exec web python manage.py migrate

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

# Загрузить фикстуры
docker-compose exec web python manage.py loaddata fixtures/categories fixtures/subcategories fixtures/products fixtures/product_images
```
