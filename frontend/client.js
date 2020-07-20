/**
 *
 * Copyright 2018 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

const {HelloRequest,
       HelloReply} = require('./proto/squeak_admin_pb.js');
const {SqueakAdminClient} = require('./proto/squeak_admin_grpc_web_pb.js');

var client = new SqueakAdminClient('http://localhost:8080');

var request = new HelloRequest();
request.setName('World');

console.log('Testing...');

client.sayHello(request, {}, (err, response) => {
  console.log(response.getMessage());
});
