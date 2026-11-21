# Chapter 06: Defining dependencies between tasks

## What I verified
- **Basic dependencies**: Linear (`>>`) and fan-out / fan-in. fetch_sales and fetch_weather ran in parallel on the CeleryExecutor worker.
- **Branching inside a task** (`02_branch_function`): `data_interval_start` vs `ERP_CHANGE_DATE` picks the old/new function. The chosen path is not visible in the Graph view, only in the task log ("Preprocessing sales data (NEW)").
- **Branching in the DAG** (`03`, `04`): BranchPythonOperator marks the unchosen path as skipped. With the default `all_success`, the skip propagates to join_datasets and below. `trigger_rule="none_failed"` on the join fixes it, or an intermediate join task (`none_failed`) absorbs the skip so downstream tasks can keep `all_success`.
- **Conditional tasks** (`05`-`07`): Compared a check inside deploy_model, raising AirflowSkipException, and LatestOnlyOperator. Only the last two show the task as skipped in the UI.
- **Trigger rules** (`08_trigger_rules_lab`, `99_trigger_rules_lab`): A failure in fetch_sales turns clean_sales, join, train and deploy into upstream_failed, while the weather branch still succeeds. `none_failed` passes skips but not failures. `one_failed` (alert) ran about 6 seconds after the failure without waiting for other tasks. `all_done` (cleanup) runs regardless of results.
- **XCom** (`09`-`11`): Explicit xcom_push / xcom_pull, pulling via a `templates_dict` template, and the automatic `return_value` key.
- **Taskflow API** (`12`-`14`): `@task` return values are passed as XCom and passing them as arguments creates the dependency. Calling `deploy_model` twice created `deploy_model__1`. In the mixed file, `join_datasets >> model_id` makes train_model wait for join_datasets.

## Summary
- **Branching**: inside a task = simple but invisible in the UI / BranchPythonOperator = path visible, needs a join trigger rule / conditional task = skip the rest of the run (e.g. deploy only on the latest run)
- **Trigger rules**: `all_success` = all upstream succeeded (default) / `none_failed` = no failure, skips allowed (join after a branch) / `all_done` = all upstream finished, any result (cleanup after a batch) / `one_failed` = any upstream failed, runs immediately (failure alert)
- **Passing data**: /tmp file = single worker only / DB = large data, durable (ch05) / XCom = small values in the metadata DB / Taskflow = XCom with automatic dependencies, still small serializable values only

## My additions
- `03_branch_dag_old_new_lab.py`, `04_branch_dag_join_lab.py`: copies to compare joins after a branch (all_success vs none_failed vs an intermediate join)
- `08_trigger_rules_lab.py`: forced failure in fetch_sales with `none_failed` on the join, to check that failures still propagate
- `99_trigger_rules_lab.py` (dag_id `lab_trigger_rules_a`): cleanup (`all_done`) and alert (`one_failed`)
- `11_xcoms_return_lab.py`: copy used for the return_value XCom experiment

## Notes
- Book listing typos: 6.7 missing colon after `else`, 6.8 / 6.11 trailing space in `"data_interval_start "`, 6.22 wrapped template string, 6.24 `xcomimport`. The repo files were used as the reference.
- Manual triggers have no data interval, so date-comparing DAGs raised `KeyError: 'data_interval_start'`. Triggering with `--logical-date` fixed it.
- `all_done` only waits for directly connected upstream tasks. Connect every branch end, e.g. `[deploy_model, clean_sales, clean_weather] >> cleanup`.
- A successful final cleanup task can make the whole run look successful, hiding the failure.
