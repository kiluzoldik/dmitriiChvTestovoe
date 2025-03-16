
# Referrals API

API реферальной системы с JWT, возможностью зарегестрироваться с реферальным кодом, который храниться в кеше + рассылка кодов по email.

## Регистрация/Аутентификация

**Примечание**: Для создания пользователя требуется реальный email, так как проверка происходит через стороннее API с использованием SMTP. Если email не существует, будет выведено сообщение "Неверный формат email".

---

## Запуск с помощью Docker Compose

1. **Клонируйте проект** на ваш локальный компьютер.
2. **Откройте терминал** в корне проекта.
3. Отредактируйте файл `.env_docker` в корне проекта, подставьте туда свои данные (PostgreSQL, Redis, EmailVerify - emailhunter.co, EmailSender - smtp сервер, порт и данные от аккаунта, если gamil, то нужен пароль приложения).
4. Запустите контейнеры с помощью одной из следующих команд:

   - Если у вас есть возможность использовать Makefile:
     ```bash
     make app
     ```

   - Если Makefile недоступен, используйте команду для запуска через Docker Compose:
     ```bash
     docker compose -f docker_compose/app.yaml -f docker_compose/storage.yaml --env-file ../dmitriiChvTestovoe/.env_docker up -d --force-recreate --build
     ```

5. После успешного запуска сервисов, откройте браузер и перейдите по следующему URL:
   ```
   http://127.0.0.1:8333/docs
   ```

---

## Примечания по дебагу

Для отладки и мониторинга работы контейнеров доступны следующие команды:

- **Просмотр логов базы данных**:
  ```bash
  make storages-logs
  ```

- **Просмотр логов приложения**:
  ```bash
  make app-logs
  ```

- **Остановка всех контейнеров (БД и приложение)**:
  ```bash
  make app-down
  ```

- **Остановка контейнера только с базой данных**:
  ```bash
  make storages-down
  ```

- **Открытие терминала PostgreSQL**:
  ```bash
  make postgres
  ```

- **Запуск контейнеров БД и приложения**:
  ```bash
  make app
  ```

---

## Запуск без Docker Compose

1. **Клонируйте проект** на ваш локальный компьютер.
2. **Откройте терминал** в корне проекта.
3. Откройте файл конфигурации `app/config.py` и в строке 33 замените `.env_docker` на `.env`:
   ```python
   env_file=".env"
   ```

4. Отредактируйте файл `.env` с вашими данными PostgreSQL, Redis, API_KEY для emailhunter.co и данные для отправки на email с какого-то определенного почтового ящика.

**Пример:**
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ваш email
SMTP_PASS=пароль приложения (если это gmail)
```

5. Установите зависимости с помощью Poetry. Если Poetry не установлен, выполните команду:
   ```bash
   pip install poetry
   ```
   Если Poetry уже установлен, просто выполните:
   ```bash
   poetry install
   ```

6. Создайте БД под названием `referals`

7. Примените миграции базы данных:
   ```bash
   alembic upgrade head
   ```

8. Запустите приложение (корень проекта):

   - Исправьте 28 строку в файле main.py `app/main.py` и замените:
   `uvicorn.run("main:app", host="0.0.0.0", reload=True)`
   на
   `uvicorn.run("main:app", host="localhost", port=8000, reload=True)`

   - Для Windows:
     ```bash
     py app/main.py
     ```

   - Для Linux:
     ```bash
     python3 app/main.py
     ```

9. После запуска приложения откройте браузер и перейдите по следующему URL:
   ```
   http://localhost:8000/docs
   ```

---

## Описание API

Документация для использования API доступна по адресу:
```
http://127.0.0.1:8345/docs (docker-compose)
http://localhost:8000/docs (без docker-compose)
```
