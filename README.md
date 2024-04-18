# DBT testing CLI tool

Changing some of your dbt model, and you want to know how this is going to affect your production tables.

`dbt-sentry` allows you to dress a profile of the model that you have changed in the CI.


It uses `dbt` python biding, and make use of `dbt inline` to leverage dbt for querying.
- Only compile manifest once per target to save time.
- Reuse dbt profile for connection: no additional configuration to set-up.

## Dbt Sentry commands

### Dependencies

To run some commands, `dbts` depend on macros build by the community.
Install them by adding them to your `packages.yml` & `dbt deps`.

```
# packages.yml
packages:
  - package: dbt-labs/audit_helper
    version: 0.11.0
  - package: data-mie/dbt_profiler
    version: 0.8.1
```

### Compare & analyse

Table profiling

```sh
dbts audit profile stg_customers
```

Compare model

```sh
dbts audit compare-model stg_customers --target-compare prd --primary-key customer_id
```

Compare row by row (you can also provide a path to the manifest to use for comparison directly).

```sh
dbts audit compare-rows stg_customers --manifest-compare-path manifest.json -k customer_id
```

Compare metric /w group by 

```sh
dbts audit metric customers "sum(number_of_orders)" last_name --target-compare prd
```

Custom test, you can provide a directory with `-R`.
```sh
dbts audit custom testci -R 
dbts audit custom testci/file.sql
```

### CI Integration


```sh
dbts ci generate
dbts ci gitlab
dbts ci github
```
-> don't work github don't render markdown too
> No need for images, go render everything in svg using agate tables
> Could use https://leather.readthedocs.io/en/latest/api/chart.html#leather.Chart.add_series for more complicated render
> pretty easy to do 
> https://github.com/wireservice/agate/blob/master/agate/table/bar_chart.py

- gitlab : https://engineering.dunelm.com/how-to-post-a-custom-message-to-your-merge-request-using-gitlabci-3551824a1e5b
    - notes : https://docs.gitlab.com/ee/api/notes.html#create-new-merge-request-note
    - image : https://docs.gitlab.com/ee/api/project_import_export.html#import-a-file-from-aws-s3
    - markdown gitlab : https://docs.gitlab.com/ee/user/markdown.html
- github
    - comment : https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28

## Contributing

Not yet open to external contribution, the project is not ready for it.

### TODO
- [ ] dbt generate run custom in passed folder when model part of the query
- [ ] parse run_result to see what was the last tables run -> to run right after dbt run .
- [ ] Markdown file refacto using this https://github.com/didix21/mdutils ?
- [ ] store results in db ?
- [ ] add mermaid graph of dbt
- [ ] get rid of external dependencies
- [ ] configuration to avoid passing params *possibilities:* - would allow to see metrics trends in ci
    - yaml
    - dbt config meta
- [ ] `dbts ci push-*` to push code by adding a comment to the MR OR template on how to do so
- [ ] plot graph in terminal : plotext


## Development

Install poetry env using.

```bash
poetry install
poetry shell
dbts --help
```

### Alternatives
- [piperider](https://github.com/InfuseAI/piperider)
- [data-diff](https://github.com/datafold/data-diff)

