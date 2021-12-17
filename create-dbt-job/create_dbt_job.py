import click
import logging
import time

from databricks_cli.sdk import ApiClient
from databricks_cli.jobs.api import JobsApi

@click.command()
@click.option('--project-directory', required=True)
@click.option('--target', required=True)
@click.option('--operation', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
def create_dbt_job(project_directory, target, operation, host, token):
    api_client = ApiClient(host=host, token=token)
    jobs_api = JobsApi(api_client)
    dbt_task_conf = {
        'project_directory': project_directory,
        'target': target,
        'operation':operation
    }
    jobs_conf = {
      'name': 'dbt job from Github Actions',
      'tasks': [
        {
          'task_key': 'dbt_task',
          'description': 'dbt task created from Github Actions',
          'depends_on': [],
          'new_cluster': {
            'spark_version': '9.1.x-scala2.12',
            'node_type_id': 'Standard_DS3_v2',
            'spark_conf': {
              'spark.speculation': True
            },
            'aws_attributes': {
              'availability': 'SPOT',
              'zone_id': 'us-west-2a'
            },
            'autoscale': {
              'min_workers': 2,
              'max_workers': 16
            }
          },
          'dbt_task': dbt_task_conf,
          'timeout_seconds': 86400,
          'max_retries': 3,
          'min_retry_interval_millis': 2000,
          'retry_on_timeout': False
        }
      ],
      'job_clusters': null,
      'email_notifications': {
        'on_start': [],
        'on_success': [],
        'on_failure': [],
        'no_alert_for_skipped_runs': False
      },
      'timeout_seconds': 86400,
      'schedule': null,
      'max_concurrent_runs': 10,
      'format': 'MULTI_TASK',
      'access_control_list': []
    }
    job_id = jobs_api.create_job(json=jobs_conf)['job_id']
    logging.info(f'Successfully created job {job_id}.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    create_dbt_job()
