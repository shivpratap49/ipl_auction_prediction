from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


dag_args={
    "owner":"shiv",
    "retries": 2,
    "retry_delay":timedelta(minutes=2)
}
with DAG(
    dag_id="setellite_data_dag",
    schedule="@daily",
    start_date=datetime(2025,2,7),
    catchup=True,
    default_args=dag_args
) as dag :
    spark_task = SparkSubmitOperator(
        task_id='run_spark_job',
        application='/home/shiv/Desktop/Big_data_project/setelite_big_data_project/cassandra_to_hive.py',
        conn_id='spark_default',
        verbose=False,
        conf={"spark.jars.packages": "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0"},
        dag=dag,
    )
    truncate_table_task = BashOperator(
        task_id='truncate_table',
        bash_command='cqlsh -e "TRUNCATE satellite_db.satellite_data;"',
        dag=dag,
    )

spark_task>>truncate_table_task