# Simple-Client-Server-File-transfer

There are two scripts: server.py and client.py

Clien connect to server and start to send a file:

+ Send file name
+ Send file size
+ Send file in chunck of 512 b

To run a server you need replace **your_server_ip** with IP of your server: localhost or Public IPv4 DNS of AWS instance

```python
    TCP_IP = socket.gethostbyaddr("your_server_ip")[0]
```

To run simply type in terminal:

```
python3 server.py
```

And to run client:

```
python3 client.py file domain-name|ip-address port-number
```
