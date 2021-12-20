# Databricks Actions

## TL;DR
```yaml
name: Databricks Workflow
on: push
jobs:
  databricks:
    name: Databricks Checkout and Run
    runs-on: ubuntu-latest
        uses: databricks/actions/checkout
        uses: databricks/actions/run
```

## Actions
To properly interact with your workspace, all actions require a [Databricks PAT](https://docs.databricks.com/dev-tools/api/latest/authentication.html) and the actual host to be passed in. Place them as secrets in your repository settings (Settings > Secrets > Actions). For the remainder of this document we assume they are called `DATABRICKS_TOKEN` and `DATABRICKS_HOST`.

_Note_: After private preview the prefix `./.` has to be removed from your workflows.

### Checkout
This action requires a [GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with repo access. See the [Databricks documentation](https://docs.databricks.com/repos.html#configure-your-git-integration-with-databricks) on how to configure the Git integration.

```yaml
uses: frankwis-db/databricks-actions/checkout
with:
    host: ${{ secrets.DATABRICKS_HOST }}
    token: ${{ secrets.DATABRICKS_TOKEN }}
    path: /Repos/{user}/{folder}
```
See [sync-repo.yaml](examples/sync-repo.yaml) for a full workflow example

### DBFS
ToDo
