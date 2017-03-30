FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
COPY . /app
RUN pip install -q -v -r /app/requirements.txt
