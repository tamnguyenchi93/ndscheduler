import logging
import hashlib
from ndscheduler.core.scheduler.base import SingletonScheduler
from ndscheduler import constants
from ndscheduler import job
from ndscheduler import settings
from ndscheduler import utils


logger = logging.getLogger(__name__)


class CeleryScheduler(SingletonScheduler):
    @classmethod
    def is_okay_to_run(cls, database):
        """Determine if it's okay to schedule jobs.

        Could override this function to dynamically decide whether to run jobs by current process.
        Typically, we try to avoid running multiple scheduler processes that schedule same jobs.

        :param DatastoreBase database: a DatastoreBase instance.
        :return: if it's okay to run jobs, returns True; otherwise, False.
        :rtype: bool
        """
        return True

    @classmethod
    def run_job(cls, job_class_path, job_id, *args, **kwargs):
        execution_id = utils.generate_uuid()
        datastore = utils.get_datastore_instance()
        datastore.add_execution(execution_id, job_id,
                                constants.EXECUTION_STATUS_SCHEDULED,
                                description=job.JobBase.get_scheduled_description())
        try:
            job_class = utils.import_from_path(job_class_path)
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_SCHEDULED,
                                       description=job_class.get_scheduled_description())
            cls.run_scheduler_job(job_class, job_id, execution_id, *args, **kwargs)
        except Exception as e:
            logger.exception(e)
            datastore.update_execution(execution_id,
                                       state=constants.EXECUTION_STATUS_SCHEDULED_ERROR,
                                       description=job.JobBase.get_scheduled_error_description(),
                                       result=job.JobBase.get_scheduled_error_result()
                                       )
            return None
        return execution_id

    @classmethod
    def run_scheduler_job(cls, job_class, job_id, execution_id, *args, **kwargs):
        """Run a job.

        Override this function for your own implementation.

        :param str job_class: String for job class.
        :param str job_id: Job id.
        :param list args: List of args.
        :param dict kwargs: Keyword arguments.
        """
        job_class.run_job(job_id, execution_id, *args, **kwargs)

    def add_scheduler_job(self, job_class_string, name, pub_args=None,
                          month=None, day_of_week=None, day=None, hour=None, minute=None,
                          **kwargs):
        """Add a job. Job infomation will be persistent in postgres.

        This is a NON-BLOCKING operation, as internally, apscheduler calls wakeup()
        that is async.

        :param str job_class_string: String for job class, e.g., myscheduler.jobs.a_job.NiceJob
        :param str name: String for job name, e.g., Check Melissa job.
        :param str pub_args: List for arguments passed to publish method of a task.
        :param str month: String for month cron string, e.g., */10
        :param str day_of_week: String for day of week cron string, e.g., 1-6
        :param str day: String for day cron string, e.g., */1
        :param str hour: String for hour cron string, e.g., */2
        :param str minute: String for minute cron string, e.g., */3
        :param dict kwargs: Other keyword arguments passed to run_job function.
        :return: String of job id, e.g., 6bca19736d374ef2b3df23eb278b512e
        :rtype: str

        Returns:
            String of job id, e.g., 6bca19736d374ef2b3df23eb278b512e
        """
        if not pub_args:
            pub_args = []

        job_id = hashlib.md5(name).hexdigest()

        job = self.get_job(job_id)
        if job is not None:
            logger.warning('Job with name %s exist pls check again' % name)
            return job_id

        arguments = [job_class_string, job_id]
        arguments.extend(pub_args)

        scheduler_class = utils.import_from_path(settings.SCHEDULER_CLASS)
        self.add_job(scheduler_class.run_job,
                     'cron', month=month, day=day, day_of_week=day_of_week, hour=hour,
                     minute=minute, args=arguments, kwargs=kwargs, name=name, id=job_id)
        return job_id
