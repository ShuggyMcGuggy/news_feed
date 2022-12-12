web: gunicorn content_aggregator.wsgi --log-file -
release: python manage.py migrate
clock: python manage.py startjobs
