# 6장: 태스크 간 의존성 정의

## 직접 확인한 것
- **기본 의존성**: 선형(`>>`)과 fan-out / fan-in. fetch_sales와 fetch_weather가 CeleryExecutor 워커에서 병렬로 실행됨.
- **태스크 안 분기** (`02_branch_function`): `data_interval_start`와 `ERP_CHANGE_DATE`를 비교해 old/new 함수를 고름. 어느 경로로 갔는지 Graph 화면에는 안 보이고 태스크 로그("Preprocessing sales data (NEW)")에서만 확인됨.
- **DAG 안 분기** (`03`, `04`): BranchPythonOperator는 선택 안 된 경로를 skipped로 만듦. 기본 `all_success`면 skip이 join_datasets 이하로 전파됨. join에 `trigger_rule="none_failed"`를 걸면 해결되고, 중간 join 태스크(`none_failed`)를 두면 skip을 흡수해서 아래 태스크는 `all_success`를 그대로 둘 수 있음.
- **조건부 태스크** (`05`-`07`): deploy_model 안에서 검사하기, AirflowSkipException 던지기, LatestOnlyOperator를 비교함. UI에서 skipped로 보이는 건 뒤의 두 방식뿐.
- **트리거 룰** (`08_trigger_rules_lab`, `99_trigger_rules_lab`): fetch_sales가 실패하면 clean_sales, join, train, deploy가 upstream_failed가 되고 날씨 쪽은 그대로 성공함. `none_failed`는 skip은 통과시키지만 실패는 통과시키지 않음. `one_failed`(alert)는 다른 태스크를 기다리지 않고 실패 약 6초 뒤 바로 실행됨. `all_done`(cleanup)은 결과와 상관없이 실행됨.
- **XCom** (`09`-`11`): xcom_push / xcom_pull 명시, `templates_dict` 템플릿으로 가져오기, 자동 `return_value` 키.
- **Taskflow API** (`12`-`14`): `@task` 반환값은 XCom으로 넘어가고, 그 값을 인자로 넘기면 의존성이 생김. `deploy_model`을 두 번 호출하니 `deploy_model__1`이 생김. 섞은 파일에서 `join_datasets >> model_id`는 train_model이 join_datasets를 기다리게 만듦.

## 요약
- **분기**: 태스크 안 = 간단하지만 UI에 안 보임 / BranchPythonOperator = 경로가 보이지만 join에 트리거 룰 필요 / 조건부 태스크 = 그 run의 나머지를 건너뜀(예: 최신 run에서만 배포)
- **트리거 룰**: `all_success` = 앞이 전부 성공(기본값) / `none_failed` = 실패만 없으면 실행, skip 허용(분기 후 합치기) / `all_done` = 결과 상관없이 앞이 다 끝나면 실행(배치 후 정리) / `one_failed` = 하나라도 실패하면 바로 실행(실패 알림)
- **데이터 전달**: /tmp 파일 = 워커 하나일 때만 / DB = 큰 데이터, 오래 보관(5장) / XCom = 메타DB에 작은 값 / Taskflow = 의존성이 자동으로 생기는 XCom, 여전히 작고 직렬화 가능한 값만

## 내가 추가한 것
- `03_branch_dag_old_new_lab.py`, `04_branch_dag_join_lab.py`: 분기 후 join 방식 비교용 복사본(all_success vs none_failed vs 중간 join)
- `08_trigger_rules_lab.py`: fetch_sales를 일부러 실패시키고 join에 `none_failed`를 걸어, 실패가 여전히 전파되는지 확인
- `99_trigger_rules_lab.py` (dag_id `lab_trigger_rules_a`): cleanup(`all_done`)과 alert(`one_failed`)
- `11_xcoms_return_lab.py`: return_value XCom 실험용 복사본

## 참고
- 책 리스팅 오타: 6.7 `else` 뒤 콜론 누락, 6.8 / 6.11 `"data_interval_start "` 키 끝 공백, 6.22 템플릿 문자열 줄바꿈, 6.24 `xcomimport`. 저장소 파일을 기준으로 함.
- 수동 트리거는 data interval이 없어서, 날짜를 비교하는 DAG에서 `KeyError: 'data_interval_start'`가 남. `--logical-date`를 주고 트리거해서 해결.
- `all_done`은 직접 연결된 앞 태스크만 기다림. 갈래 끝을 전부 연결해야 함. 예: `[deploy_model, clean_sales, clean_weather] >> cleanup`
- 마지막 cleanup이 성공하면 run 전체가 성공으로 보여서 실패를 놓칠 수 있음.
