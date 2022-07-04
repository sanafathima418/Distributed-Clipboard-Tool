# Distributed Clipboard Tool


A multi-threaded, micro-service based application that syncs clipboard contents across various devices. It is a zero trust system that authenticates and authorizes users using OAuth 2.0 tokens where the communication between client and server is secured by HTTPS with cert-manager used to simplify the process of obtaining, renewing and using TLS certificates.


## Architecture Diagram
<img width="384" alt="image" src="https://user-images.githubusercontent.com/29837264/177219032-f0124126-3d57-4ecd-a3ac-92febf79000e.png">


## Componenets

REST Server and Client: To send and receive data
Kubernetes: Deployment, scalability and load balancing
Redis Cache: UserID, Payload(data copied)
PostgreSQL database: Store user data(UserID, Password) for authorization/authentication
RabbitMQ : Logging of messages
