# JG Servers Bot

Telegram-бот для продажи VPS-серверов с гибкой настройкой.

## Функции
- Покупка VPS (страна, тип, трафик, срок аренды, оплата криптой/фиатом через админа) 
- Личный кабинет: просмотр и продление серверов 
- Админ-панель: управление заказами и пользователями /admin 

## Стек
- Python3.12.3, Poetry  
- Aiogram, SQLAlchemy, Alembic  
- Aiocryptopay (асинхронная библиотека для API Crypto Bot в telegram)  
- PostgreSQL  
- Docker, Docker-Compose  

## Запуск
```bash
git clone git@github.com:thetrueryan/JG_PRIVATE_SERVERS.git
cd JG_PRIVATE_SERVERS
cp .env.example .env
poetry install
poetry shell
alembic upgrade head
python src/main.py
```
## Docker
```bash
docker build <your_container_name> .
```

замените название образа в docker-compose.yml с
- thetrueryan/jg_servers_bot:prod_v2.1
- на название вашего контейнера (то что указали в docker build)

запустите через docker compose
```bash
docker compose up -d
```
Если выдает ошибку запустите таким способом
```bash
docker compose down && docker compose up --build -d
```

## Переменные окружения

database config:
- DB_HOST=Название хоста (если запускаете на своем компьютере то введите localhost)
- DB_PORT=Ваш порт (5432 стандартный)
- DB_USER=Ваше имя пользователя в базе (postgres по умолчанию)
- DB_PASS=Ваш пароль от базы 
- DB_NAME=Имя для вашей базы (например tg_servers)

bot config:
- ADMIN_TG_ID=Ваш telegram id (или telegram id аккаунта которому вы хотите дать права админа)
- ADMIN_TG_USERNAME=Ваш telegram username (через @, например @username)
- BOT_TOKEN=Токен вашего бота (создайте через @BotFather и скопируйте сюда)
- CRYPTOBOT_API_TOKEN=API токен вашего приложения в crypto bot @CryptoBot

## Прочее
Бот был написан для личных нужд + как учебный pet проект для портфолио.
TG для связи:
@ttryan

