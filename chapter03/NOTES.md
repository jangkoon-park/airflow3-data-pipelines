# Chapter 03: Time-based scheduling

## What I verified
- In Airflow 3, `catchup` defaults to `False`. Past runs between `start_date` and `end_date` were scheduled only after setting `catchup=True` explicitly.
- Trigger-based timetables run at the scheduled point in time. Data-interval timetables run after the interval ends and provide `data_interval_start` / `data_interval_end`.
- Atomicity: in `08_non_atomic_send`, the task failed but the stats CSV was already written. In `09_atomic_send`, only `send_stats` failed while `calculate_stats` succeeded. Idempotency: clearing `fetch_events` rewrote the same date partition without changing the result.

## Changes from the book repository
- `06_interval_delta.py`: switched from `CronDataIntervalTimetable("@daily")` to `DeltaDataIntervalTimetable(pendulum.duration(days=1))` to match the frequency-based interval example (section 3.4.3). The book text calls it `DeltaIntervalTimetable`, but the actual class is `DeltaDataIntervalTimetable`.
- `08_non_atomic_send.py`, `09_atomic_send.py`: added `raise RuntimeError("Simulated email failure")`. The original email function only prints, so without this line both DAGs succeed and the atomicity difference is not visible.
