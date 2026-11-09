from urllib import request
import shutil

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.trigger import CronTriggerTimetable

HOURS_AGO = 3  # 위키미디어 파일이 올라오기까지 걸리는 시간을 감안한 지연


def _get_data(logical_date, **_):
    target = logical_date.subtract(hours=HOURS_AGO)

    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{target.year}/{target.year}-{target.month:0>2}/"
        f"pageviews-{target.year}{target.month:0>2}{target.day:0>2}-{target.hour:0>2}0000.gz"
    )
    output_path = f"/tmp/wikipageviews-{target.format('YYYYMMDDHH')}.gz"

    req = request.Request(
        url,
        headers={
            "User-Agent": "AirflowPageviewsTraining/1.0 (https://github.com/jangkoon-park)"
        },
    )

    print(f"Downloading {url} -> {output_path}")
    with request.urlopen(req) as response:
        with open(output_path, "wb") as output_file:
            shutil.copyfileobj(response, output_file)


with DAG(
    dag_id="05_retrieve_data",
    start_date=pendulum.today("UTC").add(hours=-3),
    schedule=CronTriggerTimetable("@hourly", timezone="UTC"),
    max_active_runs=1,
    catchup=True,
):
    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data,
    )
