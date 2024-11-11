from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from include.global_variables.vars import default_args
from gecko_data_dag import dataset

DBT_PROJECT_DIR = 'dbt_project'

@dag(
    dag_id = 'coingecko_transformations_data',
    default_args = default_args,
    schedule=dataset
)
def transformation_data():
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt build',
        env = {
            'DBT_PROFILES_DIR': DBT_PROJECT_DIR
        }
    )

transformation_data()

    

