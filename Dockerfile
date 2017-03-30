FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

ENV APP_ENTRYPOINT web
ENV LOG_LEVEL info
ENV MU_SPARQL_ENDPOINT 'http://database:8890/sparql'
ENV MU_SPARQL_UPDATEPOINT 'http://database:8890/sparql'
ENV MU_APPLICATION_GRAPH 'http://mu.semte.ch/application'

COPY . /app
RUN pip install -q -v -r /app/requirements.txt
