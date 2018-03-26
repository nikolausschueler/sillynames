test:
	./run.sh &
	./seleniumtest.py

docker:
	#docker build --no-cache --tag seleniumct .
	docker build --tag seleniumct .

.PHONY: run-docker
run-docker:
	docker run -p 5000:5000 seleniumct
