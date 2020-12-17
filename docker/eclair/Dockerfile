FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
	git \
	openjdk-8-jdk \
	ruby-full \
	maven

WORKDIR /

# Copy in the local repository to build from.
RUN git clone https://github.com/bitcoin-s/eclair.git --branch develop

# Install dependencies and install/build eclair.
RUN cd eclair \
	&&  mvn install -DskipTests=true

# Expose eclair ports (server, rpc).
EXPOSE 9735 10009

# Copy the entrypoint script.
COPY "docker/eclair/start-eclair.sh" .
COPY "docker/eclair/wait-for-block-index.sh" .
RUN chmod +x start-eclair.sh
RUN chmod +x wait-for-block-index.sh
