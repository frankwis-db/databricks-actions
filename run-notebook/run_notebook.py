import click
import logging
import time

from databricks_cli.sdk import ApiClient
from databricks_cli.runs.api import RunsApi

@click.command()
@click.option('--notebook-path', required=True)
@click.option('--runtime-version', required=True)
@click.option('--node-type', required=True)
@click.option('--num-workers', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
def run_notebook(notebook_path, runtime_version, node_type, num_workers, host, token):
    api_client = ApiClient(host=host, token=token)
    runs_api = RunsApi(api_client)
    cluster_conf = {
        'spark_version': runtime_version,
        'node_type_id': node_type,
        'num_workers': num_workers,
    }
    run_conf = {
        'new_cluster': cluster_conf,
        'notebook_task': {
            'notebook_path': notebook_path,
        },
    }
    run_id = runs_api.submit_run(json=run_conf)['run_id']
    logging.info(f'Submitted run with ID {run_id}.')

    run_info = runs_api.get_run(run_id)
    run_url = run_info['run_page_url']
    logging.info(f'Run URL: {run_url}')

    run_state = None
    while run_state not in ['TERMINATED', 'SKIPPED', 'INTERNAL_ERROR']:
        logging.info('Waiting for run to finish ...')
        time.sleep(10)
        run_info = runs_api.get_run(run_id)
        run_state = run_info['state']['life_cycle_state']

    
    if run_info['state']['result_state'] == 'SUCCESS':
        logging.info('Run succeeded.')
    else:
        state_message = run_info['state']['state_message']
        raise RuntimeError(f'Run failed: {state_message}. Visit {run_url} to see detailed logs.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    run_notebook()
