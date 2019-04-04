"""A sample job that prints string."""

from ndscheduler import job
from celery import Celery
from celery_job import CeleryJob

class AwesomeJob(CeleryJob):

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': 'This will print a string in your shell. Check it out!',
            'arguments': [
                # argument1
                {'type': 'string', 'description': 'First argument'},

                # argument2
                {'type': 'string', 'description': 'Second argument'}
            ],
            'example_arguments': '["first argument AAA", "second argument BBB"]'
        }

    def run(self, argument1, argument2, *args, **kwargs):
        app = Celery('simple_worker')
        msg = 'Sent message to celery worker with argument1=\'%s\' and argument2=\'%s\' job_id=%s and execution_id=%s' % \
              (argument1, argument2, self.job_id, self.execution_id)
        print(msg)
        task_name = "simple_worker.MyTask"
        queue_name = 'MyQueue'
        # task_id = "crawler_%s_%s" % (argument1, argument2)
        app.send_task(task_name, args=[argument1, argument2], queue=queue_name, task_id=self.execution_id)
        app.close()
        return msg

if __name__ == "__main__":
    # You can easily test this job here
    job = AwesomeJob.create_test_instance()
    job.run(123, 456)
