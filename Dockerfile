FROM --platform=linux/amd64 python:3.12.4-alpine
ENV APP_PATH=/opt/web/
ENV STATIC_FOLDER_PATH=$APP_PATH/app/static

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH
COPY ./requirements.txt .

RUN apk update && \
    apk add --no-cache mariadb-dev build-base bash

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["python","app/manage.py","runserver","0.0.0.0:80"]


