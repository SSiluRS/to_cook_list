# Culinary Navigator (to_cook_list)

Умный кулинарный навигатор с возможностью учета продуктов в кладовой, расчетом КБЖУ и планированием меню.

---

## Технологический стек

- **Бэкенд:** Python (FastAPI, SQLAlchemy, Uvicorn)
- **Фронтенд:** Vue.js (Composition API, Pinia, TailwindCSS, Vite)
- **База данных:** MariaDB / SQLite
- **CI/CD:** GitHub Actions (сборка Docker-образов в GHCR)
- **Контейнеризация:** Docker / Docker Compose

---

## Архитектура развертывания и CI/CD

Проект настроен на автоматическую сборку и публикацию Docker-образов в **GitHub Container Registry (GHCR)**:
- Бэкенд-сервис: `ghcr.io/<owner>/to_cook_list_back:latest`
- Фронтенд-сервис (раздается через Nginx): `ghcr.io/<owner>/to_cook_list_front:latest`

Сборка запускается автоматически при пуше изменений в ветку `master` или при публикации соответствующих тегов (`back-v*` / `front-v*`).

---

## Локальный запуск (Разработка)

### Требования
- Docker и Docker Compose

### Инструкция по запуску
1. Склонируйте репозиторий.
2. Для подключения к вашей внешней СУБД MariaDB создайте файл `.env` в корне проекта:
   ```env
   DATABASE_URL=mysql+pymysql://<user>:<password>@<maria_db_host>:<port>/to_cook_list
   ```
   *(Если файл `.env` не создан, проект автоматически запустит и настроит локальный контейнер MariaDB).*
3. Запустите стек:
   ```bash
   docker compose up -d --build
   ```
4. Приложение будет доступно по адресам:
   - Фронтенд: `http://localhost:5173`
   - Бэкенд API: `http://localhost:8000`

---

## Тестирование

Запуск E2E-тестов с помощью Playwright во фронтенд-директории:
```bash
cd frontend
npx playwright test
```
