import click
import logging
from os import path
from glob import glob

from databricks_cli.sdk import ApiClient
from databricks_cli.dbfs.api import DbfsApi, DbfsPath
from databricks_cli.dbfs.dbfs_path import DbfsPath

@click.command()
@click.option('--overwrite', type=click.BOOL, required=True)
@click.option('--source', required=True)
@click.option('--destination', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
def dbfs_copy(overwrite, source, destination, host, token):
    client = ApiClient(host=host, token=token)
    dbfs_api = DbfsApi(client)
    target = f"dbfs:{destination}"
    logging.info(f'Copying from {source} to {target}.')

    for file_name in glob(source, recursive = True):
        full_local_path = path.abspath(file_name)
        if path.isdir(full_local_path):
            continue
        relative = path.relpath(full_local_path)
        full_dbfs_path = path.join(target, relative)
        dbfs_folder = DbfsPath(path.dirname(full_dbfs_path))
        if not overwrite and dbfs_api.file_exists(DbfsPath(full_dbfs_path)):
            logging.info(f"Skipping file {full_dbfs_path}")
            continue

        logging.info(f'Copying {full_local_path} to {full_dbfs_path}.')
        dbfs_api.mkdirs(dbfs_folder)
        dbfs_api.put_file(full_local_path, DbfsPath(full_dbfs_path), overwrite)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dbfs_copy()
