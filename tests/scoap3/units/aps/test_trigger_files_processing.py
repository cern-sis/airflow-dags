import json
import random
import string
from io import BytesIO

from airflow.models import DagBag
from airflow.models.dagrun import DagRun
from scoap3.aps.utils import trigger_file_processing_DAG


class S3BucketResultObj:
    def __init__(self, key):
        self.key = key


S3_RETURNED_VALUES = ["file1.json", "file2.json"]
FIND_ALL_EXPECTED_VALUES = ["file1.json", "file2.json"]

pseudo_article = {
    "data": [{"identifiers": {"doi": "100"}}, {"identifiers": {"doi": "100"}}]
}
file = BytesIO(json.dumps(pseudo_article).encode("utf-8"))

TRIGGERED_DAG_NAME = "scoap3_aps_process_file"


def get_dag_runs(dag_id, states=[]):
    dagbag = DagBag()
    # Check DAG exists.
    assert dag_id in dagbag.dags

    dag_runs = list()
    for state in states:
        state = state.lower() if state else None
        for run in DagRun.find(dag_id=dag_id, state=state):
            dag_runs.append(run.run_id)
    return dag_runs


def generate_pesudo_dois():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


def test_trigger_file_processing():
    id_and_articles = [
        {
            "article": {"identifiers": {"doi": "100"}},
            "id": f"APS_{generate_pesudo_dois()}__2022-04-29T15:38:32.871034",
        },
        {
            "article": {"identifiers": {"doi": "100"}},
            "id": f"APS_{generate_pesudo_dois()}__2022-04-29T15:38:32.871047",
        },
    ]
    trigger_file_processing_DAG(id_and_articles)

    runs_ids = get_dag_runs(
        TRIGGERED_DAG_NAME, states=["success", "running", "queued", "failed"]
    )
    for obj in id_and_articles:
        assert obj["id"] in runs_ids
