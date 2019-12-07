### Time Series streaming service

(tested with python 3.7)
***

Service consists of 2 parts: 
* server - continuously generates and sends data through websocket connection

* client - receives data from server, filters numbers,
store records in file and streams it to the web page trough web-sockets

Client depends on server, but if server lost connection with client -
it will save the state of time series for current client. 
By default server uses port 8081 and client uses 8082

***
#### Viewing time series in browser

go to `http://localhost:8082/index` or `http://localhost:8082/`

***
#### Starting service

To start locally run both services you need to have installed 
python 3.7

In this case firstly create virtual environments for project
And activate it

```
python3.7 -m venv venv
source /venv/bin/activate
```

install packages from requirements.txt located at root path:

``pip install requirements.txt``

There are scripts run.py in both directories
ts_server and ts_client. Run commands in different terminals (or use IDE instead)

```
python ts_server/run.py  
python ts_clients/run.py
```
To run services in docker just run the command

``docker-compose up -d`` 

To stop

``docker-compose stop``

To clean up everything after usage

``docker-compose down -v --rmi all --remove-orphans``