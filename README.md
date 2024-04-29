### **Для запуска проекта в любом из вариантов нужно:**
1) Cоздать `.env` файл, указав значения:
    - `SECRET_KEY` (секретный ключ проекта)
    - `HOST` (адрес хоста)
    - `POSTGRES_USER` (имя пользователя PostgreSQL)
    - `PASSWORD` (пароль пользователя PostgreSQL)
    - `NAME` (имя базы данных PostgreSQL)
    - `TEST_NAME` (имя базы данных, которая будет использоваться для тестов)

2) Создать базу данных `PostgreSQL` с указанными вами значениями в `.env` файле
### **Для запуска проекта с помощью Docker:**
1) нужно сменить в `.env` файле значение `HOST` на `db`

2) выполнить команду `docker compose run web python manage.py migrate`

3) выполнить команду `docker compose run web python manage.py createsuperuser`

4) выполнить команду `docker compose up`
### **Для запуска проекта без Docker'a:**
1) Выполнить команду `pip install -r requirements.txt`
2) Выполните команду `python manage.py migrate`
3) Выполнить команду `python manage.py runserver`

Чтобы база данных изначально была заполнена данными, вы можете выполнить команду `docker compose run web python manage.py loaddata fixtures/*` если запускаете приложение в Docker или `python manage.py loaddata fixtures/*` если запускаете без Docker'a 

*(так как папка с изображениями у меня в gitignore, у вас не будут отображаться изображения)*
