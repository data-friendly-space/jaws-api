@echo off

docker build . -t jaws-api

docker run -p 8000:8000 --name jaws-api --rm -it jaws-api