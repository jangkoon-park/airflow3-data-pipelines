import time

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator


def _fail():
    raise RuntimeError("의도적 실패: fetch_sales")


def _slow():
    time.sleep(30)


def _print(msg):
    print(msg)


with DAG(
    dag_id="lab_trigger_rules_a",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["lab", "chapter06"],
):
    start = EmptyOperator(task_id="start")
    fetch_sales = PythonOperator(task_id="fetch_sales", python_callable=_fail)
    clean_sales = EmptyOperator(task_id="clean_sales")
    fetch_weather = PythonOperator(task_id="fetch_weather", python_callable=_slow)
    clean_weather = PythonOperator(task_id="clean_weather", python_callable=_slow)
    join_datasets = EmptyOperator(task_id="join_datasets")
    train_model = EmptyOperator(task_id="train_model")
    deploy_model = EmptyOperator(task_id="deploy_model")
    cleanup = PythonOperator(
        task_id="cleanup", python_callable=_print,
        op_args=["cleanup 실행"], trigger_rule="all_done",
    )
    alert = PythonOperator(
        task_id="alert", python_callable=_print,
        op_args=["alert 실행"], trigger_rule="one_failed",
    )

    start >> [fetch_sales, fetch_weather]
    fetch_sales >> clean_sales
    fetch_weather >> clean_weather
    [clean_sales, clean_weather] >> join_datasets >> train_model >> deploy_model
    [deploy_model, clean_sales, clean_weather] >> cleanup
    [fetch_sales, fetch_weather] >> alert
