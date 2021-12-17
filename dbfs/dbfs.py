import click
import logging

from databricks_cli.sdk import ApiClient
from databricks_cli.dbfs.api import DbfsApi

@click.command()
@click.option('--recursive', type=click.BOOL, required=True)
@click.option('--overwrite', type=click.BOOL, required=True)
@click.option('--source', required=True)
@click.option('--destination', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
def dbfs_copy(recursive, overwrite, source, destination, host, token):
    api_client = ApiClient(host=host, token=token)
    dbfs_api = DbfsApi(api_client)
    target = f"dbfs:{destination}"
    logging.info(f'Copying from {source} to {target}.')
    dbfs_api.cp(recursive, overwrite, source, target)
    logging.info("Done")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbfs_copy()
