test-audit:
	pushd jaffle_shop &&\
		dbt run &&\
		dbt run --target=prd &&\
		popd
	pytest --ignore=jaffle_shop/dbt_packages/ -rP -vv

test-ci:
	CURRENT_GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD) &&\
			   git checkout -D test-ci-branch &&\
			   git checkout -b test-ci-branch &&\
			   echo "\n" >> jaffle_shop/models/orders.sql &&\
			   git add jaffle_shop/models/orders.sql &&\
			   git commit -m "test-ci-branch" &&\
			   git checkout $CURRENT_GIT_BRANCH
	# pushd jaffle_shop &&\
	# 	dbt run &&\
	# 	dbt run --target=prd &&\
	# 	popd
	# pytest --ignore=jaffle_shop/dbt_packages/ -rP -vv