**NOTE**: Make sure your rabbitmq server is running
Start simple celery worker:  
> $ celery worker -A simple_worker --loglevel=INFO -c 1 --queue MyQueue