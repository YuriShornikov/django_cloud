# Django Cloud Deployment Guide

## 1. Локальный запуск проекта

### 1.1. Клонирование репозитория
```sh
git clone https://github.com/YuriShornikov/django_cloud.git
cd django_cloud
```

### 1.2. Настройка backend
1. Создаем `.env` в `backend` напримере `.env.example`:
    ```python
    SECRET_KEY='создаемСвойКлюч'
    DEBUG=True
    DB_NAME=mycloud
    DB_USER=postgres
    DB_PASSWORD=admin1234
    DB_HOST=localhost
    DB_PORT=5432

    # Указывает, запущен ли сервер в продакшене, если сервер, ставим - True
    IS_SERVER=False

    # Базовый URL для сервера
    BASE_URL=http://<IP_СЕРВЕРА>:8000

    # Разрешенные хосты, укажите свой ip в конце
    ALLOWED_HOSTS=localhost,127.0.0.1,localhost:5173,<IP_СЕРВЕРА>
    ```

### 1.3. Создание базы данных
```sh
python manage.py migrate
```

### 1.4. Запуск backend
```sh
python manage.py runserver
```

### 1.5. Запуск frontend
```sh
cd frontend
npm install
npm run dev
```

---

## 2. Развертывание на сервере (REG.RU)

### 2.1. Создание сервера
1. Войти в **REG.RU** → **Мои ресурсы** → **Виртуальные машины**.
2. Добавить **Ubuntu** с **SSH-ключом**.

### 2.2. Подключение к серверу
```sh
ssh root@<IP_СЕРВЕРА>
```

### 2.3. Создание нового пользователя
```sh
adduser aukor
usermod -aG sudo aukor
su aukor
cd ~
```

### 2.4. Обновление и установка зависимостей
```sh
sudo apt update
sudo apt install python3-venv python3-pip postgresql nginx
```

### 2.5. Клонирование проекта
```sh
git clone https://github.com/YuriShornikov/django_cloud.git
cd django_cloud
```

### 2.6. Настройка backend
1. В папке создаем файл `backend/.env`, как файл `.env.example`:
    ```env
    SECRET_KEY='создаемСвойКлюч'
    DEBUG=True
    DB_NAME=mycloud
    DB_USER=postgres
    DB_PASSWORD=admin1234
    DB_HOST=localhost
    DB_PORT=5432

    # Указывает, запущен ли сервер в продакшене, если сервер, ставим - True
    IS_SERVER=True

    # Базовый URL для сервера
    BASE_URL=http://<IP_СЕРВЕРА>:8000

    # Разрешенные хосты, укажите свой ip в конце
    ALLOWED_HOSTS=localhost,127.0.0.1,localhost:5173,<IP_СЕРВЕРА>
    ```

### 2.7. Настройка frontend
1. В файле `frontend/.env.production` заменить:
    ```env
    VITE_API_BASE_URL=http://<IP_СЕРВЕРА>:8000/
    ```
2. Выполнить сборку фронтенда:
    ```sh
    cd frontend
    npm install
    npm run build
    cd ..
    ```

---

## 3. Настройка базы данных PostgreSQL

```sh
sudo su postgres
psql
```
```sql
ALTER USER postgres WITH PASSWORD 'admin1234';
CREATE DATABASE mycloud;
\q
exit
```

---

## 4. Настройка виртуального окружения и запуск backend

```sh
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

---

## 5. Настройка Gunicorn

Создать файл сервиса Gunicorn:
```sh
sudo nano /etc/systemd/system/gunicorn.service
```
Вставить:
```ini
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=aukor
Group=www-data
WorkingDirectory=/home/aukor/django_cloud/backend
ExecStart=/home/aukor/django_cloud/backend/env/bin/gunicorn --access-logfile - --workers=3 --bind unix:/home/aukor/django_cloud/backend/mycloud/project.sock mycloud.wsgi:application

[Install]
WantedBy=multi-user.target
```
Сохранить и выполнить:
```sh
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## 6. Настройка Nginx

Создать конфигурационный файл:
```sh
sudo nano /etc/nginx/sites-available/my_project
```
Вставить:
```nginx
server {
    listen 80;
    server_name <IP_СЕРВЕРА>;

    client_max_body_size 100M;

    location / {
        root /home/aukor/django_cloud/frontend/dist;
        index index.html;
        try_files $uri /index.html;
    }

    location /assets/ {
        root /home/aukor/django_cloud/frontend/dist;
        try_files $uri =404;
    }
}

server {
    listen 8000;
    server_name <IP_СЕРВЕРА>;

    client_max_body_size 100M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/aukor/django_cloud/backend/mycloud/project.sock;
    }

    location /media/ {
        alias /home/aukor/django_cloud/backend/media/;
        autoindex on;
    }

    location /static/ {
        alias /home/aukor/django_cloud/backend/static/;
    }
}
```
Активировать конфигурацию:
```sh
sudo ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enabled/
ls -l /etc/nginx/sites-enabled/
```

---

## 7. Запуск Nginx и финальные настройки

```sh
sudo systemctl start nginx
sudo ufw allow 'Nginx Full'
python manage.py collectstatic
sudo chmod 755 /home /home/aukor /home/aukor/django_cloud
mkdir -p /home/aukor/django_cloud/backend/media
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```

---

## 8. Проверка работы

Проект должен работать. Если есть ошибки, просмотреть логи:
```sh
sudo journalctl -u gunicorn --no-pager
sudo journalctl -u nginx --no-pager
```

### Готово к запуску
