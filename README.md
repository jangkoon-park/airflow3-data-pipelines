# Airflow 3 Data Pipelines

Hands-on Apache Airflow 3 pipelines on AWS EC2 (Ubuntu) with Docker Compose, following *Data Pipelines with Apache Airflow* (2nd ed.).

## Chapters
| Chapter | Topic | What I did |
|---|---|---|
| 02 | Anatomy of an Airflow DAG | Rocket-launch DAG, explicit vs context-manager DAG, catchup scheduling, failure & partial re-run (Clear), DAG versioning (v1→v2) |
| 03 | Time-based scheduling | Trigger vs data-interval timetables (cron, Delta), catchup default (False) in Airflow 3, simulated failure to compare non-atomic vs atomic tasks, idempotent re-run via Clear |
| 04 | Asset-aware scheduling | Producer/consumer DAGs linked by asset URI, passing the data date via event extra (Metadata), skip updates with AirflowSkipException, multi-asset (AND) consumer, custom AssetOrTimeSchedule DAG comparing time-based vs asset-triggered runs |
| 05 | Templating tasks using the Airflow context | Jinja templating in BashOperator / PythonOperator verified via Rendered Template (UI) and `airflow tasks render` (CLI), Wikimedia pageview pipeline (download → extract → INSERT into Postgres), worker-local /tmp limitation, idempotent re-run with UNIQUE + ON CONFLICT DO NOTHING (5 rows, 0 duplicates) |

## Environment
- AWS EC2 (Ubuntu), Docker Compose
- Apache Airflow 3.1 (CeleryExecutor: scheduler, dag-processor, api-server, worker, triggerer, Postgres, Redis)
