VERSION=v4
DOCKERUSER=maashaik

build:
	docker build -t rest-server . --platform linux/amd64

push:
	docker tag rest-server $(DOCKERUSER)/rest-server:$(VERSION)
	docker push $(DOCKERUSER)/rest-server:$(VERSION)
	docker tag rest-server $(DOCKERUSER)/rest-server:latest
	docker push $(DOCKERUSER)/rest-server:latest
