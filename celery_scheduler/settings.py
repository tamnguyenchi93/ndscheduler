"""Settings to override default settings."""
import logging
#
# Override settings
#
DEBUG = True

HTTP_PORT = 8989
HTTP_ADDRESS = '0.0.0.0'

# Postgres
DATABASE_CLASS = 'ndscheduler.core.datastore.providers.postgresql.DatastorePostgresql'
DATABASE_CONFIG_DICT = {
    'user': 'postgres',
    'password': 'mysecretpassword',
    'hostname': 'localhost',
    'port': 32768,
    'database': 'scheduler',
    'sslmode': 'disable'
}

# Set logging level
#
logging.getLogger().setLevel(logging.DEBUG)

JOB_CLASS_PACKAGES = ['jobs']
SCHEDULER_CLASS = 'sched.scheduler.CeleryScheduler'

