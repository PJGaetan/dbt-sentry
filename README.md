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


## SVG test

<pre>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" version="1.1">
  <g>
    <rect x="0" y="0" width="800" height="600" fill="#f9f9f9" />
    <g transform="translate(40 40)">
      <g transform="translate(54 0)" />
      <g transform="translate(0 0)">
        <g transform="translate(54 0)">
          <g class="axis bottom">
            <text
              x="333.0"
              y="506.0"
              dy="1em"
              fill="#666"
              transform=""
              text-anchor="middle"
              font-family="Monaco"
              font-size="14"
            >
              Date
            </text>
            <g class="tick">
              <line
                x1="0.0"
                y1="0"
                x2="0.0"
                y2="472.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="0.0"
                y="476.0"
                dy="1em"
                fill="#9c9c9c"
                text-anchor="middle"
                font-family="Monaco"
                font-size="14"
              >
                01
              </text>
            </g>
            <g class="tick">
              <line
                x1="166.5"
                y1="0"
                x2="166.5"
                y2="472.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="166.5"
                y="476.0"
                dy="1em"
                fill="#9c9c9c"
                text-anchor="middle"
                font-family="Monaco"
                font-size="14"
              >
                05
              </text>
            </g>
            <g class="tick">
              <line
                x1="333.0"
                y1="0"
                x2="333.0"
                y2="472.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="333.0"
                y="476.0"
                dy="1em"
                fill="#9c9c9c"
                text-anchor="middle"
                font-family="Monaco"
                font-size="14"
              >
                09
              </text>
            </g>
            <g class="tick">
              <line
                x1="499.5"
                y1="0"
                x2="499.5"
                y2="472.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="499.5"
                y="476.0"
                dy="1em"
                fill="#9c9c9c"
                text-anchor="middle"
                font-family="Monaco"
                font-size="14"
              >
                13
              </text>
            </g>
            <g class="tick">
              <line
                x1="666.0"
                y1="0"
                x2="666.0"
                y2="472.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="666.0"
                y="476.0"
                dy="1em"
                fill="#9c9c9c"
                text-anchor="middle"
                font-family="Monaco"
                font-size="14"
              >
                17
              </text>
            </g>
          </g>
          <g class="axis left">
            <text
              x="-32"
              y="234.0"
              dy=""
              fill="#666"
              transform="rotate(270 -32 234)"
              text-anchor="middle"
              font-family="Monaco"
              font-size="14"
            >
              Temperature (°C)
            </text>
            <g class="tick">
              <line
                x1="-4"
                y1="468"
                x2="666.0"
                y2="468"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="-8"
                y="468"
                dy="0.32em"
                fill="#9c9c9c"
                text-anchor="end"
                font-family="Monaco"
                font-size="14"
              >
                15
              </text>
            </g>
            <g class="tick">
              <line
                x1="-4"
                y1="351.00"
                x2="666.0"
                y2="351.00"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="-8"
                y="351.00"
                dy="0.32em"
                fill="#9c9c9c"
                text-anchor="end"
                font-family="Monaco"
                font-size="14"
              >
                20
              </text>
            </g>
            <g class="tick">
              <line
                x1="-4"
                y1="234.0"
                x2="666.0"
                y2="234.0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="-8"
                y="234.0"
                dy="0.32em"
                fill="#9c9c9c"
                text-anchor="end"
                font-family="Monaco"
                font-size="14"
              >
                25
              </text>
            </g>
            <g class="tick">
              <line
                x1="-4"
                y1="117.00"
                x2="666.0"
                y2="117.00"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="-8"
                y="117.00"
                dy="0.32em"
                fill="#9c9c9c"
                text-anchor="end"
                font-family="Monaco"
                font-size="14"
              >
                30
              </text>
            </g>
            <g class="tick">
              <line
                x1="-4"
                y1="0"
                x2="666.0"
                y2="0"
                stroke="#eee"
                stroke-width="1"
              />
              <text
                x="-8"
                y="0"
                dy="0.32em"
                fill="#9c9c9c"
                text-anchor="end"
                font-family="Monaco"
                font-size="14"
              >
                35
              </text>
            </g>
          </g>
          <g>
            <g class="series dots">
              <circle cx="0.0" cy="453.96" r="3" fill="#e41a1c" />
              <circle cx="41.625" cy="439.92" r="3" fill="#e41a1c" />
              <circle cx="83.25" cy="402.48" r="3" fill="#e41a1c" />
              <circle cx="124.875" cy="386.100" r="3" fill="#e41a1c" />
              <circle cx="166.5" cy="348.660" r="3" fill="#e41a1c" />
              <circle cx="208.125" cy="320.580" r="3" fill="#e41a1c" />
              <circle cx="249.75" cy="287.820" r="3" fill="#e41a1c" />
              <circle cx="291.375" cy="271.44" r="3" fill="#e41a1c" />
              <circle cx="333.0" cy="238.68" r="3" fill="#e41a1c" />
              <circle cx="374.625" cy="210.60" r="3" fill="#e41a1c" />
              <circle cx="416.25" cy="182.52" r="3" fill="#e41a1c" />
              <circle cx="457.875" cy="152.100" r="3" fill="#e41a1c" />
              <circle cx="499.5" cy="124.020" r="3" fill="#e41a1c" />
              <circle cx="541.125" cy="105.300" r="3" fill="#e41a1c" />
              <circle cx="582.75" cy="74.88" r="3" fill="#e41a1c" />
              <circle cx="624.375" cy="56.16" r="3" fill="#e41a1c" />
              <circle cx="666.0" cy="42.12" r="3" fill="#e41a1c" />
            </g>
          </g>
        </g>
      </g>
    </g>
  </g>
</svg>
</pre>

