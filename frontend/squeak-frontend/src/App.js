import React, { useState, useEffect } from 'react';
import './App.css';

import { HelloRequest,
       HelloReply } from "./proto/squeak_admin_pb"
import { SqueakAdminClient } from "./proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')
function App() {
    console.log('starting App....');
  const [temp, setTemp] = useState(-9999);

  const getTemp = () => {
      console.log("called");

      var helloRequest = new HelloRequest()
      helloRequest.setName('World');

      client.sayHello(helloRequest, {}, (err, response) => {
	  console.log(response.getMessage());
      });

      // var stream = client.sayHello(helloRequest,{})

      // stream.on('data', function(response){
      // 	  console.log('got response: ' + response);
      //     setTemp(response.getValue())
      // });
  };

  useEffect(()=>{
    getTemp()
  },[]);

  return (
    <div>
      Temperature : {temp} F
    </div>
  );
}

export default App;
