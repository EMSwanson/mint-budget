# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /.

COPY Pipfile Pipfile

RUN pip3 install pipenv --upgrade
RUN pipenv install --deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "budget.py"] 


