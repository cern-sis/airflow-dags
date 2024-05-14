FROM apache/airflow:2.8.3
COPY requirements.txt /
COPY requirements-airflow.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt -r /requirements-airflow.txt
