#!/bin/bash

python3 server.py &
SERVER_PID=$!

sleep 1 #server up wait

#get packages
curl -i localhost:5000/ricedb/api/v1.0/packages

#create package 
curl -u logos:linux -i localhost:5000/ricedb/api/v1.0/packages -X POST -d '{"title":"logos","program":"i3","url":"http://penisland.com","images":"sth","description":"your server is working. Congrats..."}' -H "Content-Type:application/json"

kill $SERVER_PID
exit 0
