(this["webpackJsonptwitter-frontend"]=this["webpackJsonptwitter-frontend"]||[]).push([[4],{123:function(e,t,a){},126:function(e,t,a){"use strict";a.r(t);var n=a(5),c=a(0),r=a.n(c),l=(a(123),a(18)),s=a.n(l),o=a(9),m=a(8),i=(a(12),a(19),a(10),a(11),a(4));t.default=Object(o.i)((function(e){var t=Object(c.useContext)(m.a),a=t.state,l=t.actions,o=Object(c.useState)(!1),d=Object(n.a)(o,2),u=(d[0],d[1],Object(c.useState)("")),p=Object(n.a)(u,2),v=p[0],E=p[1],N=Object(c.useState)(""),b=Object(n.a)(N,2),f=(b[0],b[1],Object(c.useState)(!1)),h=Object(n.a)(f,2),k=h[0],g=h[1],w=Object(c.useState)(!1),j=Object(n.a)(w,2),O=j[0],C=j[1],P=Object(c.useState)(""),y=Object(n.a)(P,2),S=(y[0],y[1],Object(c.useState)(!1)),T=Object(n.a)(S,2),A=(T[0],T[1]),I=Object(c.useState)("Members"),M=Object(n.a)(I,2),B=(M[0],M[1],Object(c.useState)(!1)),x=Object(n.a)(B,2),R=(x[0],x[1],Object(c.useState)(!1)),D=Object(n.a)(R,2),J=D[0],L=D[1],q=a.peer,z=a.peerConnection;a.list;Object(c.useEffect)((function(){window.scrollTo(0,0),l.getPeer({network:e.match.params.network,host:e.match.params.host,port:e.match.params.port}),l.getPeerConnection({network:e.match.params.network,host:e.match.params.host,port:e.match.params.port})}),[]);var F=Object(c.useRef)(!0);Object(c.useEffect)((function(){F.current?F.current=!1:document.getElementsByTagName("body")[0].style.cssText=J&&"overflow-y: hidden; margin-right: 17px"}),[J]),Object(c.useEffect)((function(){return function(){return document.getElementsByTagName("body")[0].style.cssText=""}}),[]);var G=function(){L(!J),A(!1),setTimeout((function(){g(!k)}),20)},H=function(e,t){L(!J),setTimeout((function(){C(!O)}),20)},K=function(e){e.stopPropagation()};return r.a.createElement("div",null,r.a.createElement("div",{className:"bookmarks-wrapper"},r.a.createElement("div",{className:"bookmarks-header-wrapper"},r.a.createElement("div",{className:"profile-header-back"},r.a.createElement("div",{onClick:function(){return window.history.back()},className:"header-back-wrapper"},r.a.createElement(i.a,null))),r.a.createElement("div",{className:"bookmarks-header-content"},r.a.createElement("div",{className:"bookmarks-header-name"},q&&q.getPeerName()),r.a.createElement("div",{className:"bookmarks-header-squeaks"},e.match.params.host,":",e.match.params.port))),r.a.createElement("div",{className:"listp-details-wrap"},r.a.createElement("div",{className:"bookmarks-header-name"},q&&q.getPeerName()),r.a.createElement("div",{className:"list-owner-wrap"},r.a.createElement("div",null,e.match.params.host,":",e.match.params.port)),r.a.createElement("div",{className:"profile-options"},q&&r.a.createElement("div",{onClick:function(e){return G()},className:"peer-connect-button"},r.a.createElement("span",null,"Delete")),!q&&r.a.createElement("div",{onClick:function(e){return H("edit")},className:"profiles-create-button"},r.a.createElement("span",null,"Add Saved Peer"))),r.a.createElement("div",{className:"profile-options"},r.a.createElement("div",{onClick:function(t){return z?void l.disconnectPeer({host:e.match.params.host,port:e.match.params.port,network:e.match.params.network}):void l.connectPeer({host:e.match.params.host,port:e.match.params.port,network:e.match.params.network})},className:z?"disconnect peer-connect-button":"peer-connect-button"},r.a.createElement("span",null,r.a.createElement("span",null,z?"Connected":"Connect")))),r.a.createElement("div",{className:"profile-options"},q&&r.a.createElement("div",{onClick:function(e){return q.getAutoconnect()?function(e,t){e.stopPropagation(),l.setPeerNotAutoconnect(t)}(e,q.getPeerId()):function(e,t){e.stopPropagation(),l.setPeerAutoconnect(t)}(e,q.getPeerId())},className:q.getAutoconnect()?"remove-autoconnect peer-connect-button":"peer-connect-button"},r.a.createElement("span",null,r.a.createElement("span",null,q.getAutoconnect()?"Autoconnecting":"Not Autoconnecting"))))),r.a.createElement("div",{className:"feed-wrapper"},z&&r.a.createElement("div",{className:"feed-trending-card"},r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Connection Time"),r.a.createElement("div",null,s()(1e3*z.getConnectTimeS()).fromNow(!0))),r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Bytes received"),r.a.createElement("div",null,z.getNumberBytesReceived())),r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Messages received"),r.a.createElement("div",null,z.getNumberMessagesReceived())),r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Last Message Received Time"),r.a.createElement("div",null,s()(1e3*z.getLastMessageReceivedTimeS()).fromNow(!0))),r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Bytes sent"),r.a.createElement("div",null,z.getNumberBytesSent())),r.a.createElement("div",{className:"feed-card-trend"},r.a.createElement("div",null,"Messages sent"),r.a.createElement("div",null,z.getNumberMessagesSent()))))),r.a.createElement("div",{onClick:function(){return G()},style:{display:k?"block":"none"},className:"modal-edit"},r.a.createElement("div",{onClick:function(e){return K(e)},className:"modal-content"},r.a.createElement("div",{className:"modal-header"},r.a.createElement("div",{className:"modal-closeIcon"},r.a.createElement("div",{onClick:function(){return G()},className:"modal-closeIcon-wrap"},r.a.createElement(i.d,null))),r.a.createElement("p",{className:"modal-title"},"'Delete Peer'"),r.a.createElement("div",{className:"save-modal-wrapper"},r.a.createElement("div",{onClick:function(){var e={peerId:q.getPeerId()};l.deletePeer(e),G()},className:"save-modal-btn"},"Delete"))))),r.a.createElement("div",{onClick:function(){return H()},style:{display:O?"block":"none"},className:"modal-edit"},r.a.createElement("div",{onClick:function(e){return K(e)},className:"modal-content"},r.a.createElement("div",{className:"modal-header"},r.a.createElement("div",{className:"modal-closeIcon"},r.a.createElement("div",{onClick:function(){return H()},className:"modal-closeIcon-wrap"},r.a.createElement(i.d,null))),r.a.createElement("p",{className:"modal-title"},"Save Peer"),r.a.createElement("div",{className:"save-modal-wrapper"},r.a.createElement("div",{onClick:function(){l.savePeer({name:v,host:e.match.params.host,port:e.match.params.port,network:e.match.params.network}),H()},className:"save-modal-btn"},"Submit"))),r.a.createElement("div",{className:"modal-body"},r.a.createElement("form",{className:"edit-form"},r.a.createElement("div",{className:"edit-input-wrap"},r.a.createElement("div",{className:"edit-input-content"},r.a.createElement("label",null,"Name"),r.a.createElement("input",{onChange:function(e){return E(e.target.value)},type:"text",name:"name",className:"edit-input"}))))))))}))}}]);
//# sourceMappingURL=4.04dd649a.chunk.js.map