FROM tiangolo/meinheld-gunicorn-flask:python3.7

ARG ENV
ENV ENV=${ENV}

WORKDIR /shorty
ADD . .
RUN pip install --upgrade -r requirements.txt && cp ./devops/config.${ENV}.json .
WORKDIR /shorty
CMD ["python", "run.py $ENV"]