# Project
CRM для автоматизации процессов автосервиса. Позволяет управлять заказами, клиентами, механиками и отслеживать статус выполнения работ.

## Роли
### Client
Клиенту доступны профиль, где можно редактировать личную информацию. Просмотр и создание заказов на ремонт своего авто и дальнейшее отслеживание статуса работы.

### Mechanic
Механик может просматривать заказы которые на него назначил менеджер, переводить заказ в статуы "Взят в работу", "Готов".

### Manager
Менеджер может создавать заказы, редактировать их. Просматривать всех пользователей и сотрудников, а также заказы, которые им принадлежат. Имеет возможность видеть все заказы в системе, менять их статусы, назначать заказы на механиков. Имеет доступ к разделу со статистикой работы сервиса.

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

# Getting started
``` bash
git clone https://github.com/Moonlightwas/autoservice-crm.git
cd autoservice-crm
```

Необходимо настроить переменные окружения
``` bash
cp backend/.env.example backend/.env
cp frontend/.env.example .frontend/.env
```

Запуск
``` bash
docker compose up -d --build
```

# Доступ
http://localhost -> frondend \
http://localhost/api/ -> backend \
http://localhost/admin -> django admin

# Tests
Django tests
``` bash
cd backend/ && pytest
```

При запуске контейнера автоматически создаются пользователи

Role | Email | Password |
|---|--------|----------|
| admin | admin@example.com | qwerty@123 |
| mechanic | mechanic@example.com | qwerty@123 |
| client | client@example.com | qwerty@123 |