import logging
from airflow.models import Variable
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'fabio',
    'depends_on_past': False,
    'retries': 2,
    'start_date': days_ago(1)
}


task_log = logging.getLogger("airflow.task")

api_key = Variable.get("api_key")