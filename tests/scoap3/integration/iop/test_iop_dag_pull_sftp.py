import pytest
from airflow.models import DagBag
from scoap3.common.pull_ftp import migrate_from_ftp, trigger_file_processing
from scoap3.iop.repository import IOPRepository
from scoap3.iop.sftp_service import IOPSFTPService
from structlog import get_logger

DAG_NAME = "scoap3_iop_pull_sftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/scoap3/{DAG_NAME}.py") is None
    iop_dag = dagbag.get_dag(dag_id=DAG_NAME)
    return iop_dag

@pytest.fixture
def iop_empty_repo():
    repo = IOPRepository()
    repo.delete_all()
    yield repo


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(dag, iop_empty_repo):
    assert len(iop_empty_repo.find_all()) == 0
    dag.clear()
    dag.test()
    expected_files = [
        {
            "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.pdf",
            "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.xml",
        },
        {
            "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.pdf",
            "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.xml",
        },
        {
            "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.pdf",
            "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.xml",
        },
        {
            "pdf": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.pdf",
            "xml": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.xml",
        },
        {
            "pdf": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.pdf",
            "xml": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.xml",
        },
        {
            "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.pdf",
            "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.xml",
        },
        {"xml": "extracted/aca95c.xml/aca95c.xml"},
    ]

    assert sorted(iop_empty_repo.find_all(), key=lambda x: x.get("xml", "")) == sorted(
        expected_files, key=lambda x: x.get("xml", "")
    )


def test_dag_migrate_from_FTP(iop_empty_repo):
    assert len(iop_empty_repo.find_all()) == 0
    with IOPSFTPService() as sftp:
        migrate_from_ftp(
            sftp,
            iop_empty_repo,
            get_logger().bind(class_name="test_logge"),
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

        expected_files = [
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.xml",
            },
            {
                "pdf": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.pdf",
                "xml": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.xml",
            },
            {
                "pdf": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.pdf",
                "xml": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.xml",
            },
            {"xml": "extracted/aca95c.xml/aca95c.xml"},
        ]
        for (file_from_repo, expected_file) in zip(
            iop_empty_repo.find_all(), expected_files
        ):
            assert file_from_repo == expected_file


def test_dag_trigger_file_processing():
    repo = IOPRepository()
    assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
        "iop", repo, get_logger().bind(class_name="test_logger")
    )
