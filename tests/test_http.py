import pytest 


def test_http_operator(test_dag,mocker):
    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(scheama="https",host="api.sunrise-sunset.org")
    )

def _check_light(sunset_sunrise_response):
    results = sunset_sunrise_response.json()["results"]
    sunrise = datetime.strptime(results["sunrise"][:-6], "%Y-%m-%dT%H:%M:%S")
    sunset = datetime.strptime(results["sunset"][:-6], "%Y-%m-%dT%H:%M:%S")
    
    if sunrise < datetime.utcnow() < sunset:
        return False
    else:
        return True
    
is_light = SimpleHttpOpreator(
    task_id="is_light",
    http_conn_id="descomplica"
    endpoint="json",
    method="GET",
    data={"lat": "52.370216","lng":"4,895168","formatted":"0"},
    response_check=_check_light()
    dag=test_dag
)

pytest.helpers.run_task(task=is_light, dag=test_dag)

def test_postgresql(test_dag, mocker, postgres_credentials):
    mocker.patch.object(
        PostgresHook,
        "get_connection",
        return_value=Connection(
            host="localhost",
            conn_type="postgres",
            login=postgres_credentials.username,
            password=postgres_credentials.password
        )
    )

task = PostgresOperator(
    task_id="postgres_task",
    postgres_conn_id="PG-SWORDBLAST",
    sql="SELECT * FROM characters",
    dag=test_dag
)


pytest.helpers.run_task(task, test_dag)

