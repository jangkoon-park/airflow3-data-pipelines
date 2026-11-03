# Chapter 04: Asset-aware scheduling

Environment: EC2 (Ubuntu), Docker Compose, Airflow 3.1.2 (checked with `airflow version`)

## What I verified
- A producer task with `outlets=[asset]` creates an asset event only when it succeeds. A consumer that schedules on the same URI then runs automatically. The URI is only an ID; Airflow does not watch the file path.
- Asset-triggered runs have no `logical_date` or `data_interval` (all None in my run). The producer sends the data date with `Metadata(asset, extra={"date": ...})`, and the consumer reads it with `(triggering_asset_events.values() | first | first).extra.date`. `source_dag_run.logical_date` raised an error on 3.1.2.
- If the output file already exists, `AirflowSkipException` marks the task as skipped. No event is created, so the consumer does not run. This is different from idempotent overwriting, where the task succeeds and creates an event.
- With two assets in `schedule`, the consumer waits for both (AND). AND does not guarantee both events have the same data date; producer metadata or consumer checks must enforce that.
- `AssetOrTimeSchedule` runs on cron OR on an asset event. Time-based runs have `logical_date` and `data_interval`; asset-triggered runs do not. So the task needs two ways to get the date.

## My own file
- `dags/05_asset_or_time_schedule.py`: the book repo has no example for section 4.8, so I wrote one. It reuses `file:///data/events_04_1`, with the cron shortened to every 3 minutes (UTC). The `inspect_trigger` task logs run_id, logical_date, the data interval, and the triggering events.
