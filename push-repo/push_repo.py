import click
import logging

from databricks_cli.sdk import ApiClient
from databricks_cli.repos.api import ReposApi

@click.command()
@click.option('--url', required=True)
@click.option('--path', required=True)
@click.option('--host', required=True)
@click.option('--token', required=True)
@click.option('--branch', required=True)
def push_repo(url, path, host, token, branch):
    api_client = ApiClient(host=host, token=token)
    repos_api = ReposApi(api_client)
    try:
        repo_id = repos_api.get_repo_id(path)
        logging.info(f'Found repo at {path} with ID {repo_id}.')
        repo_info = repos_api.get(repo_id)
        repo_provider = repo_info['provider']
        assert repo_provider == 'gitHub', f'Repo is not a GitHub repo: {repo_provider}.'
        repo_url = repo_info['url']
        assert repo_url == url, f'Repo exists but URL does not match: {repo_url} != {url}.'
    except RuntimeError:
        # check the output
        logging.info(f'No repo found at {path}.')
        repo_id = repos_api.create(url=url, provider='gitHub', path=path)['id']
        print(repo_id)
        logging.info(f'Created repo at {path} with ID {repo_id}.')
    repos_api.update(repo_id, branch=branch, tag=None)
    logging.info(f'Updated the repo to branch {branch}.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    push_repo()
