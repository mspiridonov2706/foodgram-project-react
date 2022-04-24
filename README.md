![foodgram_workflow](https://github.com/Muxa2793/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# YANDEX PRAKTIKUM DIPLOM PROJECT

## FOODGRAM

### Описание

Платформа которой вы можете публиковать рецепты, добавлять чужие рецепты
в избранное и подписываться на публикации других авторов,
а также создавать и скачивать свои списки для покупок.

#### Запуск приложения

- подготовьте ваш сервер (рекомендуемая система):
  - установите [Docker](https://docs.docker.com/engine/install/) и [Docker-compose](https://docs.docker.com/compose/install/)
- Сделайте fork данного репозитория к себе;
- Создайте в Repository secrets на Github следующие секреты:

```bash
SECRET_KEY=your_secret_key_for_django
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=your_postgres_db_name
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
DB_HOST=db
DB_PORT=5432
SERVER_HOST=your_host_ip
SERVER_USER=your_host_username
SSH_KEY=your_private_ssh_key
TELEGRAM_TO=your_telegram_id (по-желанию)
TELEGRAM_TOKEN=your_bot_token (по-желанию)
```

- создайте и запустите свой github workflow:
    <details><summary>cодержание файла workflow <strong>main.yml</strong></summary>

    </details>
- создайте суперпользователя на сервере:

```bash
docker-compose exec web python manage.py createsuperuser
```

#### Описание API приложения можно посмотреть в документации проекта после запуска сервера

```bash
GET HOST_IP/redoc/
```

#### Технологии

    Python
    django rest_framework
    docker
    docker-compose

#### Авторы

Команда [Яндекс.Практикума](https://practicum.yandex.ru/profile/python-developer-plus/ "Яндекс.Практикум") и [Михаил Спиридонов](https://t.me/MikhailSpiridonov "Мой Telegram для связи").

#### License

MIT

#### Ссылки
1) http://51.250.15.246/api/
2) http://51.250.15.246/admin/
2) http://51.250.15.246/redoc/
3) суперпользователь:
   - логин - admin
   - пароль - admin
   - почта - admin@example.com
