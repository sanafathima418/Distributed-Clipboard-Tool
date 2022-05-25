#!/bin/sh

#gcloud config set compute/zone us-central1-b
#gcloud container clusters create --preemptible mykube

kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl apply -f rabbitmq/rabbitmq-service.yaml

kubectl create -f postgres/postgres-configmap.yaml
kubectl create -f postgres/postgres-storage.yaml  
kubectl create -f postgres/postgres-deployment.yaml
kubectl create -f postgres/postgres-service.yaml

kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml

kubectl apply -f logs/logs-deployment.yaml
