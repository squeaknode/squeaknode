FROM python:3.8-slim AS compile-image

WORKDIR /

RUN apt-get update && apt-get install -y libpq-dev gcc libffi-dev

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /
COPY libs /libs

RUN pip install psycopg2 && \
	pip install -r requirements.txt

WORKDIR /app

# Copy the source code.
COPY squeaknode ./squeaknode
COPY proto ./proto
COPY LICENSE MANIFEST.in README.md requirements.txt setup.cfg setup.py  ./

RUN python3 setup.py install

FROM python:3.8-slim

COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app

EXPOSE 8774
EXPOSE 8994
EXPOSE 18774
EXPOSE 18994
# Web server
EXPOSE 12994

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Copy the entrypoint script.
COPY "docker/squeaknode/start-squeaknode.sh" .
RUN chmod +x start-squeaknode.sh
