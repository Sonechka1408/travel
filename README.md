# Travel Portal Microservices

Микросервисная архитектура для туристического портала, разделенная на следующие сервисы:

- **auth-service**: Аутентификация и управление пользователями (порт 8000)
- **destination-service**: Управление направлениями путешествий (порт 8001)
- **comment-service**: Управление комментариями (порт 8002)
- **like-service**: Система лайков/дизлайков (порт 8003)
- **nginx**: Веб-сервер и обратный прокси (порт 80)

## Требования

- Docker
- Docker Compose

## Структура проекта

```
travel-portal/
├── auth-service/
├── destination-service/
├── comment-service/
├── like-service/
├── nginx/
├── docker-compose.yml
├── deploy-local.sh
└── README.md
```

## Локальное развертывание

1. Убедитесь, что Docker и Docker Compose установлены:
```bash
docker --version
docker-compose --version
```

2. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd travel-portal
```

3. Сделайте скрипт развертывания исполняемым:
```bash
chmod +x deploy-local.sh
```

4. Запустите скрипт развертывания:
```bash
./deploy-local.sh
```

5. После завершения развертывания, приложение будет доступно по адресу:
```
http://localhost
```

## API Endpoints

### Auth Service
- `POST /api/auth/login/`: Вход в систему
- `POST /api/auth/register/`: Регистрация
- `POST /api/auth/logout/`: Выход из системы

### Destination Service
- `GET /api/destinations/`: Список направлений
- `GET /api/destinations/{id}/`: Детали направления
- `POST /api/destinations/`: Создание направления (только для админов)

### Comment Service
- `GET /api/comments/{destination_id}/`: Получение комментариев
- `POST /api/comments/create/`: Создание комментария
- `DELETE /api/comments/delete/`: Удаление комментария (только для админов)

### Like Service
- `POST /api/likes/`: Поставить/убрать лайк или дизлайк

## Разработка

Каждый сервис имеет свой собственный Dockerfile и requirements.txt. При необходимости внести изменения в сервис:

1. Внесите изменения в код
2. Пересоберите контейнеры:
```bash
docker-compose up -d --build
```

## Мониторинг

Для просмотра логов сервисов:
```bash
docker-compose logs -f [service-name]
```

## Остановка сервисов

Для остановки всех сервисов:
```bash
docker-compose down
```

Для остановки с удалением томов:
```bash
docker-compose down -v
``` 
