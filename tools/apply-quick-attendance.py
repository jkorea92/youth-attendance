from pathlib import Path
import re

files = [Path('index.html'), Path('app-v4.html')]
marker = 'quick-attendance-20260917'

css = r'''

/* quick-attendance-20260917 */
.quick-wrap{display:flex;flex-direction:column;gap:8px;min-width:220px}
.quick-present{width:100%;background:#e9f8f0;color:var(--green);border:1px solid #bce5cf;padding:10px 12px}
.quick-present:hover{filter:brightness(.98)}
.att-detail{border:1px solid var(--line);border-radius:10px;background:#f8fafc;overflow:hidden}
.att-detail>summary{cursor:pointer;list-style:none;padding:9px 11px;font-size:12px;font-weight:900;color:var(--p);text-align:center;user-select:none}
.att-detail>summary::-webkit-details-marker{display:none}
.att-detail[open]>summary{border-bottom:1px solid var(--line);background:#eef2ff}
.detail-tracks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:9px}
.detail-track{min-width:0}
.detail-track .track-title{margin-bottom:5px}
.detail-track .actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:5px;flex-wrap:nowrap}
.detail-track .att{width:100%;min-width:0;padding:8px 4px;font-size:11px}
.status-summary{display:inline-block;font-size:12px;font-weight:800;line-height:1.5;color:#344054;white-space:normal!important}
.status-summary.done{color:var(--green)}
.status-summary.long{color:var(--purple)}
@media(max-width:760px){
  #attBody td:nth-child(4)::before{content:'빠른 체크'!important}
  #attBody td:nth-child(5)::before{content:'현재 상태'!important}
  #attBody td:nth-child(6)::before{content:'장기결석'!important}
  #attBody td:nth-child(4),#attBody td:nth-child(5){white-space:normal!important;align-items:start!important}
  #attBody .quick-wrap{width:100%;min-width:0}
  #attBody .quick-present{width:100%!important;min-width:0!important}
  #attBody .att-detail{width:100%;min-width:0}
  #attBody .detail-tracks{grid-template-columns:minmax(0,1fr)}
  #attBody .detail-track .actions{grid-template-columns:repeat(3,minmax(0,1fr))!important}
  #attBody .detail-track .att{min-width:0!important;width:100%!important;font-size:12px!important;padding:9px 3px!important}
  #attBody .status-summary{width:100%}
}
'''

block = r'''function statusButtons(track,state,disabled){
 const wrap=document.createElement("div");wrap.className="actions";
 [["present","출석","p"],["late","지각","l"],["absent","결석","a"]].forEach(([val,label,cls])=>{
  const b=document.createElement("button");b.type="button";b.className=`att ${cls}${state===val?" on":""}`;b.textContent=label;b.dataset.track=track;b.dataset.state=val;b.disabled=disabled;wrap.appendChild(b);
 });return wrap;
}
function stateLabel(v){return({present:"출석",late:"지각",absent:"결석"}[v]||"미체크")}
function statusSummaryText(p,tr,isLong=false){
 if(isLong||p.participation==="long")return"장기 결석";
 const parts=[];
 if(trackEnabled(p,"worship"))parts.push(`예배 ${stateLabel(tr.dataset.worship||"")}`);
 if(trackEnabled(p,"cell"))parts.push(`셀 ${stateLabel(tr.dataset.cellstate||"")}`);
 return parts.join(" · ")||"해당 없음";
}
function updateRowSummary(tr,p,isLong=false){
 const el=tr.querySelector("[data-status-summary]");if(!el)return;
 el.textContent=statusSummaryText(p,tr,isLong);
 const complete=isLong||["worship","cell"].filter(t=>trackEnabled(p,t)).every(t=>["present","late","absent"].includes(tr.dataset[t==="worship"?"worship":"cellstate"]||""));
 el.classList.toggle("done",complete&&!isLong);el.classList.toggle("long",isLong||p.participation==="long");
}
function setTrackState(tr,track,state){
 const prop=track==="worship"?"worship":"cellstate";tr.dataset[prop]=state;
 tr.querySelectorAll(`[data-track="${track}"]`).forEach(x=>x.classList.toggle("on",x.dataset.state===state));
}
function quickButtonLabel(p){
 if(p.participation==="worship")return"✓ 예배 출석";
 if(p.participation==="cell")return"✓ 셀 모임 출석";
 return"✓ 둘 다 출석";
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
   tr.dataset.k=k;tr.dataset.personIndex=String(i);tr.dataset.worship=isLong?"":r.worship;tr.dataset.cellstate=isLong?"":r.cell;tr.dataset.cell=c.id;if(isLong)tr.className="longrow";
   const tdName=document.createElement("td"),tdRole=document.createElement("td"),tdPart=document.createElement("td"),tdQuick=document.createElement("td"),tdStatus=document.createElement("td"),tdLong=document.createElement("td");
   const strong=document.createElement("b");strong.textContent=p.name;tdName.appendChild(strong);tdRole.textContent=p.role;
   tdPart.innerHTML=`<span class="part-badge">${participationLabel(p.participation)}</span>`;
   const quickWrap=document.createElement("div");quickWrap.className="quick-wrap";
   if(!isLong&&p.participation!=="long"){
    const qb=document.createElement("button");qb.type="button";qb.className="quick-present";qb.textContent=quickButtonLabel(p);qb.dataset.quick="present";qb.disabled=!editable;quickWrap.appendChild(qb);
    const details=document.createElement("details");details.className="att-detail";
    const summary=document.createElement("summary");summary.textContent="세부 수정";details.appendChild(summary);
    const tracks=document.createElement("div");tracks.className="detail-tracks";
    if(trackEnabled(p,"worship")){
      const box=document.createElement("div");box.className="detail-track";box.innerHTML='<div class="track-title">예배</div>';box.appendChild(statusButtons("worship",r.worship,!editable));tracks.appendChild(box);
    }
    if(trackEnabled(p,"cell")){
      const box=document.createElement("div");box.className="detail-track";box.innerHTML='<div class="track-title">셀 모임</div>';box.appendChild(statusButtons("cell",r.cell,!editable));tracks.appendChild(box);
    }
    details.appendChild(tracks);quickWrap.appendChild(details);
   }else quickWrap.innerHTML='<span class="na">장기 결석</span>';
   tdQuick.appendChild(quickWrap);
   const ss=document.createElement("span");ss.dataset.statusSummary="1";ss.className="status-summary";tdStatus.appendChild(ss);
   const managedLong=p.participation==="long";const lb=document.createElement("button");lb.type="button";lb.className=`att x${isLong?" on":""}`;lb.textContent=managedLong?"장기결석":(isLong?"장기결석 해제":"장기결석");lb.dataset.long="1";lb.disabled=!editable||managedLong;tdLong.appendChild(lb);
   tr.append(tdName,tdRole,tdPart,tdQuick,tdStatus,tdLong);updateRowSummary(tr,p,isLong);frag.appendChild(tr);
  });body.appendChild(frag);
 }catch(e){console.error("renderAttendance",e);body.innerHTML='<tr><td colspan="6" class="error">셀 목록 표시 오류</td></tr>';$("attMsg").textContent="오류: "+(e?.message||e)}
}

$("attBody").addEventListener("click",async e=>{
 const b=e.target.closest("button");if(!b||b.disabled||!canEdit())return;
 const tr=b.closest("tr[data-k]");if(!tr)return;
 const c=cells.find(x=>x.id===tr.dataset.cell),p=c?people(c)[Number(tr.dataset.personIndex)]:null;if(!p)return;
 if(b.dataset.quick){
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
 if(b.dataset.state&&b.dataset.track){
  const prop=b.dataset.track==="worship"?"worship":"cellstate",same=tr.dataset[prop]===b.dataset.state;
  setTrackState(tr,b.dataset.track,same?"":b.dataset.state);updateRowSummary(tr,p,false);return;
 }
 if(b.dataset.long){
  if(!c)return;
  const set=new Set(Array.isArray(c.longAbsentKeys)?c.longAbsentKeys:[]),k=tr.dataset.k;
  set.has(k)?set.delete(k):set.add(k);b.disabled=true;
  try{await updateDoc(doc(db,"cells",c.id),{longAbsentKeys:[...set],longAbsentUpdatedAt:Date.now(),longAbsentUpdatedBy:currentUser?.email||""})}
  catch(err){b.disabled=false;alert("장기결석 저장 실패: "+(err.code||err.message))}
 }
});
$("allPresent").onclick=()=>{if(!canEdit())return;const c=cells.find(x=>x.id===selectedCellId);if(!c)return;const ppl=people(c);document.querySelectorAll("#attBody tr[data-k]").forEach((tr,i)=>{if(tr.classList.contains("longrow"))return;const p=ppl[i];["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,"present")});updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open")})};
$("saveAtt").onclick=async()=>{
 const c=cells.find(x=>x.id===selectedCellId),date=$("attDate").value;if(!c||!date||!canEdit())return;
 const records={};document.querySelectorAll("#attBody tr[data-k]").forEach(tr=>records[tr.dataset.k]=tr.classList.contains("longrow")?{worship:"",cell:""}:{worship:tr.dataset.worship||"",cell:tr.dataset.cellstate||""});
 try{await setDoc(doc(db,"attendance",attId(date,c.id)),{date,cellId:c.id,cellName:c.name,records,attendanceVersion:2,updatedAt:Date.now(),updatedBy:currentUser?.email||""});$("attMsg").innerHTML='<span class="ok">예배 / 셀 모임 출석 저장 완료</span>'}
 catch(e){$("attMsg").innerHTML='<span class="error">출석 저장 실패: '+esc(e.code||e.message)+'</span>'}
};

'''

old_head = '<div class="card s12"><h3>출석 체크</h3><div class="row">'
new_head = '<div class="card s12"><h3>출석 체크</h3><div class="muted" style="margin:-4px 0 12px">전체 출석을 먼저 적용한 뒤, 지각·결석 등 예외 인원만 세부 수정하면 빠르게 체크할 수 있습니다.</div><div class="row">'
old_table = '<thead><tr><th>이름</th><th>역할</th><th>참여 유형</th><th>예배 출석</th><th>셀 모임 출석</th><th>장기결석</th></tr></thead>'
new_table = '<thead><tr><th>이름</th><th>역할</th><th>참여 유형</th><th>빠른 체크 / 세부 수정</th><th>현재 상태</th><th>장기결석</th></tr></thead>'

for path in files:
    text = path.read_text(encoding='utf-8')
    if marker not in text:
        text = text.replace('</style>', css + '\n</style>', 1)
    text = text.replace(old_head, new_head, 1)
    text = text.replace(old_table, new_table, 1)
    text, n = re.subn(r'function statusButtons\(track,state,disabled\)\{.*?(?=function trackStatus\(c,date,track\)\{)', block, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'Could not replace attendance block in {path}')
    path.write_text(text, encoding='utf-8')
