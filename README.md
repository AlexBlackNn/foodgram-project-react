## Проект Foodgram

 
Cайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Авторы проекта: 

**[Чернов Алексей](https://github.com/AlexBlackNn) Backend**.

**[Yandex практикум](https://practicum.yandex.ru/) Frontend**.

### Cписок используемых технологий:
Django 

Django-rest-framework

### Как запустить проект:

Клонировать репозиторий и перейти в папку foodgram-project-react и далее в папку infra

```
cd foodgram-project-react/infra
```


Запустить проект:

```
 docker-compose up --build --force-recreate

```

Создать суперпользователя для входа в админку: 

```
docker-compose exec backend python manage.py createsuperuser

```
Описание документации доступно по адресу:

```
http://localhost/api/docs/
```

Выгрузить данные из БД для сохранения:
```
docker-compose exec backend python manage.py dumpdata > init_database.json
```
Загрузить сохраненные данные для инициализации БД:
```
sudo docker-compose exec backend python manage.py loaddata init_database.json
```