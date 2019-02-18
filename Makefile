.PHONY: test
test:
	./names.py &
	./seleniumtest.py

.PHONY: docker
docker:
	docker build --no-cache --tag seleniumct .
	#docker build --tag seleniumct .

.PHONY: run-docker
run-docker:
	docker run -p 5000:5000 seleniumct

.PHONY: docker-compose-up
docker-compose-up:
	docker-compose up --detach

.PHONY: docker-compose-stop
docker-compose-stop:
	docker-compose stop

.PHONY: venv
venv:
	virtualenv --python `which python3` venv

.PHONY: pip
pip:
	pip install -r requirements.txt

.PHONY: clean
clean: venv-clean

.PHONY: venv-clean
venv-clean:
	rm -fr venv
