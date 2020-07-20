import React, { useState, useEffect } from 'react';
import './App.css';

import { HelloRequest,
       HelloReply } from "./proto/squeak_admin_pb"
import { SqueakAdminClient } from "./proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')
function App() {
    console.log('starting App....');
  const [msg, setMsg] = useState("waiting for message...");

  const getMsg = () => {
      console.log("called");

      var helloRequest = new HelloRequest()
      helloRequest.setName('World');

      client.sayHello(helloRequest, {}, (err, response) => {
	  console.log(response.getMessage());
	  setMsg(response.getMessage())
      });
  };

  useEffect(()=>{
    getMsg()
  },[]);

  return (
    <div>
      Message : {msg}
    </div>
  );
}

export default App;
