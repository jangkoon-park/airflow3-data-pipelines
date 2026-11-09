# Chapter 05: Templating tasks using the Airflow context

## What I verified
- **Template rendering**: Jinja templates are rendered to real values before the task runs. Checked in the Rendered Template view (UI) and with `airflow tasks render` (CLI). BashOperator renders into `bash_command`; PythonOperator passes the context or rendered `op_args` / `op_kwargs` to the Python callable.
- **Passing data via /tmp**: Works on a single worker, but each worker has its own local `/tmp`. A downstream task running on another worker may not find the file.
- **Idempotency**: Loaded 5 pageview rows into Postgres (`wiki_results`). With a UNIQUE (pagename, datetime) constraint and `ON CONFLICT DO NOTHING`, re-running `write_to_postgres` via Clear kept 5 rows with 0 duplicates.

## My additions
- `04b_print_trigger_interval.py`: CronTriggerTimetable version, to compare with CronDataIntervalTimetable
- `05b_test_op_args_kwargs.py`: test of `op_args` / `op_kwargs` templating
- `05_retrieve_data.py`: added a User-Agent header for Wikimedia requests

## Notes
- Some book listings have typos (5.3 `*_`, 5.13 extra parenthesis, 5.20 `return_last`). The repo files were used as the reference.
- Inside Docker, the Postgres host is the service name `wiki_results`, not `localhost`.
