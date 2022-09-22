# praktikum_new_diplom

пока запускаемся так:

ФРОНТ 

cd frontend
npm run start 

Бэк 

python manage.py runserver

docker build -t backend .
docker run -p 8000:8000 backend .

docker-compose up --build --force-recreate

docker exec -it 56155920acbd bash

sudo service apache2 stop
