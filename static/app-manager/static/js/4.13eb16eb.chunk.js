(this["webpackJsonpjts-manager"]=this["webpackJsonpjts-manager"]||[]).push([[4],{488:function(e,s,t){},489:function(e,s,t){"use strict";var c=t(20),a=t(12),l=t(11),i=t(155),n=t(1),r=t(4),o=t.n(r),j=t(572),d=t(571),b=t(116),m=t(17),x=["label","hideIcon","showIcon","visible","className","htmlFor","placeholder","iconSize","inputClassName","invalid"],h=Object(n.forwardRef)((function(e,s){var t,r=e.label,h=e.hideIcon,O=e.showIcon,u=e.visible,f=e.className,p=e.htmlFor,g=e.placeholder,v=e.iconSize,N=e.inputClassName,y=e.invalid,w=Object(i.a)(e,x),C=Object(n.useState)(u),k=Object(l.a)(C,2),F=k[0],L=k[1];return Object(m.jsxs)(n.Fragment,{children:[r?Object(m.jsx)(b.u,{className:"form-label",for:p,children:r}):null,Object(m.jsxs)(b.s,{className:o()((t={},Object(a.a)(t,f,f),Object(a.a)(t,"is-invalid",y),t)),children:[Object(m.jsx)(b.r,Object(c.a)(Object(c.a)({ref:s,invalid:y,type:!1===F?"password":"text",placeholder:g||"\xb7\xb7\xb7\xb7\xb7\xb7\xb7\xb7\xb7\xb7\xb7\xb7",className:o()(Object(a.a)({},N,N))},r&&p?{id:p}:{}),w)),Object(m.jsx)(b.t,{className:"cursor-pointer",onClick:function(){return L(!F)},children:function(){var e=v||14;return!1===F?h||Object(m.jsx)(j.a,{size:e}):O||Object(m.jsx)(d.a,{size:e})}()})]})]})}));s.a=h,h.defaultProps={visible:!1}},886:function(e,s,t){"use strict";t.r(s);var c=t(20),a=t(1),l=t(8),i=t(154),n=t(491),r=t(166),o=t(169),j=t.n(o),d=t(156),b=t(494),m=t(564),x=t(531),h=t(541),O=t(573),u=t(610),f=t(537),p=t(577),g=t(161),v=t(160),N=t(490),y=t(489),w=t(492),C=t(116),k=(t(488),t(17)),F=function(e){var s=e.t,t=e.name,c=e.role;return Object(k.jsxs)("div",{className:"d-flex",children:[Object(k.jsx)("div",{className:"me-1",children:Object(k.jsx)(N.a,{size:"sm",color:"success",icon:Object(k.jsx)(m.a,{size:12})})}),Object(k.jsxs)("div",{className:"d-flex flex-column",children:[Object(k.jsxs)("div",{className:"d-flex justify-content-between",children:[Object(k.jsx)("h6",{children:t}),Object(k.jsx)(x.a,{size:12,className:"cursor-pointer",onClick:function(){return j.a.dismiss(s.id)}})]}),Object(k.jsxs)("span",{children:["You have successfully logged in as an ",c," user to Vuexy. Now you can start to explore. Enjoy!"]})]})]})},L={password:"admin",loginEmail:"admin@demo.com"};s.default=function(){var e=Object(n.a)().skin,s=Object(d.b)(),o=Object(l.m)(),m=Object(a.useContext)(v.a),x=Object(b.e)({defaultValues:L}),N=x.control,E=x.setError,z=x.handleSubmit,P=x.formState.errors,G="dark"===e?"login-v2-dark.svg":"login-v2.svg",S=t(493)("./".concat(G)).default;return Object(k.jsx)("div",{className:"auth-wrapper auth-cover",children:Object(k.jsxs)(C.D,{className:"auth-inner m-0",children:[Object(k.jsxs)(i.b,{className:"brand-logo",to:"/",onClick:function(e){return e.preventDefault()},children:[Object(k.jsxs)("svg",{viewBox:"0 0 139 95",version:"1.1",height:"28",children:[Object(k.jsxs)("defs",{children:[Object(k.jsxs)("linearGradient",{x1:"100%",y1:"10.5120544%",x2:"50%",y2:"89.4879456%",id:"linearGradient-1",children:[Object(k.jsx)("stop",{stopColor:"#000000",offset:"0%"}),Object(k.jsx)("stop",{stopColor:"#FFFFFF",offset:"100%"})]}),Object(k.jsxs)("linearGradient",{x1:"64.0437835%",y1:"46.3276743%",x2:"37.373316%",y2:"100%",id:"linearGradient-2",children:[Object(k.jsx)("stop",{stopColor:"#EEEEEE",stopOpacity:"0",offset:"0%"}),Object(k.jsx)("stop",{stopColor:"#FFFFFF",offset:"100%"})]})]}),Object(k.jsx)("g",{id:"Page-1",stroke:"none",strokeWidth:"1",fill:"none",fillRule:"evenodd",children:Object(k.jsx)("g",{id:"Artboard",transform:"translate(-400.000000, -178.000000)",children:Object(k.jsxs)("g",{id:"Group",transform:"translate(400.000000, 178.000000)",children:[Object(k.jsx)("path",{d:"M-5.68434189e-14,2.84217094e-14 L39.1816085,2.84217094e-14 L69.3453773,32.2519224 L101.428699,2.84217094e-14 L138.784583,2.84217094e-14 L138.784199,29.8015838 C137.958931,37.3510206 135.784352,42.5567762 132.260463,45.4188507 C128.736573,48.2809251 112.33867,64.5239941 83.0667527,94.1480575 L56.2750821,94.1480575 L6.71554594,44.4188507 C2.46876683,39.9813776 0.345377275,35.1089553 0.345377275,29.8015838 C0.345377275,24.4942122 0.230251516,14.560351 -5.68434189e-14,2.84217094e-14 Z",id:"Path",className:"text-primary",style:{fill:"currentColor"}}),Object(k.jsx)("path",{d:"M69.3453773,32.2519224 L101.428699,1.42108547e-14 L138.784583,1.42108547e-14 L138.784199,29.8015838 C137.958931,37.3510206 135.784352,42.5567762 132.260463,45.4188507 C128.736573,48.2809251 112.33867,64.5239941 83.0667527,94.1480575 L56.2750821,94.1480575 L32.8435758,70.5039241 L69.3453773,32.2519224 Z",id:"Path",fill:"url(#linearGradient-1)",opacity:"0.2"}),Object(k.jsx)("polygon",{id:"Path-2",fill:"#000000",opacity:"0.049999997",points:"69.3922914 32.4202615 32.8435758 70.5039241 54.0490008 16.1851325"}),Object(k.jsx)("polygon",{id:"Path-2",fill:"#000000",opacity:"0.099999994",points:"69.3922914 32.4202615 32.8435758 70.5039241 58.3683556 20.7402338"}),Object(k.jsx)("polygon",{id:"Path-3",fill:"url(#linearGradient-2)",opacity:"0.099999994",points:"101.428699 0 83.0667527 94.1480575 130.378721 47.0740288"})]})})})]}),Object(k.jsx)("h2",{className:"brand-text text-primary ms-1",children:"Vuexy"})]}),Object(k.jsx)(C.i,{className:"d-none d-lg-flex align-items-center p-5",lg:"8",sm:"12",children:Object(k.jsx)("div",{className:"w-100 d-lg-flex align-items-center justify-content-center px-5",children:Object(k.jsx)("img",{className:"img-fluid",src:S,alt:"Login Cover"})})}),Object(k.jsx)(C.i,{className:"d-flex align-items-center auth-bg px-2 p-lg-5",lg:"4",sm:"12",children:Object(k.jsxs)(C.i,{className:"px-xl-2 mx-auto",sm:"8",md:"6",lg:"12",children:[Object(k.jsx)(C.h,{tag:"h2",className:"fw-bold mb-1",children:"Welcome to Vuexy! \ud83d\udc4b"}),Object(k.jsx)(C.g,{className:"mb-2",children:"Please sign-in to your account and start the adventure"}),Object(k.jsxs)(C.a,{color:"primary",children:[Object(k.jsxs)("div",{className:"alert-body font-small-2",children:[Object(k.jsx)("p",{children:Object(k.jsxs)("small",{className:"me-50",children:[Object(k.jsx)("span",{className:"fw-bold",children:"Admin:"})," admin@demo.com | admin"]})}),Object(k.jsx)("p",{children:Object(k.jsxs)("small",{className:"me-50",children:[Object(k.jsx)("span",{className:"fw-bold",children:"Client:"})," client@demo.com | client"]})})]}),Object(k.jsx)(h.a,{id:"login-tip",className:"position-absolute",size:18,style:{top:"10px",right:"10px"}}),Object(k.jsx)(C.H,{target:"login-tip",placement:"left",children:"This is just for ACL demo purpose."})]}),Object(k.jsxs)(C.o,{className:"auth-login-form mt-2",onSubmit:z((function(e){if(Object.values(e).every((function(e){return e.length>0})))r.a.login({email:e.loginEmail,password:e.password}).then((function(e){var t=Object(c.a)(Object(c.a)({},e.data.userData),{},{accessToken:e.data.accessToken,refreshToken:e.data.refreshToken});s(Object(g.b)(t)),m.update(e.data.userData.ability),o(Object(w.a)(t.role)),j()((function(e){return Object(k.jsx)(F,{t:e,role:t.role||"admin",name:t.fullName||t.username||"John Doe"})}))})).catch((function(e){return console.log(e)}));else for(var t in e)0===e[t].length&&E(t,{type:"manual"})})),children:[Object(k.jsxs)("div",{className:"mb-1",children:[Object(k.jsx)(C.u,{className:"form-label",for:"login-email",children:"Email"}),Object(k.jsx)(b.a,{id:"loginEmail",name:"loginEmail",control:N,render:function(e){var s=e.field;return Object(k.jsx)(C.r,Object(c.a)({autoFocus:!0,type:"email",placeholder:"john@example.com",invalid:P.loginEmail&&!0},s))}})]}),Object(k.jsxs)("div",{className:"mb-1",children:[Object(k.jsxs)("div",{className:"d-flex justify-content-between",children:[Object(k.jsx)(C.u,{className:"form-label",for:"login-password",children:"Password"}),Object(k.jsx)(i.b,{to:"/forgot-password",children:Object(k.jsx)("small",{children:"Forgot Password?"})})]}),Object(k.jsx)(b.a,{id:"password",name:"password",control:N,render:function(e){var s=e.field;return Object(k.jsx)(y.a,Object(c.a)({className:"input-group-merge",invalid:P.password&&!0},s))}})]}),Object(k.jsxs)("div",{className:"form-check mb-1",children:[Object(k.jsx)(C.r,{type:"checkbox",id:"remember-me"}),Object(k.jsx)(C.u,{className:"form-check-label",for:"remember-me",children:"Remember Me"})]}),Object(k.jsx)(C.c,{type:"submit",color:"primary",block:!0,children:"Sign in"})]}),Object(k.jsxs)("p",{className:"text-center mt-2",children:[Object(k.jsx)("span",{className:"me-25",children:"New on our platform?"}),Object(k.jsx)(i.b,{to:"/register",children:Object(k.jsx)("span",{children:"Create an account"})})]}),Object(k.jsx)("div",{className:"divider my-2",children:Object(k.jsx)("div",{className:"divider-text",children:"or"})}),Object(k.jsxs)("div",{className:"auth-footer-btn d-flex justify-content-center",children:[Object(k.jsx)(C.c,{color:"facebook",children:Object(k.jsx)(O.a,{size:14})}),Object(k.jsx)(C.c,{color:"twitter",children:Object(k.jsx)(u.a,{size:14})}),Object(k.jsx)(C.c,{color:"google",children:Object(k.jsx)(f.a,{size:14})}),Object(k.jsx)(C.c,{className:"me-0",color:"github",children:Object(k.jsx)(p.a,{size:14})})]})]})})]})})}}}]);
//# sourceMappingURL=4.13eb16eb.chunk.js.map