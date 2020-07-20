# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM node:10-stretch

RUN apt-get -qq update && apt-get -qq install -y \
  unzip

WORKDIR /tmp

RUN curl -sSL https://github.com/protocolbuffers/protobuf/releases/download/v3.12.2/\
protoc-3.12.2-linux-x86_64.zip -o protoc.zip && \
  unzip -qq protoc.zip && \
  cp ./bin/protoc /usr/local/bin/protoc

RUN curl -sSL https://github.com/grpc/grpc-web/releases/download/1.2.0/\
protoc-gen-grpc-web-1.2.0-linux-x86_64 -o /usr/local/bin/protoc-gen-grpc-web && \
  chmod +x /usr/local/bin/protoc-gen-grpc-web

COPY frontend .

RUN mkdir proto
COPY proto/squeak_admin.proto proto/
RUN curl -o rpc.proto -s https://raw.githubusercontent.com/lightningnetwork/lnd/master/lnrpc/rpc.proto
RUN cp rpc.proto proto/lnd.proto

RUN protoc -I=. proto/squeak_admin.proto proto/lnd.proto \
	--js_out=import_style=commonjs:. \
	--grpc-web_out=import_style=commonjs,mode=grpcwebtext:.

RUN npm install && \
	npm link grpc-web && \
	npx webpack client.js

EXPOSE 8081
CMD ["python", "-m", "SimpleHTTPServer", "8081"]
