(this["webpackJsonptwitter-frontend"]=this["webpackJsonptwitter-frontend"]||[]).push([[4],{141:function(e,t,a){},143:function(e,t,a){"use strict";a.r(t);var n=a(10),l=a(0),c=a.n(l),r=(a(141),a(18),a(16)),m=(a(13),a(19),a(41),a(42),a(7)),o=a(3),s=a(30);t.default=Object(r.h)((function(e){var t=Object(l.useState)(!1),a=Object(n.a)(t,2),r=(a[0],a[1],Object(l.useState)(!1)),i=Object(n.a)(r,2),d=i[0],u=i[1],p=Object(l.useState)(""),E=Object(n.a)(p,2),f=E[0],v=E[1],N=Object(l.useState)(""),b=Object(n.a)(N,2),g=(b[0],b[1],Object(l.useState)(!1)),O=Object(n.a)(g,2),h=O[0],j=O[1],k=Object(l.useState)(!1),w=Object(n.a)(k,2),y=w[0],C=w[1],I=Object(l.useState)(!1),P=Object(n.a)(I,2),S=P[0],M=P[1],T=Object(l.useState)(""),x=Object(n.a)(T,2),B=(x[0],x[1],Object(l.useState)(!1)),D=Object(n.a)(B,2),A=(D[0],D[1]),R=Object(l.useState)("Members"),J=Object(n.a)(R,2),V=(J[0],J[1],Object(l.useState)(!1)),L=Object(n.a)(V,2),q=(L[0],L[1],Object(l.useState)(!1)),z=Object(n.a)(q,2),F=z[0],G=z[1],H=Object(o.c)(s.d),K=Object(o.b)();Object(l.useEffect)((function(){window.scrollTo(0,0),K(Object(s.b)({network:e.match.params.network,host:e.match.params.host,port:e.match.params.port}))}),[]);var Q=Object(l.useRef)(!0);Object(l.useEffect)((function(){Q.current?Q.current=!1:document.getElementsByTagName("body")[0].style.cssText=F&&"overflow-y: hidden; margin-right: 17px"}),[F]),Object(l.useEffect)((function(){return function(){return document.getElementsByTagName("body")[0].style.cssText=""}}),[]);var U=function(e,t){G(!F),A(!1),v(H.getPeerName()),setTimeout((function(){j(!h)}),20)},W=function(){G(!F),A(!1),setTimeout((function(){C(!y)}),20)},X=function(e,t){G(!F),setTimeout((function(){M(!S)}),20)},Y=function(e){e.stopPropagation()},Z=function(){u(!d)};return c.a.createElement("div",null,c.a.createElement("div",{className:"profile-wrapper"},c.a.createElement("div",{className:"profile-header-wrapper"},c.a.createElement("div",{className:"profile-header-back"},c.a.createElement("div",{onClick:function(){return window.history.back()},className:"header-back-wrapper"},c.a.createElement(m.a,null))),c.a.createElement("div",{className:"profile-header-content"},c.a.createElement("div",{className:"profile-header-name"},e.match.params.host,":",e.match.params.port))),c.a.createElement("div",{className:"profile-details-wrapper"},c.a.createElement("div",{className:"profile-options"},H&&c.a.createElement("div",{id:"profileMoreMenu",onClick:Z,className:"Nav-link"},c.a.createElement("div",{className:"Nav-item-hover"},c.a.createElement(m.w,null)),c.a.createElement("div",{onClick:function(){return Z()},style:{display:d?"block":"none"},className:"more-menu-background"},c.a.createElement("div",{className:"more-modal-wrapper"},d?c.a.createElement("div",{style:{top:document.getElementById("profileMoreMenu")&&"".concat(document.getElementById("profileMoreMenu").getBoundingClientRect().top-40,"px"),left:document.getElementById("profileMoreMenu")&&"".concat(document.getElementById("profileMoreMenu").getBoundingClientRect().left,"px"),height:"210px"},onClick:function(e){return function(e){e.stopPropagation()}(e)},className:"more-menu-content"},c.a.createElement("div",{onClick:W,className:"more-menu-item"},c.a.createElement("span",null,"Delete Profile")),c.a.createElement("div",{onClick:U,className:"more-menu-item"},c.a.createElement("span",null,"Edit Profile"))):null))),H&&c.a.createElement("div",{onClick:function(e){return H.getAutoconnect()?function(e,t){e.stopPropagation();var a={peerId:H.getPeerId()};K(Object(s.g)(a))}(e,H.getPeerId()):function(e,t){e.stopPropagation(),console.log(t),console.log(H.getPeerId());var a={peerId:H.getPeerId()};K(Object(s.h)(a))}(e,H.getPeerId())},className:H.getAutoconnect()?"enable-btn-wrap disable-switch":"enable-btn-wrap"},c.a.createElement("span",null,c.a.createElement("span",null,H.getAutoconnect()?"Enabled":"Disabled")))),c.a.createElement("div",{className:"profile-details-box"},c.a.createElement("div",{className:"profile-name"},H&&H.getPeerName()),c.a.createElement("div",{className:"profile-username"},e.match.params.host,":",e.match.params.port)),c.a.createElement("div",{className:"profile-options"},!H&&c.a.createElement("div",{onClick:function(e){return X("edit")},className:"profiles-create-button"},c.a.createElement("span",null,"Add Saved Peer")))),c.a.createElement("div",{className:"feed-wrapper"},c.a.createElement("div",{className:"feed-trending-card"},c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Number of downloads"),c.a.createElement("div",null,"TODO")),c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Number of purchases"),c.a.createElement("div",null,"TODO")),c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Last connection time"),c.a.createElement("div",null,"TODO"))))),c.a.createElement("div",{onClick:function(){return W()},style:{display:y?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return Y(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return W()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"'Delete Peer'"),c.a.createElement("div",{className:"save-modal-wrapper"},c.a.createElement("div",{onClick:function(){var e={peerId:H.getPeerId()};K(Object(s.f)(e)),W()},className:"save-modal-btn"},"Delete"))))),c.a.createElement("div",{onClick:function(){return X()},style:{display:S?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return Y(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return X()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"Save Peer"),c.a.createElement("div",{className:"save-modal-wrapper"},c.a.createElement("div",{onClick:function(){var t=e.match.params.host.replace(/^https?:\/\//,"");K(Object(s.i)({name:f,host:t,port:e.match.params.port,network:e.match.params.network})),X()},className:"save-modal-btn"},"Submit"))),c.a.createElement("div",{className:"modal-body"},c.a.createElement("form",{className:"edit-form"},c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement("div",{className:"edit-input-content"},c.a.createElement("label",null,"Name"),c.a.createElement("input",{onChange:function(e){return v(e.target.value)},type:"text",name:"name",className:"edit-input"}))))))),c.a.createElement("div",{onClick:function(){return U()},style:{display:h?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return Y(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return U()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"'Edit Profile'"),c.a.createElement("div",{className:"save-modal-wrapper"},c.a.createElement("div",{onClick:function(){H.getPeerId();alert("Rename peer not yet implemented!"),A(!0),U()},className:"save-modal-btn"},"Save"))),c.a.createElement("div",{className:"modal-body"},H?c.a.createElement("form",{className:"edit-form"},c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement("div",{className:"edit-input-content"},c.a.createElement("label",null,"Name"),c.a.createElement("input",{defaultValue:H.getPeerName(),onChange:function(e){return v(e.target.value)},type:"text",name:"name",className:"edit-input"})))):c.a.createElement("form",{className:"create-form"},c.a.createElement("div",{className:"create-input-wrap"},c.a.createElement("div",{className:"create-input-content"},c.a.createElement("label",null,"Name"),c.a.createElement("input",{defaultValue:"",onChange:function(e){return v(e.target.value)},type:"text",name:"name",className:"edit-input"}))))))))}))}}]);
//# sourceMappingURL=4.9fa333a6.chunk.js.map