import { SqueakAdminClient } from "../proto/squeak_admin_grpc_web_pb"

export let client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')
