# test-task-python
- docker-compose build
- docker-compose up
# at another tab at terminal
- docker-compose run web python /code/manage.py migrate
- docker-compose run web python /code/manage.py createsuperuser
