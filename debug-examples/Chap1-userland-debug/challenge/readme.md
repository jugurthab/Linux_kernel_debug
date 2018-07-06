# Chap1-userland-debug/challenge

Challenge example on debugging userland applications. one need to troubleshoot communication between client (or clients) and a server as well as bugs associated with each. 

# Folder layout

- **client.h** : Header definition file for **client.c**.

- **client.c** : Code logic implementing a client capable to connect to a **server.c**.

- **server.h** : Header definition file for **server.c**.

- **server.c** : server code example, that accepts connections from **client.c** and stores them in **log.txt**.

- **log.txt** : Log file containing IP addresses of connected clients (**client.c**) and ports.

# Usage

- Compile and launch server code :

> gcc server.c -o server
> ./server

- Compile and run the client :

> gcc client.c -o client
> ./client

### Important

You can start multiple clients (*pay attention to your server resources!*).

# Feedbacks
Please feel free to contact me : <jugurtha.belkalem@smile.fr>
