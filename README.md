## key-value-pair


It is a simple key value store web service.

python 3.5 is required.

### Directory Structure
```
├── backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
├── frontend
│   ├── client.py
│   └── requirements.txt
└── README.md
```

#### To setup the server run following commands:
```
git clone https://github.com/ankitsaini2609/key-value-pair.git
cd key-value-pair/backend
docker build -t server .
docker run -p 80:80 server
```

#### To setup the client run following commands:
**pip3 install -r frontend/requirements.txt**

Now find the ip address of docker and replace it in client file in this [line](https://github.com/ankitsaini2609/key-value-pair/blob/4116b1bd72da0fa624287bd2597eabd974da83c0/frontend/client.py#L114). 

**python3.5 client.py**


check the usage video :)
