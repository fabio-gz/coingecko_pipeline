import logging
from airflow.models import Variable


task_log = logging.getLogger("airflow.task")

api_key = Variable.get("api_key")