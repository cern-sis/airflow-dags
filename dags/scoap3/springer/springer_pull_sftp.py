import scoap3.common.pull_ftp as pull_ftp
import pendulum
from airflow.decorators import dag, task
from scoap3.springer.repository import SpringerRepository
from scoap3.springer.sftp_service import SpringerSFTPService
from structlog import get_logger


@dag(
    start_date=pendulum.today("UTC").add(days=-1),
    schedule="30 */3 * * *",
    params={
        "excluded_directories": [],
        "force_pull": False,
        "filenames_pull": {"enabled": False, "filenames": [], "force_from_ftp": False},
    },
)
def scoap3_springer_pull_sftp():
    logger = get_logger().bind(class_name="springer_pull_sftp")

    @task()
    def migrate_from_ftp(
        repo=SpringerRepository(), sftp=SpringerSFTPService(), **kwargs
    ):
        params = kwargs["params"]
        reprocess_specific_files = (
            "filenames_pull" in params
            and params["filenames_pull"]["enabled"]
            and not params["filenames_pull"]["force_from_ftp"]
        )
        if reprocess_specific_files:
            specific_files_names = pull_ftp.reprocess_files(repo, logger, **kwargs)
            return specific_files_names
        with sftp:
            return pull_ftp.migrate_from_ftp(sftp, repo, logger, **kwargs)

    @task()
    def trigger_file_processing(repo=SpringerRepository(), filenames=None):
        return pull_ftp.trigger_file_processing(
            publisher="springer", repo=repo, logger=logger, filenames=filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames=filenames)


dag_taskflow = scoap3_springer_pull_sftp()
