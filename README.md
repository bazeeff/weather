# WEATHER

### Инструкция по запуску проекта
1. Клонируем проект
```bash
git clone https://github.com/bazeeff/weather
```
2. Переходим в weather
```bash
cd weather
```
3. Запускаем контейнеры
```bash
docker-compose up --build -d
```
5. Переходим в контейнер web
```bash
docker-compose exec web bash
```
6. Применяем миграции
```bash
python manage.py migrate
```
7. Заполняем файлы static для админки и отображения swagger
```bash
python manage.py collectstatic
```
8. Создаем пользователя для админки и отображения swagger
```bash
python manage.py createsuperuser
```

10. **https://<ip-хоста>/admin - доступ к админ.панели

11. **https://<ip-хоста>/api/v1/swagger - доступ к апи


<img width="882" alt="Снимок экрана 2024-11-06 в 16 12 32" src="https://github.com/user-attachments/assets/48921a1a-c21f-416b-bcf6-4ec4b227037b">

Пример запроса выше вернет погоду в городе Москва


/api/v1/requests_history/ - история запросов к апи погоды
/api/v1/city/ - список городов

телеграмм бот общается с апи из собственного контейнера

ссылка на тг бот: https://t.me/weather_russian_cities_bot






