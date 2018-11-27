import datetime
import os

from airflow import models
from airflow.contrib.operators import dataproc_operator
from airflow.utils import trigger_rule



yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': 'data-academy-2018'
}

# [START composer_quickstart_schedule]
with models.DAG(
        'composer_csv2parquetv4',
        # Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    # [END composer_quickstart_schedule]

    # Create a Cloud Dataproc cluster.
    create_dataproc_cluster = dataproc_operator.DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        # Give the cluster a unique name by appending the date scheduled.
        # See https://airflow.apache.org/code.html#default-variables
        cluster_name='parquetconverter2',
        num_workers=3,
        zone='europe-west1-b',
        master_machine_type='n1-standard-1',
        worker_machine_type='n1-standard-1')

    # Run the pyspark CSV2PARQUET example
    run_dataproc_csv2parquet = dataproc_operator.DataProcPySparkOperator(
        task_id='run_dataproc_parquetconvert',
        cluster_name='parquetconverter2',
        main='gs://alex-code/convert.py')

    # Delete Cloud Dataproc cluster.
    delete_dataproc_cluster = dataproc_operator.DataprocClusterDeleteOperator(
        task_id='delete_dataproc_cluster',
        cluster_name='parquetconverter2',
        # Setting trigger_rule to ALL_DONE causes the cluster to be deleted
        # even if the Dataproc job fails.
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE)

    # [START composer_quickstart_steps]
    # Define DAG dependencies.
    create_dataproc_cluster >> run_dataproc_csv2parquet >> delete_dataproc_cluster
    # [END composer_quickstart_steps]

# [END composer_quickstart]
