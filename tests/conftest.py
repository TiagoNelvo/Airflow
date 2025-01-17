

pytest_plugins = ["helpers_namespace"]

@pytest.helpers.register
def run_task(task,dag):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
       #end_date=dag.default_arg["end_date"],        
    )

@pytest.fixture
def test_dag():
    return DAG(
        dag_id="test_dag",
        start_date={"owner":"airflow","start_date" :datetime(2020,1,1)},
        schedule_interval=None
    )








