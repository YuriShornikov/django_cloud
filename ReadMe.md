3. Проект работает на рег.ру. Для просмотра перейдите по адресу: `http://79.174.92.124/` Для развертывания проекта необходимо:
3.1 В мои ресурсы/виртуальные машины добавить ubuntu на минималках с ssh ключом.
3.2 В PowerShell прописать ssh root@[79.174.92.124](http://79.174.92.124) - ip вашего сервера ввести пароль
3.3 adduser aukor - создание пользователя
3.4 usermod aukor -aG sudo - дать права
3.5 su aukor - зайти под пользователем aukor
3.6 cd ~ - выход в директорию
3.7 sudo apt update - провести обновление
3.8 sudo apt install python3-venv python3-pip postgresql nginx - провести установку
3.9 git clone https://github.com/YuriShornikov/django_cloud.git - провести клонирование репа
Для того, чтобы все работало, вам необходимо поменять ip в нескольких файлах и выполнить build для фронта:
В папке backend в .env: DOMAIN=79.174.92.124:8000 (прописать свой ip), в settings.py: CSRF_TRUSTED_ORIGINS = ["http://79.174.92.124"], ALLOWED_HOSTS = ['localhost', '127.0.0.1', '79.174.80.81']. В папке frontend в файле .env.production: VITE_API_BASE_URL=http://79.174.92.124:8000/    После этого выполнить npm run build для папки frontend. И после этого можно заливать на сервер.
3.10 cd django_cloud - перейти в папку с распакованными файлами
3.11 sudo su postgres - зайти в бд
3.12 psql
3.13 ALTER USER postgres WITH PASSWORD 'admin1234'; - создаем пользователя с паролем
3.14 CREATE DATABASE cloud; - создаем бд
3.15 \q - выходим из бд
3.16 cd backend - переходим в папку
3.17 python3 -m venv env
3.18 source env/bin/activate - активация
3.19 pip install -r requirements.txt - установка библиотек
3.20 python manage.py migrate - приминение миграции
3.21 sudo nano /etc/systemd/system/gunicorn.service - прописываем значения
```
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=aukor
Group=www-data
WorkingDirectory=/home/aukor/django_cloud/backend
ExecStartPre=/home/aukor/django_cloud/backend/env/bin/python /home/aukor/django_cloud/backend/manage.py update_site
ExecStart=/home/aukor/django_cloud/backend/env/bin/gunicorn --access-logfile - --workers=3 --bind unix:/home/aukor/django_cloud/backend/mycloud/project.sock mycloud.wsgi:application

[Install]
WantedBy=multi-user.target
```
3.22 sudo systemctl start gunicorn
3.23 sudo systemctl enable gunicorn
3.24 sudo nano /etc/nginx/sites-available/my_project - прописываем
```
server {
        listen 80;
        server_name 79.174.92.124;

        client_max_body_size 100M;

        # Обслуживание React-приложения
        location / {
            root /home/aukor/django_cloud/frontend/dist;
            index index.html;
            try_files $uri /index.html;
        }

        # Статические файлы фронтенда (например, ассеты)
        location /assets/ {
            root /home/aukor/django_cloud/frontend/dist;
            try_files $uri =404;
        }
    }

server {
        listen 8000;
        server_name 79.174.92.124;

        client_max_body_size 100M;

        # Проксирование всех запросов к бэкенду
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/aukor/django_cloud/backend/mycloud/project.sock;
        }

        # Обслуживание медиа-файлов Django
        location /media/ {
            alias /home/aukor/django_cloud/backend/media/;
            autoindex on;
        }

        # Обслуживание статических файлов Django
        location /static/ {
            alias /home/aukor/django_cloud/backend/static/;
        }
}
```
3.25 sudo ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enabled/
3.26 ls -l /etc/nginx/sites-enabled/ - проверка создания
3.27 sudo systemctl start nginx
3.28 sudo ufw allow 'Nginx Full'
3.29 python manage.py collectstatic
3.30 sudo chmod 755 /home /home/aukor /home/aukor/django_cloud - при необходимости даем доступа всем папкам, если проект не открывается
3.31 mkdir -p /home/aukor/django_cloud/backend/media - создаем папку, вероятно она отсутствует в репе
3.32 sudo systemctl restart nginx
3.33 sudo systemctl restart gunicorn

4. Проект должен работать, либо необходимо просмотреть логи с ошибками и скорректировать.
        