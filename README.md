# Traffic Light Test Task
## Made by Sergei Shinn
A Django app made as a test task for a Backend-developer vacancy.  


## Link Structure

- **/** - Home, Swagger
- **/redoc** - Redoc API Page
- **/admin** - Admin panel
- **/api** - API part of the App
    - **/clients** - API Clients List
    - **/departments** - API Departments List
    - **/entities** - API Entities List


## Installation
##### *For Linux users*
After pushing this repository and creating your DB on Postgre, you'll need to create new python venv for it and install requirements:

```sh
pipenv install
pipenv shell
cp .env.example .env
```

After that you'll need to migrate the data, create a superuser, fill database (it's gonna take a long time) and run the application:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py fill_db
python manage.py runserver
```
