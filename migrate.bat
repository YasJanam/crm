@echo off
echo Applying migrations...
python manage.py makemigrations accounts
python manage.py makemigrations company
python manage.py makemigrations sale
python manage.py makemigrations activities
python manage.py migrate