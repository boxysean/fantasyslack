.PHONY: deps deploy update

deps:
	test -d venv || python3 -m venv venv
	pip install -r requirements.txt

deploy:
	zappa deploy dev

update:
	deploy.sh
