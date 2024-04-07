# DBT testing CLI tool
Inspired by former
    - https://docs.piperider.io/get-started/run
    - https://github.com/InfuseAI/piperider

It uses `dbt` python biding, and make use of `dbt show` to execute inline test.
Reuse manifest to save waiting time.

### Type of tests
- profiling : https://github.com/data-mie/dbt-profiler
- table difference a'la data-diff : https://hub.getdbt.com/dbt-labs/audit_helper/latest/
- Trend difference
    - GROUP BY
    - Perc diff
    - Chart to show that ?

### Test selection
- manual : -s select specific model
- git based 
    - get file changed
    - capture what model are tested in a test (using `compile` and refs)
    - run all test concerning models that could be altered based on model changed (`dbt list model1+ model2+` to get a list)

### Output generated
- Markdown file : https://github.com/didix21/mdutils

Format
```md
# DBT CI tests

## Table profiling

## Compare
```
- csv to share
- png to share
- stdout

### CI Integration
> have a `cli ci gitlab`
> or `cli ci github` kind of cmd
  - gitlab : https://engineering.dunelm.com/how-to-post-a-custom-message-to-your-merge-request-using-gitlabci-3551824a1e5b
  - github

## CMD

```sh
# print to stdout
dbts test profile
dbts test compare
# group by an non group by are essentially the same
# group by just has multiple columns
# and multiple metrics
# I can refacto this into one main 
# TODO: add capability to have non present key (FULL OUTER JOIN)
dbts test scpecific (add capability to run custom test if wanted)

# generate artefact
dbts generate
# push to github/gitlab hooks
dbts ci gitlab/github
```


## Contributing

Install poetry env using.

```bash
poetry install
poetry shell
dbts --help
```

