.PHONY: deps deploy

deps:
	pip install -r requirements.txt

launch:
	FLASK_APP=fantasyslack/app.py flask run --debugger --reload

deploy:
	./deploy.sh
