"""Run the scheduler process."""

from ndscheduler.server import server
import logging

class CeleryServer(server.SchedulerServer):

    def post_scheduler_start(self):
        # New user experience! Make sure we have at least 1 job to demo!
        jobs = self.scheduler_manager.get_jobs()
        if len(jobs) == 0:
            self.scheduler_manager.add_job(
                job_class_string='jobs.sample_job.AwesomeJob',
                name='My Awesome Job',
                pub_args=['first parameter', {'second parameter': 'can be a dict'}],
                minute='0')


if __name__ == "__main__":
    # root_logger = logging.getLogger()
    # current_handler = root_logger.handlers
    # for handler in current_handler:
    #     root_logger.removeHandler(handler)
    # root_logger.setLevel(logging.DEBUG)
    # # logging.basicConfig(format='[%(asctime)s: %(levelname)s %(name)s] [%(funcName)s %(lineno)d] %(message)s')
    # fmt = logging.Formatter(fmt='[%(asctime)s: %(levelname)s %(name)s] [%(funcName)s %(lineno)d] %(message)s')
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(fmt)
    #
    # root_logger.addHandler(ch)

    CeleryServer.run()
