VERSION=v3
DOCKERUSER=maashaik

#
# You should probably update the docker.io user if you update this
#

build:
	docker build -t logs  . --platform linux/amd64
push:
	docker tag logs  $(DOCKERUSER)/logs:$(VERSION)
	docker push $(DOCKERUSER)/logs:$(VERSION)
	docker tag logs  $(DOCKERUSER)/logs:latest
	docker push $(DOCKERUSER)/logs:latest