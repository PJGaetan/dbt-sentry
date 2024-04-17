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

- IDEAD : add mermaid graph of dbt ?

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


### Testing

#### audit

- run dbt project in dev and prd (the project is set up to change the number between target)
- run the test on correct files

#### ci

- create another branch (delete if exists), add a space to a file and commit it
- run the test generate part

