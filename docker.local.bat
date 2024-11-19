@echo off

docker rmi jaws-api

docker build . -t jaws-api

docker run -p 8000:80 --name jaws-api --rm -it jaws-api