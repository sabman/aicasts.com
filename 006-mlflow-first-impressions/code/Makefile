.PHONY: clean
# Substitute your own docker index username, if you like.
DOCKER_USER=sabman
DOCKER_REPO_NAME=mlflow

# Change this to suit your needs.
CONTAINER_NAME:=lon-dev-mlflow
LOG_DIR:=`pwd`/logs/$(CONTAINER_NAME)/log
FILE_STORE:=$(shell pwd)/mlruns
PORT:=5000

DOCKER_RUN_COMMON=--name="$(CONTAINER_NAME)" \
	-v $(LOG_DIR):/var/log -v $(FILE_STORE):/mlflow\
	-p $(PORT):5000 \
	$(DOCKER_USER)/$(DOCKER_REPO_NAME)

all: build

build:
	docker build \
		--build-arg BACKEND_URI=${BACKEND_URI} \
		--build-arg BUCKET=${BUCKET} \
		-t="$(DOCKER_USER)/$(DOCKER_REPO_NAME)" .

run:
	mkdir -p $(LOG_DIR)
	docker run -d $(DOCKER_RUN_COMMON)

bash:
	mkdir -p $(LOG_DIR)
	docker run -t -i $(DOCKER_RUN_COMMON) /bin/bash

# Removes existing containers.
clean:
	docker  ps -a | grep $(CONTAINER_NAME) | awk '{print $$1}' | xargs docker stop

rmi:
	docker images -a | grep $(DOCKER_REPO_NAME) | awk '{print $$3}' | xargs docker rmi

# Deletes the directories and unused containers/images
deepclean: clean
	rm -rf $(LOG_DIR)
	@echo "Remove all non running containers"
	-docker rm `docker ps -q -f status=exited`
	@echo "Delete all untagged/dangling (<none>) images"
	-docker rmi `docker images -q -f dangling=true`
