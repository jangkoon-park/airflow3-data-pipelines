import pendulum

from airflow.sdk import DAG, Asset
from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.assets import AssetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable


# 기존 Producer가 생성하는 Asset
events_asset = Asset("file:///data/events_04_1")


def inspect_trigger(**context):
    print("========== DAG Run Information ==========")

    print("Run ID:", context.get("run_id"))
    print("Logical Date:", context.get("logical_date"))
    print("Data Interval Start:", context.get("data_interval_start"))
    print("Data Interval End:", context.get("data_interval_end"))

    asset_events = context.get("triggering_asset_events", {})

    print("========== Asset Events ==========")

    for asset, events in asset_events.items():
        print("Asset URI:", asset.uri)
        print("Event Count:", len(events))

        for event in events:
            print("Event:", event)

    if not asset_events:
        print("No triggering asset events (time-based run)")


with DAG(
    dag_id="05_asset_or_time_schedule",
    schedule=AssetOrTimeSchedule(
        timetable=CronTriggerTimetable(
            "*/3 * * * *",
            timezone="UTC",
        ),
        assets=events_asset,
    ),
    start_date=pendulum.datetime(2026, 11, 3, 0, 0, tz="UTC"),
    catchup=False,
    tags=["chapter04"],
):
    inspect_task = PythonOperator(
        task_id="inspect_trigger",
        python_callable=inspect_trigger,
    )
