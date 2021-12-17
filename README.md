# Databricks Actions
_Hackathon Q4/21 Project_

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

### Private Preview
As long as these actions are in private preview (a.k.a a private GitHub repo) you would need to add a custom step to pull these actions into your workflow:

```yaml
- name: Install Databricks Actions
    uses: actions/checkout@v2
    with:
        repository: frankwis-db/databricks-action
        token: ${{ secrets.GH_TOKEN }}
        path: .databricks/actions
```

This step requires a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with repo access. Place it as a secret (Settings > Secrets > Actions) for your repository. In this example it is named `GH_TOKEN`.

This enables the workflow to use an action via `uses: ./.databricks/actions/{your-action}`.

## Actions
To properly interact with your workspace, all actions require a [Databricks PAT](https://docs.databricks.com/dev-tools/api/latest/authentication.html) and the actual host to be passed in. Place them as secrets in your repository settings (Settings > Secrets > Actions). For the remainder of this document we assume they are called `DATABRICKS_TOKEN` and `DATABRICKS_HOST`.

_Note_: After private preview the prefix `./.` has to be removed from your workflows.

### Checkout
This action requires a [GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with repo access. See the [Databricks documentation](https://docs.databricks.com/repos.html#configure-your-git-integration-with-databricks) on how to configure the Git integration.

```yaml
name: Databricks Workflow
on: push
jobs:
  databricks:
    name: Sync Repository
    runs-on: ubuntu-latest
    steps:
      - name: Install Databricks Actions
        uses: actions/checkout@v2
        with:
          repository: frankwis-db/databricks-action
          token: ${{ secrets.GH_TOKEN }}
          path: .databricks/actions
      - name: Databricks Checkout
        uses: ./.databricks/actions/checkout
        with:
            host: ${{ secrets.DATABRICKS_HOST }}
            token: ${{ secrets.DATABRICKS_TOKEN }}
            path: /Repos/{user}/{folder}
```
