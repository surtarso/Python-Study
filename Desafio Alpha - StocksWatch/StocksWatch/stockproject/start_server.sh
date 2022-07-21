

#start celery workers
celery -A stockproject.celery worker --pool=solo -l info

#delete celery tasks from redis
redis-cli KEYS "celery*" | xargs redis-cli DEL

#start celery beat
celery -A stockproject beat -l INFO

#start server 
python3 manage.py runserver 0:8000
