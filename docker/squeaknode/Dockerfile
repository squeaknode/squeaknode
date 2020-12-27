FROM python:3.8-slim

WORKDIR /

RUN apt-get update && apt-get install -y libpq-dev gcc libffi-dev

COPY requirements.txt /
COPY libs /libs

RUN pip install psycopg2 && \
	pip install -r requirements.txt

RUN apt-get autoremove -y gcc

WORKDIR /app

# Copy the source code.
COPY alembic ./alembic
COPY squeaknode ./squeaknode
COPY proto ./proto
COPY alembic.ini LICENSE MANIFEST.in README.md requirements.txt setup.cfg setup.py  ./

RUN python3 setup.py install

EXPOSE 8774
EXPOSE 8994
EXPOSE 18774
EXPOSE 18994
# Web server
EXPOSE 12994

# Copy the entrypoint script.
COPY "docker/squeaknode/start-squeaknode.sh" .
RUN chmod +x start-squeaknode.sh
