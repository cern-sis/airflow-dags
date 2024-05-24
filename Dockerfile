FROM apache/airflow:2.8.3-python3.8
ENV AIRFLOW_HOME=/opt/airflow
WORKDIR /opt/airflow
RUN curl -o constraints.txt 'https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt'
COPY requirements.txt ./requirements.txt
COPY requirements-airflow.txt ./requirements-airflow.txt
COPY requirements-test.txt ./requirements-test.txt
RUN pip install --no-cache-dir --user -r requirements.txt -r requirements-test.txt -r requirements-airflow.txt
