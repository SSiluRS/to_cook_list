# Техническое задание: Платформа планирования питания (AI-Agent Ready)
Название проекта: to_cook_list
## 1. Контекст и архитектура
* **Задача:** Разработка приложения для управления продуктами, рецептами и меню.
* **Стек:** Python (FastAPI), Vue 3, PostgreSQL.
* **Инфраструктура:** Docker, Docker Compose (изолированные контейнеры).
* **Методология:** GitFlow.

## 2. Структура БД (Schema Definition)
Агент должен реализовать следующие сущности:
- **User:** Auth credentials.
- **Product:** КБЖУ справочник (name, cal, pro, fat, carb).
- **Pantry:** Связь пользователя с имеющимися продуктами (id, user_id, product_id, weight).
- **Recipe:** Конструктор рецептов (id, author_id, is_public).
- **RecipeIngredient:** Связь (recipe_id, product_id, weight_g).
- **Menu:** Планировщик (user_id, date, meal_type, recipe_id).
- **SharedAccess:** Система прав (owner, shared_with, entity_id).
- **CookingRequest:** Запросы (sender, receiver, recipe/menu_id, status).

## 3. Ключевой функционал
1.  **Калькулятор КБЖУ:** Автоматический расчет состава блюда на основе суммы ингредиентов.
2.  **Smart Matching:** Алгоритм, сравнивающий `Pantry.weight` и `RecipeIngredient.weight`, выводящий список доступных и отсутствующих ингредиентов.
3.  **Социальные функции:**
    - Шеринг рецептов между пользователями.
    - Формирование меню из чужих рецептов.
    - Система запросов "Приготовь для меня".

## 4. Требования к API
- JWT-аутентификация.
- RESTful принципы.
- Эндпоинты для: `/auth`, `/products`, `/pantry`, `/recipes`, `/menu`, `/shares`, `/cooking-requests`.

## 5. DevOps / Docker
- Корневой `docker-compose.yml` для orchestrating:
    - `db`: postgres:15-alpine
    - `backend`: python:3.11-slim
    - `frontend`: node:18-alpine (с Nginx для статики)
- Использование `depends_on` для инициализации базы.

## 6. Задачи для ИИ-агента (Workflow)
1.  **Setup:** Сгенерировать структуру каталогов и Docker-конфиги.
2.  **Backend:** Реализовать модели данных и миграции.
3.  **Logic:** Написать сервис для расчета КБЖУ и алгоритм подбора рецептов.
4.  **Frontend:** Настроить Vue 3 проект с Pinia и Axios.
5.  **Integration:** Соединить социальные функции (шеринг/запросы) с БД.