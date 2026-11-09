import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def _show_args(dataset, delay_hours, source, retry):
    print(f"dataset: {dataset}")
    print(f"delay_hours: {delay_hours}")
    print(f"source: {source}")
    print(f"retry: {retry}")


with DAG(
    dag_id="05b_test_op_args_kwargs",
    start_date=pendulum.datetime(2026, 11, 1, tz="UTC"),
    schedule=None,
):
    test_task = PythonOperator(
        task_id="show_args",
        python_callable=_show_args,
        op_args=["pageviews", 3],
        op_kwargs={
            "source": "wikipedia",
            "retry": True,
        },
    )
