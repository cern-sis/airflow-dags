import json

import pytest
from airflow.models import DagBag
from scoap3.aps.aps_api_client import APSApiClient
from scoap3.aps.aps_params import APSParams
from scoap3.aps.repository import APSRepository
from scoap3.aps.utils import save_file_in_s3

DAG_NAME = "scoap3_aps_pull_api"
TRIGGERED_DAG_NAME = "scoap3_aps_pull_api"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/scoap3/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 3


@pytest.mark.vcr
def test_aps_pull_api(dag):
    repo = APSRepository()
    repo.delete_all()
    dates = {
        "from_date": "2022-02-05",
        "until_date": "2022-03-05",
    }
    assert len(repo.find_all()) == 0
    parameters = APSParams(
        from_date=dates["from_date"],
        until_date=dates["until_date"],
    ).get_params()
    aps_api_client = APSApiClient()
    articles_metadata = str.encode(
        json.dumps(aps_api_client.get_articles_metadata(parameters))
    )
    save_file_in_s3(articles_metadata, repo)
    assert len(repo.find_all()) == 1


@pytest.mark.skip("Flaky test: passes locally, but not on github actions")
@pytest.mark.vcr
def test_dag_run(dag):
    repo = APSRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    dag.clear()
    dag.test(
        run_conf={
            "from_date": "2022-02-07",
            "until_date": "2022-02-07",
            "per_page": "1",
        }
    )
    assert len(repo.find_all()) == 1
