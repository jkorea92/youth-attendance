from pathlib import Path
import re

FILES = [Path('index.html'), Path('app-v4.html')]

CSS = r'''
/* attendance-types-20260910 */
.member-editor{display:flex;flex-direction:column;gap:8px;margin-top:8px}.member-row{display:grid;grid-template-columns:minmax(110px,1fr) minmax(105px,.8fr) minmax(130px,1.2fr) auto;gap:7px;align-items:center;padding:8px;border:1px solid var(--line);border-radius:11px;background:#fff}.member-row input,.member-row select{min-width:0}.member-summary{display:flex;flex-direction:column;gap:6px;margin-top:9px}.member-summary-row{display:grid;grid-template-columns:minmax(90px,.8fr) minmax(90px,.7fr) minmax(0,1.5fr);gap:8px;padding:7px 9px;border:1px solid var(--line);border-radius:9px;background:#fff;font-size:12px}.part-badge{display:inline-block;padding:4px 7px;border-radius:999px;background:#eef2ff;color:var(--p);font-size:11px;font-weight:800}.na{font-size:12px;color:var(--muted);font-weight:700}.track-title{font-size:11px;font-weight:900;color:#475467;margin-bottom:5px}.dual-rate{font-size:21px!important;line-height:1.35}.status-section{margin-top:10px;border-top:1px solid var(--line);padding-top:9px}.status-section-title{font-size:12px;font-weight:900;margin-bottom:7px}
@media(max-width:760px){.member-row{grid-template-columns:1fr 1fr}.member-row [data-member-note]{grid-column:1 / -1}.member-row .danger{grid-column:1 / -1}.member-summary-row{grid-template-columns:1fr 1fr}.member-summary-row span:last-child{grid-column:1 / -1}#attBody td{grid-template-columns:88px minmax(0,1fr)}#attBody td:nth-child(1)::before{content:'이름'}#attBody td:nth-child(2)::before{content:'역할'}#attBody td:nth-child(3)::before{content:'참여'}#attBody td:nth-child(4)::before{content:'예배'}#attBody td:nth-child(5)::before{content:'셀 모임'}#attBody td:nth-child(6)::before{content:'장기결석'}#attBody td:nth-child(n+1)::before{font-size:11px;font-weight:800;color:var(--muted)}#attBody td:nth-child(3),#attBody td:nth-child(4),#attBody td:nth-child(5),#attBody td:nth-child(6){white-space:normal}#attBody .actions{grid-template-columns:repeat(3,minmax(66px,1fr))}}
'''

old_att_table = '<div class="card s12"><div class="table"><table><thead><tr><th>이름</th><th>역할</th><th>출석 상태</th><th>장기결석</th></tr></thead><tbody id="attBody"><tr><td colspan="4">셀을 선택해주세요.</td></tr></tbody></table></div></div>'
new_att_table = '<div class="card s12"><div class="table"><table><thead><tr><th>이름</th><th>역할</th><th>참여 유형</th><th>예배 출석</th><th>셀 모임 출석</th><th>장기결석</th></tr></thead><tbody id="attBody"><tr><td colspan="6">셀을 선택해주세요.</td></tr></tbody></table></div></div>'

old_cell_form = '<div class="card s4"><h3 id="cellFormTitle">새 셀 등록</h3><div class="muted">새 셀을 만들거나, 오른쪽 등록된 셀의 수정 버튼을 눌러 기존 셀 명단을 변경하세요.</div><label>셀 이름</label><input id="cellName"><label>리더</label><input id="leader"><label>헬퍼</label><input id="helper"><label>셀원</label><textarea id="members" rows="7" placeholder="한 줄에 한 명"></textarea><button id="addCell" class="primary w100">새 셀 저장</button><button id="cancelCellEdit" class="soft w100 hidden">수정 취소</button></div>'
new_cell_form = '<div class="card s4"><h3 id="cellFormTitle">새 셀 등록</h3><div class="muted">셀원별로 예배+셀 / 예배만 / 셀만 / 출석관리 제외를 지정하고 비고를 기록할 수 있습니다.</div><label>셀 이름</label><input id="cellName"><label>리더</label><input id="leader"><label>헬퍼</label><input id="helper"><label>셀원</label><div id="memberEditor" class="member-editor"></div><button id="addMemberRow" class="soft w100" type="button">+ 셀원 추가</button><button id="addCell" class="primary w100">새 셀 저장</button><button id="cancelCellEdit" class="soft w100 hidden">수정 취소</button></div>'

old_helpers = r'''function memberNames(c){
 const m=c?.members;
 if(Array.isArray(m))return m.map(x=>typeof x==="string"?x:(x?.name||"")).map(String).filter(Boolean);
 if(typeof m==="string")return m.split(/\n|,/).map(x=>x.trim()).filter(Boolean);
 if(m&&typeof m==="object")return Object.values(m).map(x=>typeof x==="string"?x:(x?.name||"")).map(String).filter(Boolean);
 return[];
}
function people(c){
 const out=[];
 if(c?.leader)out.push({name:String(c.leader),role:"리더"});
 if(c?.helper)out.push({name:String(c.helper),role:"헬퍼"});
 memberNames(c).forEach(name=>out.push({name,role:"셀원"}));
 return out;
}'''
new_helpers = r'''const PARTICIPATIONS=["both","worship","cell","inactive"];
const participationLabel=v=>({both:"예배+셀",worship:"예배만",cell:"셀만",inactive:"출석관리 제외"}[v]||"예배+셀");
function normalizeMember(x){
 if(typeof x==="string")return{name:x.trim(),participation:"both",note:""};
 if(!x||typeof x!=="object")return{name:"",participation:"both",note:""};
 const participation=PARTICIPATIONS.includes(x.participation)?x.participation:"both";
 return{name:String(x.name||"").trim(),participation,note:String(x.note||"").trim()};
}
function memberEntries(c){
 const m=c?.members;
 if(Array.isArray(m))return m.map(normalizeMember).filter(x=>x.name);
 if(typeof m==="string")return m.split(/\n|,/).map(x=>normalizeMember(x)).filter(x=>x.name);
 if(m&&typeof m==="object")return Object.values(m).map(normalizeMember).filter(x=>x.name);
 return[];
}
function memberNames(c){return memberEntries(c).map(x=>x.name)}
function people(c){
 const out=[];
 if(c?.leader)out.push({name:String(c.leader),role:"리더",participation:"both",note:""});
 if(c?.helper)out.push({name:String(c.helper),role:"헬퍼",participation:"both",note:""});
 memberEntries(c).forEach(m=>out.push({...m,role:"셀원"}));
 return out;
}
const trackEnabled=(p,track)=>p.participation==="both"||p.participation===track;
function normalizeRecord(v){
 if(typeof v==="string")return{worship:v,cell:v};
 if(v&&typeof v==="object")return{worship:v.worship||"",cell:v.cell||""};
 return{worship:"",cell:""};
}'''

new_cell_management = r'''let editingCellId="";
function memberRowHtml(m={}){
 const x=normalizeMember(m),opts=PARTICIPATIONS.map(v=>`<option value="${v}" ${x.participation===v?"selected":""}>${participationLabel(v)}</option>`).join("");
 return `<div class="member-row"><input data-member-name placeholder="이름" value="${esc(x.name)}"><select data-member-part>${opts}</select><input data-member-note placeholder="비고 / 사유" value="${esc(x.note)}"><button type="button" class="danger" data-member-remove>삭제</button></div>`;
}
function renderMemberEditor(list=[]){
 $("memberEditor").innerHTML=list.map(memberRowHtml).join("");
 if(!list.length)$("memberEditor").insertAdjacentHTML("beforeend",memberRowHtml());
}
function collectMembers(){
 const out=[],seen=new Set();
 $("memberEditor").querySelectorAll(".member-row").forEach(row=>{
  const name=row.querySelector("[data-member-name]").value.trim();if(!name)return;
  const key=name.toLowerCase();if(seen.has(key))return;seen.add(key);
  out.push({name,participation:row.querySelector("[data-member-part]").value,note:row.querySelector("[data-member-note]").value.trim()});
 });
 return out;
}
$("addMemberRow").onclick=()=>$("memberEditor").insertAdjacentHTML("beforeend",memberRowHtml());
$("memberEditor").addEventListener("click",e=>{const b=e.target.closest("[data-member-remove]");if(b)b.closest(".member-row")?.remove()});
function resetCellForm(){
 editingCellId="";
 $("cellName").value=$("leader").value=$("helper").value="";
 renderMemberEditor([]);
 $("cellName").disabled=$("leader").disabled=$("helper").disabled=false;
 if(isAdmin()){
  $("cellFormTitle").textContent="새 셀 등록";
  $("addCell").textContent="새 셀 저장";
  $("addCell").classList.remove("hidden");
 }else{
  $("cellFormTitle").textContent="내 셀 명단 관리";
  $("addCell").textContent="셀원 명단 저장";
  $("addCell").classList.add("hidden");
 }
 $("cancelCellEdit").classList.add("hidden");
}
function editCell(id){
 const c=cells.find(x=>x.id===id);if(!c)return;
 if(!isAdmin()&&id!==profile?.cellId)return;
 editingCellId=id;
 $("cellName").value=c.name||"";
 $("leader").value=c.leader||"";
 $("helper").value=c.helper||"";
 renderMemberEditor(memberEntries(c));
 $("cellName").disabled=$("leader").disabled=$("helper").disabled=!isAdmin();
 $("cellFormTitle").textContent=isAdmin()?`${c.name||"셀"} 수정`:`${c.name||"셀"} 셀원 관리`;
 $("addCell").textContent=isAdmin()?"변경사항 저장":"셀원 명단 저장";
 $("addCell").classList.remove("hidden");
 $("cancelCellEdit").classList.remove("hidden");
 $("memberEditor").scrollIntoView({behavior:"smooth",block:"center"});
}
function memberSummary(c){
 const ms=memberEntries(c);if(!ms.length)return '<div class="muted">등록된 셀원이 없습니다.</div>';
 return `<div class="member-summary">${ms.map(m=>`<div class="member-summary-row"><b>${esc(m.name)}</b><span class="part-badge">${participationLabel(m.participation)}</span><span>${m.note?`비고: ${esc(m.note)}`:'<span class="muted">비고 없음</span>'}</span></div>`).join("")}</div>`;
}
function renderCells(){
 const box=$("cellList");
 if(!cells.length){box.innerHTML='<div class="muted">등록된 셀이 없습니다.</div>';return}
 box.innerHTML=cells.map(c=>`<div class="cell"><div class="celltop"><div><b>${esc(c.name)}</b><div class="muted">리더 ${esc(c.leader||"-")} · 헬퍼 ${esc(c.helper||"-")} · ${people(c).length}명</div></div>${(isAdmin()||canEdit())?`<div class="actions"><button class="soft" data-edit="${esc(c.id)}">${isAdmin()?"수정":"셀원 관리"}</button>${isAdmin()?`<button class="danger" data-del="${esc(c.id)}">삭제</button>`:""}</div>`:""}</div>${(isAdmin()||canEdit())?`<details class="roster"><summary>셀원 참여 유형 / 비고 보기</summary>${memberSummary(c)}</details>`:""}</div>`).join("");
 box.querySelectorAll("[data-edit]").forEach(b=>b.onclick=()=>editCell(b.dataset.edit));
 box.querySelectorAll("[data-del]").forEach(b=>b.onclick=async()=>{if(confirm("삭제할까요?")){await deleteDoc(doc(db,"cells",b.dataset.del));if(editingCellId===b.dataset.del)resetCellForm()}});
}
function renderCellSelect(){'''

new_attendance = r'''function statusButtons(track,state,disabled){
 const wrap=document.createElement("div");wrap.className="actions";
 [["present","출석","p"],["late","지각","l"],["absent","결석","a"]].forEach(([val,label,cls])=>{
  const b=document.createElement("button");b.type="button";b.className=`att ${cls}${state===val?" on":""}`;b.textContent=label;b.dataset.track=track;b.dataset.state=val;b.disabled=disabled;wrap.appendChild(b);
 });return wrap;
}
function renderAttendance(){
 const body=$("attBody"),c=cells.find(x=>x.id===selectedCellId),date=$("attDate").value;
 if(!c){body.innerHTML='<tr><td colspan="6">셀을 선택해주세요.</td></tr>';return}
 try{
  const ppl=people(c),rec=attendance[attId(date,c.id)]?.records||{},ls=knownLongSet(c),editable=canEdit();
  body.innerHTML="";
  if(!ppl.length){body.innerHTML='<tr><td colspan="6">등록된 인원이 없습니다.</td></tr>';return}
  const frag=document.createDocumentFragment();
  ppl.forEach((p,i)=>{
   const k=personKey(p,i),r=normalizeRecord(rec[k]),isLong=ls.has(k),tr=document.createElement("tr");
   tr.dataset.k=k;tr.dataset.worship=isLong?"":r.worship;tr.dataset.cellstate=isLong?"":r.cell;tr.dataset.cell=c.id;if(isLong)tr.className="longrow";
   const tdName=document.createElement("td"),tdRole=document.createElement("td"),tdPart=document.createElement("td"),tdW=document.createElement("td"),tdC=document.createElement("td"),tdLong=document.createElement("td");
   const strong=document.createElement("b");strong.textContent=p.name;tdName.appendChild(strong);tdRole.textContent=p.role;
   tdPart.innerHTML=`<span class="part-badge">${participationLabel(p.participation)}</span>`;
   if(trackEnabled(p,"worship"))tdW.appendChild(statusButtons("worship",r.worship,!editable||isLong));else tdW.innerHTML='<span class="na">해당 없음</span>';
   if(trackEnabled(p,"cell"))tdC.appendChild(statusButtons("cell",r.cell,!editable||isLong));else tdC.innerHTML='<span class="na">해당 없음</span>';
   const lb=document.createElement("button");lb.type="button";lb.className=`att x${isLong?" on":""}`;lb.textContent=isLong?"장기결석 해제":"장기결석";lb.dataset.long="1";lb.disabled=!editable;tdLong.appendChild(lb);
   tr.append(tdName,tdRole,tdPart,tdW,tdC,tdLong);frag.appendChild(tr);
  });body.appendChild(frag);
 }catch(e){console.error("renderAttendance",e);body.innerHTML='<tr><td colspan="6" class="error">셀 목록 표시 오류</td></tr>';$("attMsg").textContent="오류: "+(e?.message||e)}
}

$("attBody").addEventListener("click",async e=>{
 const b=e.target.closest("button");if(!b||b.disabled||!canEdit())return;
 const tr=b.closest("tr[data-k]");if(!tr)return;
 if(b.dataset.state&&b.dataset.track){
  const prop=b.dataset.track==="worship"?"worship":"cellstate",same=tr.dataset[prop]===b.dataset.state;
  tr.dataset[prop]=same?"":b.dataset.state;
  tr.querySelectorAll(`[data-track="${b.dataset.track}"]`).forEach(x=>x.classList.remove("on"));if(!same)b.classList.add("on");return;
 }
 if(b.dataset.long){
  const c=cells.find(x=>x.id===tr.dataset.cell);if(!c)return;
  const set=new Set(Array.isArray(c.longAbsentKeys)?c.longAbsentKeys:[]),k=tr.dataset.k;
  set.has(k)?set.delete(k):set.add(k);b.disabled=true;
  try{await updateDoc(doc(db,"cells",c.id),{longAbsentKeys:[...set],longAbsentUpdatedAt:Date.now(),longAbsentUpdatedBy:currentUser?.email||""})}
  catch(err){b.disabled=false;alert("장기결석 저장 실패: "+(err.code||err.message))}
 }
});
$("allPresent").onclick=()=>{if(!canEdit())return;const c=cells.find(x=>x.id===selectedCellId);if(!c)return;const ppl=people(c);document.querySelectorAll("#attBody tr[data-k]").forEach((tr,i)=>{if(tr.classList.contains("longrow"))return;const p=ppl[i];["worship","cell"].forEach(track=>{if(!trackEnabled(p,track))return;const prop=track==="worship"?"worship":"cellstate";tr.dataset[prop]="present";tr.querySelectorAll(`[data-track="${track}"]`).forEach(x=>x.classList.remove("on"));tr.querySelector(`[data-track="${track}"][data-state="present"]`)?.classList.add("on")})})};
$("saveAtt").onclick=async()=>{
 const c=cells.find(x=>x.id===selectedCellId),date=$("attDate").value;if(!c||!date||!canEdit())return;
 const records={};document.querySelectorAll("#attBody tr[data-k]").forEach(tr=>records[tr.dataset.k]=tr.classList.contains("longrow")?{worship:"",cell:""}:{worship:tr.dataset.worship||"",cell:tr.dataset.cellstate||""});
 try{await setDoc(doc(db,"attendance",attId(date,c.id)),{date,cellId:c.id,cellName:c.name,records,attendanceVersion:2,updatedAt:Date.now(),updatedBy:currentUser?.email||""});$("attMsg").innerHTML='<span class="ok">예배 / 셀 모임 출석 저장 완료</span>'}
 catch(e){$("attMsg").innerHTML='<span class="error">출석 저장 실패: '+esc(e.code||e.message)+'</span>'}
};

function cellStatus'''

new_dashboard = r'''function trackStatus(c,date,track){
 const ppl=people(c),ls=knownLongSet(c),rec=attendance[attId(date,c.id)]?.records||{};
 const names={present:[],late:[],absent:[],missing:[]};let p=0,l=0,a=0,m=0,eligible=0;
 const displayName=person=>person.role==="셀원"?person.name:`${person.name} (${person.role})`;
 ppl.forEach((person,i)=>{const k=personKey(person,i);if(ls.has(k)||!trackEnabled(person,track))return;eligible++;const state=normalizeRecord(rec[k])[track],name=displayName(person);if(state==="present"){p++;names.present.push(name)}else if(state==="late"){l++;names.late.push(name)}else if(state==="absent"){a++;names.absent.push(name)}else{m++;names.missing.push(name)}});
 return{p,l,a,m,eligible,rate:eligible?Math.round(p/eligible*100):0,names};
}
function cellStatus(c,date){
 const ppl=people(c),ls=knownLongSet(c),long=[];ppl.forEach((person,i)=>{if(ls.has(personKey(person,i)))long.push(person.role==="셀원"?person.name:`${person.name} (${person.role})`)});
 return{total:ppl.length,long,worship:trackStatus(c,date,"worship"),cell:trackStatus(c,date,"cell"),has:!!attendance[attId(date,c.id)]};
}
function nameChips(list){return list.length?list.map(n=>`<span class="name-chip">${esc(n)}</span>`).join(""):'<span class="roster-empty">없음</span>'}
function statusGroups(s){return `<div class="roster-grid"><div class="roster-group"><div class="roster-title p">출석 ${s.p}</div><div class="name-list">${nameChips(s.names.present)}</div></div><div class="roster-group"><div class="roster-title l">지각 ${s.l}</div><div class="name-list">${nameChips(s.names.late)}</div></div><div class="roster-group"><div class="roster-title a">결석 ${s.a}</div><div class="name-list">${nameChips(s.names.absent)}</div></div><div class="roster-group"><div class="roster-title m">미체크 ${s.m}</div><div class="name-list">${nameChips(s.names.missing)}</div></div></div>`}
function renderDash(){
 const date=$("dashDate").value||today();$("nPeople").textContent=cells.reduce((n,c)=>n+people(c).length,0);$("nCells").textContent=cells.length;
 let WP=0,WE=0,CP=0,CE=0;cells.forEach(c=>{const s=cellStatus(c,date);WP+=s.worship.p;WE+=s.worship.eligible;CP+=s.cell.p;CE+=s.cell.eligible});
 const wr=WE?Math.round(WP/WE*100):0,cr=CE?Math.round(CP/CE*100):0;$("rate").classList.add("dual-rate");$("rate").textContent=`예배 ${WE?wr+"%":"-"} · 셀 ${CE?cr+"%":"-"}`;$("rateNote").textContent=`${date} · 예배 대상 ${WE}명 / 출석 ${WP}명 · 셀 대상 ${CE}명 / 출석 ${CP}명`;
 $("summary").innerHTML=cells.length?cells.map(c=>{const s=cellStatus(c,date);return `<div class="cell"><div class="celltop"><div><b>${esc(c.name)}</b><div class="muted">전체 ${s.total}명 · 장기결석 ${s.long.length}명</div></div><div><b style="color:var(--p)">예배 ${s.worship.eligible?s.worship.rate+"%":"-"}</b><br><b style="color:var(--purple)">셀 ${s.cell.eligible?s.cell.rate+"%":"-"}</b></div></div><div class="metrics"><span class="metric mp">예배 출석 ${s.worship.p}/${s.worship.eligible}</span><span class="metric mp">셀 출석 ${s.cell.p}/${s.cell.eligible}</span><span class="metric mx">장기결석 ${s.long.length}</span></div><details class="roster" open><summary>예배 출석 명단</summary>${statusGroups(s.worship)}</details><details class="roster"><summary>셀 모임 출석 명단</summary>${statusGroups(s.cell)}</details>${s.long.length?`<div class="status-section"><div class="status-section-title">장기결석</div><div class="name-list">${nameChips(s.long)}</div></div>`:""}</div>`}).join(""):'<div class="muted">표시할 셀이 없습니다.</div>';
}

$("addCell").onclick'''

new_addcell = r'''$("addCell").onclick=async()=>{
 const members=collectMembers();
 if(!isAdmin()){
  if(!canEdit()||!editingCellId||editingCellId!==profile?.cellId)return alert("자신의 셀원 명단만 수정할 수 있습니다.");
  try{await updateDoc(doc(db,"cells",editingCellId),{members,updatedAt:Date.now()});alert("셀원 참여 유형과 비고가 저장되었습니다.");resetCellForm()}
  catch(e){console.error(e);alert("셀원 저장 실패: "+(e.code||e.message||e))}return;
 }
 const cellName=$("cellName").value.trim();if(!cellName)return alert("셀 이름을 입력해주세요.");
 const data={name:cellName,leader:$("leader").value.trim(),helper:$("helper").value.trim(),members,updatedAt:Date.now()};
 try{if(editingCellId){await updateDoc(doc(db,"cells",editingCellId),data);alert("기존 셀이 수정되었습니다.")}else{await addDoc(collection(db,"cells"),{...data,longAbsentKeys:[],createdAt:Date.now()});alert("새 셀이 등록되었습니다.")}resetCellForm()}
 catch(e){console.error(e);alert("셀 저장 실패: "+(e.code||e.message||e))}
};'''

new_sync = r'''async function syncUserToCell(user,newRole,newCellId){
 const name=(user?.name||"").trim();if(!name)return;
 const oldRole=user?.role||"pending",oldCellId=user?.cellId||"",touched=new Set([oldCellId,newCellId].filter(Boolean));
 for(const cellId of touched){
  const c=cells.find(x=>x.id===cellId);if(!c)continue;
  let leader=String(c.leader||""),helper=String(c.helper||""),members=memberEntries(c);
  if(cellId===oldCellId){if(oldRole==="leader"&&leader===name)leader="";if(oldRole==="helper"&&helper===name)helper="";if(oldRole==="member")members=members.filter(x=>x.name!==name)}
  if(cellId===newCellId){members=members.filter(x=>x.name!==name);if(newRole==="leader")leader=name;else if(newRole==="helper")helper=name;else if(newRole==="member")members.push({name,participation:"both",note:""})}
  const seen=new Set(),dedup=members.filter(m=>{const k=m.name.toLowerCase();if(!m.name||seen.has(k))return false;seen.add(k);return true});
  await updateDoc(doc(db,"cells",cellId),{leader,helper,members:dedup,updatedAt:Date.now()});
 }
}'''

new_csv = r'''$("csv").onclick=()=>{
 let rows=[["날짜","셀","역할","이름","참여유형","비고","예배상태","셀모임상태","장기결석"]];const vals=Object.values(attendance).sort((a,b)=>(a.date||"").localeCompare(b.date||""));
 if(vals.length)vals.forEach(a=>{const c=cells.find(x=>x.id===a.cellId);if(!c)return;const ls=knownLongSet(c);people(c).forEach((p,i)=>{const k=personKey(p,i),r=normalizeRecord(a.records?.[k]);rows.push([a.date,c.name,p.role,p.name,participationLabel(p.participation),p.note||"",r.worship,r.cell,ls.has(k)?"Y":""])})});
 else cells.forEach(c=>{const ls=knownLongSet(c);people(c).forEach((p,i)=>rows.push(["",c.name,p.role,p.name,participationLabel(p.participation),p.note||"","","",ls.has(personKey(p,i))?"Y":""]))});
 const csv="\ufeff"+rows.map(r=>r.map(v=>`"${String(v??"").replaceAll('"','""')}"`).join(",")).join("\n"),url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"})),a=document.createElement("a");a.href=url;a.download="청년부_예배_셀출석.csv";a.click();URL.revokeObjectURL(url);
};'''

def sub_once(s, pattern, repl, label):
    out, n = re.subn(pattern, repl, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out

for path in FILES:
    s = path.read_text(encoding='utf-8')
    if 'attendance-types-20260910' in s:
        continue
    if old_att_table not in s or old_cell_form not in s or old_helpers not in s:
        raise SystemExit(f'expected base blocks not found in {path}')
    s = s.replace(old_att_table, new_att_table, 1)
    s = s.replace(old_cell_form, new_cell_form, 1)
    s = s.replace('<div class="card s4"><div class="muted">선택 날짜 출석률</div><div id="rate" class="stat">-</div>', '<div class="card s4"><div class="muted">선택 날짜 예배 / 셀 출석률</div><div id="rate" class="stat">-</div>', 1)
    s = s.replace('</style>', CSS + '\n</style>', 1)
    s = s.replace(old_helpers, new_helpers, 1)
    s = sub_once(s, r'let editingCellId="";.*?\nfunction renderCellSelect\(\)\{', new_cell_management, 'cell management')
    s = sub_once(s, r'function renderAttendance\(\)\{.*?\nfunction cellStatus', new_attendance, 'attendance')
    s = sub_once(s, r'function cellStatus\(c,date\)\{.*?\n\$\("addCell"\)\.onclick', new_dashboard, 'dashboard')
    s = sub_once(s, r'\$\("addCell"\)\.onclick=async\(\)=>\{.*?\n\};\n\$\("cancelCellEdit"\)\.onclick=resetCellForm;', new_addcell + '\n$("cancelCellEdit").onclick=resetCellForm;', 'cell save')
    s = sub_once(s, r'async function syncUserToCell\(user,newRole,newCellId\)\{.*?\n\}\n\nfunction renderUsers', new_sync + '\n\nfunction renderUsers', 'user sync')
    s = sub_once(s, r'\$\("csv"\)\.onclick=\(\)=>\{.*?\n\};\n\nrenderCells\(\);', new_csv + '\n\nrenderCells();', 'csv')
    path.write_text(s, encoding='utf-8')
