.PHONY: deps build clean deploy

deps:
	npm install

build:
	npm run-script build

clean:
	rm -rf build

deploy: clean build
	aws s3 sync build s3://fantasyslack/ --delete --acl public-read

launch:
	npm start

