(this["webpackJsonptwitter-frontend"]=this["webpackJsonptwitter-frontend"]||[]).push([[4],{141:function(e,a,t){},143:function(e,a,t){"use strict";t.r(a);var n=t(10),l=t(0),c=t.n(l),r=(t(141),t(18),t(16)),m=(t(14),t(19),t(41),t(42),t(7)),s=t(13),i=t(3),o=t(30);a.default=Object(r.h)((function(e){var a=Object(l.useState)(!1),t=Object(n.a)(a,2),r=(t[0],t[1],Object(l.useState)(!1)),d=Object(n.a)(r,2),u=d[0],p=d[1],E=Object(l.useState)(""),b=Object(n.a)(E,2),v=(b[0],b[1]),f=Object(l.useState)(""),N=Object(n.a)(f,2),k=(N[0],N[1],Object(l.useState)(!1)),h=Object(n.a)(k,2),O=h[0],g=h[1],j=Object(l.useState)(!1),w=Object(n.a)(j,2),y=w[0],S=w[1],P=Object(l.useState)(!1),C=Object(n.a)(P,2),I=C[0],T=C[1],q=Object(l.useState)(""),M=Object(n.a)(q,2),x=(M[0],M[1],Object(l.useState)(!1)),B=Object(n.a)(x,2),D=(B[0],B[1]),R=Object(l.useState)("Members"),A=Object(n.a)(R,2),V=(A[0],A[1],Object(l.useState)(!1)),z=Object(n.a)(V,2),J=(z[0],z[1],Object(l.useState)(!1)),H=Object(n.a)(J,2),L=H[0],W=H[1],F=Object(i.c)(o.d),G=Object(i.b)();Object(l.useEffect)((function(){window.scrollTo(0,0),G(Object(o.b)({network:e.match.params.network,host:e.match.params.host,port:e.match.params.port}))}),[]);var K=Object(l.useRef)(!0);Object(l.useEffect)((function(){K.current?K.current=!1:document.getElementsByTagName("body")[0].style.cssText=L&&"overflow-y: hidden; margin-right: 17px"}),[L]),Object(l.useEffect)((function(){return function(){return document.getElementsByTagName("body")[0].style.cssText=""}}),[]);var Q=function(){var e={peerId:F.getPeerId()};G(Object(o.f)(e)),Z()};var U=function(a){var t=a.values;G(Object(o.i)({name:t.name,host:e.match.params.host,port:e.match.params.port,network:e.match.params.network})),$()},X=function(e){var a=e.values;console.log("Calling editPeer with name:",a.name),alert("Rename peer not yet implemented!"),D(!0),Y()},Y=function(e,a){p(!1),W(!L),D(!1),v(F.getPeerName()),setTimeout((function(){g(!O)}),20)},Z=function(){p(!1),W(!L),D(!1),setTimeout((function(){S(!y)}),20)},$=function(e,a){p(!1),W(!L),setTimeout((function(){T(!I)}),20)},_=function(e){e.stopPropagation()},ee=function(){p(!u)},ae=function(){return c.a.createElement(s.b,{onSubmit:U,className:"Squeak-input-side"},c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement(s.c,{class:"informed-input",name:"name",label:"Peer Name (not required)"})),c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement(s.c,{class:"informed-input",name:"host",label:"Host",defaultValue:e.match.params.host,readOnly:!0,disabled:!0})),c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement(s.c,{class:"informed-input",name:"port",type:"number",label:"Port",defaultValue:e.match.params.port,readOnly:!0,disabled:!0})),c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement(s.a,{class:"informed-input",name:"useTor",label:"Connect With Tor: ",defaultValue:"TORV3"===e.match.params.network,disabled:!0})),c.a.createElement("div",{className:"inner-input-links"},c.a.createElement("div",{className:"input-links-side"}),c.a.createElement("div",{className:"squeak-btn-holder"},c.a.createElement("div",{style:{fontSize:"13px",color:null}}),c.a.createElement("button",{type:"submit",className:"squeak-btn-side squeak-btn-active"},"Submit"))))},te=function(){return c.a.createElement(s.b,{onSubmit:Q,className:"Squeak-input-side"},c.a.createElement("div",{className:"inner-input-links"},c.a.createElement("div",{className:"input-links-side"}),c.a.createElement("div",{className:"squeak-btn-holder"},c.a.createElement("div",{style:{fontSize:"13px",color:null}}),c.a.createElement("button",{type:"submit",className:"squeak-btn-side squeak-btn-active"},"Delete"))))},ne=function(){return c.a.createElement(s.b,{onSubmit:X,className:"Squeak-input-side"},c.a.createElement("div",{className:"edit-input-wrap"},c.a.createElement(s.c,{class:"informed-input",name:"name",label:"Peer Name"})),c.a.createElement("div",{className:"inner-input-links"},c.a.createElement("div",{className:"input-links-side"}),c.a.createElement("div",{className:"squeak-btn-holder"},c.a.createElement("div",{style:{fontSize:"13px",color:null}}),c.a.createElement("button",{type:"submit",className:"squeak-btn-side squeak-btn-active"},"Submit"))))};return c.a.createElement("div",null,c.a.createElement("div",{className:"profile-wrapper"},c.a.createElement("div",{className:"profile-header-wrapper"},c.a.createElement("div",{className:"profile-header-back"},c.a.createElement("div",{onClick:function(){return window.history.back()},className:"header-back-wrapper"},c.a.createElement(m.a,null))),c.a.createElement("div",{className:"profile-header-content"},c.a.createElement("div",{className:"profile-header-name"},e.match.params.host,":",e.match.params.port))),c.a.createElement("div",{className:"profile-details-wrapper"},c.a.createElement("div",{className:"profile-options"},F&&c.a.createElement("div",{id:"profileMoreMenu",onClick:ee,className:"Nav-link"},c.a.createElement("div",{className:"Nav-item-hover"},c.a.createElement(m.w,null)),c.a.createElement("div",{onClick:function(){return ee()},style:{display:u?"block":"none"},className:"more-menu-background"},c.a.createElement("div",{className:"more-modal-wrapper"},u?c.a.createElement("div",{style:{top:document.getElementById("profileMoreMenu")&&"".concat(document.getElementById("profileMoreMenu").getBoundingClientRect().top-40,"px"),left:document.getElementById("profileMoreMenu")&&"".concat(document.getElementById("profileMoreMenu").getBoundingClientRect().left,"px"),height:"210px"},onClick:function(e){return function(e){e.stopPropagation()}(e)},className:"more-menu-content"},c.a.createElement("div",{onClick:Z,className:"more-menu-item"},c.a.createElement("span",null,"Delete Peer")),c.a.createElement("div",{onClick:Y,className:"more-menu-item"},c.a.createElement("span",null,"Edit Peer"))):null))),F&&c.a.createElement("div",{onClick:function(e){return F.getAutoconnect()?function(e,a){e.stopPropagation();var t={peerId:F.getPeerId()};G(Object(o.g)(t))}(e,F.getPeerId()):function(e,a){e.stopPropagation(),console.log(a),console.log(F.getPeerId());var t={peerId:F.getPeerId()};G(Object(o.h)(t))}(e,F.getPeerId())},className:F.getAutoconnect()?"enable-btn-wrap disable-switch":"enable-btn-wrap"},c.a.createElement("span",null,c.a.createElement("span",null,F.getAutoconnect()?"Enabled":"Disabled")))),c.a.createElement("div",{className:"profile-details-box"},c.a.createElement("div",{className:"profile-name"},F&&F.getPeerName()),c.a.createElement("div",{className:"profile-username"},e.match.params.host,":",e.match.params.port)),c.a.createElement("div",{className:"profile-options"},!F&&c.a.createElement("div",{onClick:function(e){return $("edit")},className:"profiles-create-button"},c.a.createElement("span",null,"Add Saved Peer")))),c.a.createElement("div",{className:"feed-wrapper"},c.a.createElement("div",{className:"feed-trending-card"},c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Number of downloads"),c.a.createElement("div",null,"TODO")),c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Number of purchases"),c.a.createElement("div",null,"TODO")),c.a.createElement("div",{className:"feed-card-trend"},c.a.createElement("div",null,"Last connection time"),c.a.createElement("div",null,"TODO"))))),c.a.createElement("div",{onClick:function(){return Z()},style:{display:y?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return _(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return Z()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"'Delete Peer'")),c.a.createElement("div",{className:"modal-body"},c.a.createElement(te,null)))),c.a.createElement("div",{onClick:function(){return $()},style:{display:I?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return _(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return $()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"Save Peer")),c.a.createElement("div",{className:"modal-body"},c.a.createElement(ae,null)))),c.a.createElement("div",{onClick:function(){return Y()},style:{display:O?"block":"none"},className:"modal-edit"},c.a.createElement("div",{onClick:function(e){return _(e)},className:"modal-content"},c.a.createElement("div",{className:"modal-header"},c.a.createElement("div",{className:"modal-closeIcon"},c.a.createElement("div",{onClick:function(){return Y()},className:"modal-closeIcon-wrap"},c.a.createElement(m.d,null))),c.a.createElement("p",{className:"modal-title"},"Edit Peer")),c.a.createElement("div",{className:"modal-body"},c.a.createElement(ne,null)))))}))}}]);
//# sourceMappingURL=4.e66590da.chunk.js.map