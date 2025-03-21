# 1. run project
### 1.1. Create, activate virtual environment
- python -m venv venv
- venv\Scripts\activate

### 1.2. Install all packages of project
- pip install -r requirements.txt

### 1.3. Create and apply migrations
- cd lms_maihoc_be
- python manage.py makemigrations
- python manage.py migrate

### 1.4. Run the development server
- python manage.py runserver

# 2. Addtional

### 2.1. Create a new app
- python manage.py startapp product

### 2.2. Update requirements.txt After installing additional packages
- pip freeze > requirements.txt

### 2.3. Create Django project
- django-admin startproject lms_maihoc_be
- cd lms_maihoc_be

### 2.4. Create superuser (follow the prompts)
- python manage.py createsuperuser