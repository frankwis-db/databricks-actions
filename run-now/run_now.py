import click
import logging

from databricks_cli.sdk import ApiClient
from databricks_cli.jobs.api import JobsApi

@click.command()
@click.option('--job-id', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
def run_now(job_id, host, token):
    api_client = ApiClient(host=host, token=token)
    jobs_api = JobsApi(api_client)
    try:
        run_id = jobs_api.run_now(job_id=job_id, jar_params=None, notebook_params=None, python_params=None, spark_submit_params=None)['run_id']
        logging.info(f'Run {run_id} was trigger for job {job_id}.')
    except RuntimeError:
        logging.info(f'Cannot run job {job_id}.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    run_now()
