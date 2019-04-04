from celery import Celery
import sqlalchemy
import os
import json
from celery import Task
import tables
app = Celery('MyApp')


DATABASE_CONFIG_DICT = {
    'user': 'postgres',
    'password': 'mysecretpassword',
    'hostname': 'localhost',
    'port': 32768,
    'database': 'scheduler',
    'sslmode': 'disable'
}


class CeleryTask(Task):
    db_url = 'postgresql://%s:%s@%s:%d/%s?sslmode=%s' % (
        DATABASE_CONFIG_DICT['user'],
        DATABASE_CONFIG_DICT['password'],
        DATABASE_CONFIG_DICT['hostname'],
        DATABASE_CONFIG_DICT['port'],
        DATABASE_CONFIG_DICT['database'],
        DATABASE_CONFIG_DICT['sslmode'])
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = sqlalchemy.create_engine(self.db_url)
        return self._db

    def on_success(self, retval, task_id, args, kwargs):
        # print "on_success of add. Do special add things here. Task: {0}  sender: {1}".format(task_id, retval)

        update_data = {
            'result': retval,
            'state': tables.EXECUTION_STATUS_SUCCEEDED,
        }
        execution_update = tables.EXECUTIONS.update().where(
            tables.EXECUTIONS.c.eid == task_id).values(update_data)
        self.db.execute(execution_update)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print "on_failure of add. Do special add things here. Task: {0}  sender: {1}".format(task_id, einfo)

        update_data = {
            'result': einfo.traceback,
            'state': tables.EXECUTION_STATUS_FAILED,
        }
        execution_update = tables.EXECUTIONS.update().where(
            tables.EXECUTIONS.c.eid == task_id).values(update_data)
        self.db.execute(execution_update)

@app.task(base=CeleryTask)
def MyTask(arg1, arg2):
    print('%s, %s' % (arg1, arg2))
    return 'Received message to celery worker with argument1=\'%s\' and argument2=\'%s\'' % (arg1, arg2)