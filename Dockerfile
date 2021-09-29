FROM python:3.8-slim-buster AS compile-image

WORKDIR /

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
	apt-get install -y \
	libpq-dev \
	gcc \
	libffi-dev \
	build-essential

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /

RUN pip install --upgrade pip && \
	pip install -r requirements.txt

WORKDIR /app

# Copy the source code.
COPY squeaknode ./squeaknode
COPY proto ./proto
COPY LICENSE MANIFEST.in README.md requirements.txt setup.cfg setup.py  ./

RUN pip install .[postgres]

FROM python:3.8-slim-buster

COPY --from=compile-image /opt/venv /opt/venv

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
	apt-get install -y libpq-dev

EXPOSE 8555
EXPOSE 18555
EXPOSE 18666
EXPOSE 18777
# Web server
EXPOSE 12994

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Copy the entrypoint script.
COPY "start-squeaknode.sh" .
RUN chmod +x start-squeaknode.sh

CMD ["./start-squeaknode.sh"]
