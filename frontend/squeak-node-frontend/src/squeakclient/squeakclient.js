import { SqueakAdminClient } from "../proto/squeak_admin_grpc_web_pb"

const PORT = process.env.REACT_APP_PORT;

console.log("port:");
console.log(PORT);

const rpc_port = PORT ? PORT : 8080

console.log("rpc_port:");
console.log(rpc_port);

export let client = new SqueakAdminClient('http://' + window.location.hostname + ':' + rpc_port)
