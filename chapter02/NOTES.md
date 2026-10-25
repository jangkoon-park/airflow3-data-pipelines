# Chapter 02 Notes

- Clear vs Trigger: Clear re-runs the same run (same logical date); Trigger creates a new run.
- Clear resets task state only. Logs and output files (e.g. /tmp/launches.json) remain.
- Re-running only the failed task is safe only if upstream output is valid for that run and tasks are idempotent.
- Output in worker container /tmp can be lost on restart or when another worker picks the task.
- dag=dag is optional when a task is linked (>>) to a task already in a DAG.
- DAG versioning: new runs use latest code; past runs keep their v1 record. With the local bundle, clearing a past run executes the current code.
