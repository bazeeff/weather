# Communication Manager

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
8. **https://<ip-хоста>/admin/** - доступ к админ.панели
9. **https://<ip-хоста>/api/v1/swagger/** - доступ к апи




