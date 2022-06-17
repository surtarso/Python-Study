#!/bin/bash

#start celery workers
celery -A stockproject.celery worker --pool=solo -l info &
#start celery beat
celery -A stockproject beat -l INFO &
#start server
python3 manage.py runserver
