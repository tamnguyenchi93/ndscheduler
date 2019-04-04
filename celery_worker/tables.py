"""Define database schemas."""

import sqlalchemy

import datetime
import pytz

METADATA = sqlalchemy.MetaData()


def get_current_datetime():
    """Retrieves the current datetime.

    :return: A datetime representing the current time.
    :rtype: datetime
    """
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

#
# Jobs
# It's defined by apscheduler library.
#

#
# Executions
#

EXECUTION_STATUS_SCHEDULED = 0
EXECUTION_STATUS_RUNNING = 1
EXECUTION_STATUS_STOPPING = 2
EXECUTION_STATUS_STOPPED = 3
EXECUTION_STATUS_FAILED = 4
EXECUTION_STATUS_PUBLISHED = 5
EXECUTION_STATUS_TIMEOUT = 6
EXECUTION_STATUS_SCHEDULED_ERROR = 7
EXECUTION_STATUS_SUCCEEDED = 8

EXECUTIONS_TABLENAME = 'scheduler_execution'

EXECUTIONS = sqlalchemy.Table(
    EXECUTIONS_TABLENAME, METADATA,
    sqlalchemy.Column('eid', sqlalchemy.Unicode(191, _warn_on_bytestring=False), primary_key=True),
    sqlalchemy.Column('hostname', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('pid', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('state', sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column('scheduled_time', sqlalchemy.DateTime(timezone=True), nullable=False,
                      default=get_current_datetime),
    sqlalchemy.Column('updated_time', sqlalchemy.DateTime(timezone=True),
                      default=get_current_datetime, onupdate=get_current_datetime),
    sqlalchemy.Column('description', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('result', sqlalchemy.Text, nullable=True),
    sqlalchemy.Column('job_id', sqlalchemy.Text, nullable=False),
    sqlalchemy.Column('task_id', sqlalchemy.Text, nullable=True))

