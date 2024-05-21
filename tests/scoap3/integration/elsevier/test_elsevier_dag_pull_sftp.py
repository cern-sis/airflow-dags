from airflow.models import DagBag
from scoap3.common.pull_ftp import migrate_from_ftp
from pytest import fixture
from scoap3.elsevier.repository import ElsevierRepository
from scoap3.elsevier.sftp_service import ElsevierSFTPService
from structlog import get_logger

DAG_NAME = "scoap3_elsevier_pull_sftp"


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/scoap3/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@fixture
def elsevier_empty_repo():
    repo = ElsevierRepository()
    repo.delete_all()
    yield repo


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_migrate_from_FTP(elsevier_empty_repo):
    assert len(elsevier_empty_repo.find_all()) == 0
    with ElsevierSFTPService() as ftp:
        migrate_from_ftp(
            ftp,
            elsevier_empty_repo,
            get_logger().bind(class_name="test_logger"),
            publisher="elsevier",
            **{
                "params": {
                    "excluded_directories": [],
                    "force_pull": False,
                    "filenames_pull": {
                        "enabled": False,
                        "filenames": [],
                        "force_from_ftp": False,
                    },
                }
            },
        )
        assert elsevier_empty_repo.get_all_raw_filenames() == [
            "CERNQ000000010011A.tar",
            "CERNQ000000010669A.tar",
            "vtex00403986_a-2b_CLEANED.zip",
        ]
