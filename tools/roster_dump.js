async()=>{const po=document.getElementById("profov");if(po)po.style.display="none";const out=[];
for(const C of CH){if(C.hidden||!C.looks)continue;out.push({id:C.id,n:C.n,q:C.q,ty:C.ty,d:C.d,na:C.na,role:C.role,sp:C.sp,g:GTXT[C.id],fs:FSD[C.id]&&FSD[C.id].name,qa:C.qa,
 looks:C.looks.map(L=>[L.cname||'',L.sub||'',L.req||null])});}
return JSON.stringify({ch:out,items:ITEMS.list.map(i=>({n:i.n,c:i.c,d:i.d})),cls:ITEMS.cls,stages:STAGES.filter(s=>!s.hidden).map(s=>s.n||s.name||s.id)});}
