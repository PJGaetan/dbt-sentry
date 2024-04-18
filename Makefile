#!make

CURRENT_GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

test:
	git branch -D test-ci-branch || true &&\
	   git checkout -b test-ci-branch &&\
	   git stash &&\
	   echo "\n" >> jaffle_shop/models/orders.sql &&\
	   git add jaffle_shop/models/orders.sql &&\
	   git commit -m "test-ci-branch" &&\
	   git stash pop &&\
        	pushd jaffle_shop &&\
		poetry run dbt run --target=prd &&\
		popd &&\
	   git checkout ${CURRENT_GIT_BRANCH}
	pushd jaffle_shop &&\
		poetry run dbt run &&\
		popd
	tox run
	git branch -D test-ci-branch || true
