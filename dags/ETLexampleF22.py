"""
Example Airflow DAG to submit Apache Druid json index file
"""
from datetime import datetime

from airflow.models import DAG
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from pathlib import Path
from airflow.providers.apache.druid.operators.druid import DruidOperator
from airflow.providers.apache.druid.hooks.druid import DruidHook
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from textwrap import dedent
from airflow.operators.python import PythonOperator

#these are additional packages imported for the load_druid function
import os
from airflow.hooks.base_hook import BaseHook
import json
import requests


extract_query = 'Select * from shows'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='tutorial_etl_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = __doc__



    # [END transform_function]
    def extract(**kwargs):
        task_instance = kwargs['ti']

        #commented for example
    # [END transform_function]

   
   
    # [START transform_function]
    def transform(**kwargs):
        task_instance = kwargs['ti']
        #commented for example
    # [END transform_function]

    def load_druid(**kwargs):
        task_instance = kwargs['ti']

        # get the connection
        CONN_ID = kwargs.get('druid_ingest_conn_id','druid_ingest_default')
        print(CONN_ID)
       
     
        conn = BaseHook.get_connection(CONN_ID)
        host = conn.host
        port = conn.port
        conn_type = 'http' #if not conn.conn_type else conn.conn_type
        endpoint = conn.extra_dejson.get('endpoint', 'druid/indexer/v1/task')
       
        conn_url = "{conn_type}://{host}:{port}/{endpoint}".format(
            conn_type=conn_type, host=host, port=port, endpoint=endpoint)

        print(conn_url)
        # get the druid ingestion spec file
        json_index_file = kwargs.get('json_index_file','ingest.json')
       
        base_folder = os.getenv('AIRFLOW__CORE__DAGS_FOLDER', '/opt/airflow/dags')

        fname = os.path.join(base_folder, json_index_file)
        #load the the druid file and convert to json string
        with open(fname, 'r') as f:
            druid_spec = json.load(f)

       
        print(json_index_file)
        # send the ingestion spec to druid
        data = json.dumps(druid_spec)
        print(data)
        # data = json_index_file
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=conn_url, data=data, headers=headers)
       
        if response.status_code == 200:
            print(response._content)
        else:
            # throw exception if any other response from druid
            print(response.status_code)
            raise
    # [END transform_function]





    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        op_kwargs = {
            "sql": extract_query,
            "postgres_conn_id":"pgoltp",
            "pandas_sql_params": None,
            "csv_path": '/tmp/filesystem/extract.csv',
            "csv_sep":","
        }
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    The data is getting loaded from PostgreSQL and saved to a file.
    The file name is pushed (using xcom) so it can be used by the next task
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        op_kwargs = {
            "csv_path": '/tmp/filesystem/transform.csv',
            "csv_sep":","
        }
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which using xcom_pull for the file name of the extracted data,
    performs and transformation, and outputs the transformed data
    This value is used in the next stage for loading data into druid
    """
    )


    # This is a python operator with code that will show you more debugging information
    # replace the druid operator task with this to help debug your settings and json  
    # [START load_task]
    load_task = PythonOperator(
        task_id='load',
        python_callable=load_druid,
        op_kwargs = {
            "druid_ingest_conn_id":"druid_ingest_default",
            "json_index_file":"druid-spec.json",
            "csv_path": '/tmp/filesystem/tranformed.csv',
            "csv_sep":","
        }
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple load task for ingestion into druid
    """
    )



    # load_task
    extract_task >> transform_task >> load_task
