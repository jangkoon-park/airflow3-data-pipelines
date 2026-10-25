# Airflow 3 Data Pipelines

Hands-on Apache Airflow 3 pipelines on AWS EC2 (Ubuntu) with Docker Compose, following *Data Pipelines with Apache Airflow* (2nd ed.).

## Chapters
| Chapter | Topic | What I did |
|---|---|---|
| 02 | Anatomy of an Airflow DAG | Rocket-launch DAG, explicit vs context-manager DAG, catchup scheduling, failure & partial re-run (Clear), DAG versioning (v1→v2) |

## Environment
- AWS EC2 (Ubuntu), Docker Compose
- Apache Airflow 3.1 (CeleryExecutor: scheduler, dag-processor, api-server, worker, triggerer, Postgres, Redis)
