# DBT testing CLI tool
Inspired by former
    - https://docs.piperider.io/get-started/run
    - https://github.com/InfuseAI/piperider

It uses `dbt` python biding, and make use of `dbt show` to execute inline test.
Reuse manifest to save waiting time.

## Compare & analyse

Table profiling

```sh
dbts audit profile stg_customers --target-compare prd
```

Compare model

```sh
dbts audit compare-model stg_customers --target-compare prd
```

Compare row by row (you can also provide a path to the manifest to use for comparison directly).

```sh
dbts audit compare-rows stg_customers --manifest-compare-path m.json
```

Compare metric /w group by 

```sh
dbts audit metric customers "sum(number_of_orders)" last_name --dbt-path jaffle_shop --target-compare prd
```

Custom test, you can provide a directory with `-R`.
```sh
dbts audit custom testci -R 
```

## CI Integration

IN PROGRESS

```sh
dbts ci generate
dbts ci gitlab
dbts ci github
```
- gitlab : https://engineering.dunelm.com/how-to-post-a-custom-message-to-your-merge-request-using-gitlabci-3551824a1e5b
- github

## TODO
- better input filter 
    - git to determine what changed
        - get file changed
        - capture what model are tested in a test (using `compile` and refs)
        - run all test concerning models that could be altered based on model changed (`dbt list model1+ model2+` to get a list)
    - parse run_result to see what was the last tables run
    - [x] ask for two target or override manifest or specify table
    - [x] manual model selection : -s select specific model

- better ouput generation
    - file
        - Markdown file : https://github.com/didix21/mdutils
    - [x] stdout
    - store in dbt
- plot graph in terminal : plotext

## Contributing

Install poetry env using.

```bash
poetry install
poetry shell
dbts --help
```

