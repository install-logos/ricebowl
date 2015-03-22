#!/bin/bash

python3 ricedb_server.py &
SERVER_PID=$!

sleep 1 #server up wait

#get packages
curl -i localhost:5000/ricedb/api/v1.0/packages
curl -i localhost:5000/ricedb/api/v1.0/packages/1

#create package 
curl -u logos:linux -i localhost:5000/ricedb/api/v1.0/packages -X POST -d '{"title":"logos","program":"i3","url":"http://penisland.com","images":"sth","description":"your server is working. Congrats..."}' -H "Content-Type:application/json"

kill $SERVER_PID
exit 0
