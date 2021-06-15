# syntax=docker/dockerfile:1

FROM python:3.8.2-alpine3.10

WORKDIR /.

COPY Pipfile Pipfile

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver


#RUN apt install -y google-chrome-stable

RUN pip3 install pipenv --upgrade
RUN pipenv install --deploy --ignore-pipfile
RUN pipenv install selenium

COPY . .

CMD ["pipenv", "run", "python", "budget.py"] 


