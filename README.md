# Project
CRM для автоматизации процессов автосервиса. Позволяет управлять заказами, клиентами, механиками и отслеживать статус выполнения работ.

## Роли
### Client
Клиенту доступны профиль, где можно редактировать личную информацию. Просмотр и создание заказов на ремонт своего авто и дальнейшее отслеживание статуса работы.

### Mechanic
Механик может просматривать заказы которые на него назначил менеджер, переводить заказ в статуы "Взят в работу", "Готов".

### Manager
Менеджер может создавать заказы, редактировать их. Просматривать всех пользователей и сотрудников, а также заказы, которые им принадлежат. Имеет возможность видеть все заказы в системе, менять их статусы, назначать заказы на механиков. Имеет доступ к разделу со статистикой работы сервиса.

### Admin
Админ имеет все выше перечисленные права + админка DRF.

# Stack

**Backend**
- DRF
- JWT authentication
- PostgreSQL

**Frontend**
- Vue js
- Bootstrap
- Pinia

**DevOps**
- Docker compose
- Nginx

# Запуск
``` bash
git clone https://github.com/Moonlightwas/autoservice-crm.git
cd autoservice-crm
```

Настройка переменных окружения
``` bash
cp backend/.env.example backend/.env
cp frontend/.env.example .frontend/.env
```
# Docker
## Dev
Для локальной разработки. Контейнеры монтирует католг с хоста, любые изменения в бэке иил фронте будут отображаться сразу.
``` bash
docker compose -f docker-compse.dev.yml up -d --build
```
### Доступ
http://localhost:3000 -> frondend \
http://localhost:8000 -> backend

## Prod
Для запуска на удаленном сервере Все запросы идут через nginx.
``` bash
docker compose -f docker-compse.prod.yml up -d --build
```
### Доступ
http://localhost -> frondend \
http://localhost/api/ -> backend \
http://localhost/admin -> django admin

# Tests
Backend tests

При запуске вне контейнера нужно указать POSTGRES_HOST=localhost в .env 
``` bash
cd backend/ && pytest
```

Запуск тестов в контейнере
``` bash
docker compose -f docker-compose.dev.yml exec backend pytest
```

При запуске docker-compse.prod.yml автоматически создаются тестовые пользователи

Role | Email | Password |
|---|--------|----------|
| admin | admin@example.com | qwerty@123 |
| mechanic | mechanic@example.com | qwerty@123 |
| client | client@example.com | qwerty@123 |
