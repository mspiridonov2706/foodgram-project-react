![foodgram_workflow](https://github.com/Muxa2793/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# YANDEX PRAKTIKUM DIPLOM PROJECT

## FOODGRAM

### Описание

Платформа которой вы можете публиковать рецепты, добавлять чужие рецепты
в избранное и подписываться на публикации других авторов,
а также создавать и скачивать свои списки для покупок.

#### Запуск приложения

- подготовьте ваш сервер (рекомендуемая система):
  - установите [Docker](https://docs.docker.com/engine/install/) и [Docker-compose](https://docs.docker.com/compose/install/);
  - сделайте fork данного репозитория к себе;
  - склонируйте репозиторий на ваш сервер;
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

    ```yaml
    name: foodgram workflow
    on: [push]
    jobs:
      deploy:
        name: Deploy on server
        runs-on: ubuntu-latest
        steps:
          - name: executing remote ssh commands to deploy
            uses: appleboy/ssh-action@master
            with:
              host: ${{ secrets.SERVER_HOST }}
              username: ${{ secrets.SERVER_USER }}
              key: ${{ secrets.SSH_KEY }}
              script: |
                cd foodgram-project-react
                touch .env
                echo SECRET_KEY=${{ secrets.SECRET_KEY }} >> .env
                echo DB_ENGINE=${{ secrets.DB_ENGINE }} >> .env
                echo POSTGRES_DB=${{ secrets.POSTGRES_DB }} >> .env
                echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
                echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env
                echo DB_HOST=${{ secrets.DB_HOST }} >> .env
                echo DB_PORT=${{ secrets.DB_PORT }} >> .env
                cd infra
                sudo docker-compose up -d --build
                sudo docker-compose exec -T backend python manage.py collectstatic --no-input
                sudo docker-compose exec -T backend python manage.py makemigrations
                sudo docker-compose exec -T backend python manage.py migrate
    ```

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
1) http://51.250.15.246
2) http://51.250.15.246/api/
3) http://51.250.15.246/admin/
4) http://51.250.15.246/api/docs/
5) суперпользователь:
   - логин - admin
   - пароль - admin
   - почта - admin@example.com
