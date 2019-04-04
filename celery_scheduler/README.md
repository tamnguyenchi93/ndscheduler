# Celery Ndscheduler
This is an example of simple Celery scheduler server base on Ndscheduler.
Scheduler node just do a simple action is sent message to Celery worker. Celery worker will perform task then update execution status on db server
So that you must have a stand alone sql server. In this example I use postgres server.

# Run Example:
## Start postgres database:
I use docker version for easy to setup

> $ docker run --name some-postgres -p 32768:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

## Start Celery scheduler server:
```bash
$ chmod +x start_service.sh
$ ./start_service.sh

```

## Start celery worker:
```bash
$ cd ../celery_worker
$ celery worker -A simple_worker --loglevel=INFO -c 1 --queue MyQueue
```