# pull official base image
FROM python:3.10-alpine

# set work directory
RUN mkdir /app
WORKDIR /app

# NOTE: adding user and run as non-root is not possible since we need the device /dev/mem
# set environment variables

# install dependencies
RUN apk add --no-cache g++ libstdc++ libffi-dev openssl openssl-dev && \
    apk add --no-cache rust cargo python3-dev && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./src /app/src
COPY ./main.py /app/main.py
RUN mkdir config

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

CMD ["python3", "main.py"]