#!/bin/bash  
docker stop $(docker ps -aq)
docker volume rm $(docker volume ls -q)
docker rm $(docker ps -a -q)
