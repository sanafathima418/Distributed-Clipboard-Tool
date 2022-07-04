# Distributed Clipboard Tool


A multi-threaded, micro-service based application that syncs clipboard contents across various devices. It is a zero trust system that authenticates and authorizes users using OAuth 2.0 tokens where the communication between client and server is secured by HTTPS with cert-manager used to simplify the process of obtaining, renewing and using TLS certificates.


## Architecture Diagram
<img width="800" alt="image" src="https://user-images.githubusercontent.com/29837264/177219032-f0124126-3d57-4ecd-a3ac-92febf79000e.png">


## Componenets

**REST Client:** Listener that captures copy and paste requests and forwards the same to the server. <br /> On copy - Clipboard contents are copied and transferred to the server. <br /> On Paste - Copied content is fetched from the server.<br />
**REST Server** Accepts requests from client to store copied content or transfer the copied contents in the cache<br />
**Kubernetes:** For deploying the application and facilitating horizontal scaling along with load balancing <br />
**Redis Cache:** Stores user data: UserID, Payload(data copied) <br />
**PostgreSQL Database:** Store user credentials(UserID, Password) for authentication <br />
**RabbitMQ :** Logging of messages <br />

## How HTTPS communication was achieved
To secure communication between rest client and server(ingress), cert-manager was used that relied on LetsEncrypt to obtain, distribute and renew certificates. When the client pings the server for the first time, the public keys are exchanged which will then be used to secure the communication channel between the parties.

## Usage of OAuth 2.0 framework
JWT tokens were used to authorizate and identify the user pinging the resource server so the respective user-specific contents are delivered.

