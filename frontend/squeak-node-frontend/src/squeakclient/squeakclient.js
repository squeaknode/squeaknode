import { SqueakAdminClient } from "../proto/squeak_admin_grpc_web_pb"

console.log("fooooooo")

const PORT = process.env.REACT_APP_PORT;

console.log("port:");
console.log(PORT);

export let client = new SqueakAdminClient('http://' + window.location.hostname + ':' + PORT)
