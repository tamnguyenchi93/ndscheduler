import json
import logging
import os
import socket

from ndscheduler.job import JobBase
from ndscheduler.core import scheduler_manager
from ndscheduler import constants
from ndscheduler import utils

logger = logging.getLogger(__name__)


class CeleryJob(JobBase):
    @classmethod
    def run_job(cls, job_id, execution_id, *args, **kwargs):
        """Wrapper to run this job.

        It updates the execution state, i.e., running, succeeded or failed.

        :param str job_id: Job id.
        :param str execution_id: Execution id.
        :param args:
        :param kwargs:
        """
        scheduler = scheduler_manager.SchedulerManager.get_instance()
        datastore = scheduler.get_datastore()
        try:
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_RUNNING,
                                       hostname=socket.gethostname(), pid=os.getpid(),
                                       description=cls.get_running_description())
            job = cls(job_id, execution_id)
            result = job.run(*args, **kwargs)
            result_json = json.dumps(result, indent=4, sort_keys=True)
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_PUBLISHED,
                                       description=cls.get_succeeded_description(result),
                                       result=result_json)
        except Exception as e:
            logger.exception(e)
            datastore.update_execution(execution_id,
                                       state=constants.EXECUTION_STATUS_FAILED,
                                       description=cls.get_failed_description(),
                                       result=cls.get_failed_result())