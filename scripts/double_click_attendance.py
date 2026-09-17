from pathlib import Path

files = [Path('index.html'), Path('app-v4.html')]

button_css = '''
/* button-feedback-20260917 */
button{
  transition:transform .12s ease,box-shadow .18s ease,filter .18s ease,background-color .18s ease,border-color .18s ease,color .18s ease,opacity .18s ease;
  -webkit-tap-highlight-color:transparent;
  transform-origin:center;
}
button:not(:disabled){cursor:pointer}
@media(hover:hover){
  button:not(:disabled):hover{transform:translateY(-1px);box-shadow:0 5px 14px rgba(16,24,40,.12);filter:brightness(1.015)}
}
button:not(:disabled):active{transform:scale(.97);box-shadow:0 2px 6px rgba(16,24,40,.14);filter:brightness(.96);transition-duration:.06s}
button:focus-visible{outline:3px solid rgba(54,91,220,.28);outline-offset:2px}
button:disabled{opacity:.52!important;cursor:not-allowed!important;transform:none!important;box-shadow:none!important;filter:none!important}
.quick-present.on,#allPresent.toggle-on{background:var(--green)!important;color:#fff!important;border-color:var(--green)!important;box-shadow:0 0 0 3px rgba(22,132,90,.14)}
.tab.active{transform:translateY(0)}
@media(prefers-reduced-motion:reduce){button{transition:none!important}}
'''

for path in files:
    text = path.read_text(encoding='utf-8')

    # Keep quick attendance as a simple one-tap toggle.
    text = text.replace(
        '출석 버튼을 빠르게 두 번 누르면 해당 체크가 해제됩니다. 출석 버튼을 빠르게 두 번 누르면 해당 체크가 해제됩니다.',
        '출석 버튼을 한 번 더 누르면 체크가 해제됩니다.'
    )
    text = text.replace(
        '출석 버튼을 빠르게 두 번 누르면 해당 체크가 해제됩니다.',
        '출석 버튼을 한 번 더 누르면 체크가 해제됩니다.'
    )

    old_quick = '''if(b.dataset.quick){
  const now=Date.now(),last=Number(b.dataset.lastQuickTap||0),isDouble=now-last<360;
  b.dataset.lastQuickTap=isDouble?"0":String(now);
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,isDouble?"":"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    simple_quick = '''if(b.dataset.quick){
  const enabled=["worship","cell"].filter(track=>trackEnabled(p,track));
  const alreadyPresent=enabled.length>0&&enabled.every(track=>(track==="worship"?tr.dataset.worship:tr.dataset.cellstate)==="present");
  enabled.forEach(track=>setTrackState(tr,track,alreadyPresent?"":"present"));
  updateRowSummary(tr,p,false);syncAllPresentButton();tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    current_quick = '''if(b.dataset.quick){
  const enabled=["worship","cell"].filter(track=>trackEnabled(p,track));
  const alreadyPresent=enabled.length>0&&enabled.every(track=>(track==="worship"?tr.dataset.worship:tr.dataset.cellstate)==="present");
  enabled.forEach(track=>setTrackState(tr,track,alreadyPresent?"":"present"));
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    if old_quick in text:
        text = text.replace(old_quick, simple_quick, 1)
    elif current_quick in text:
        text = text.replace(current_quick, simple_quick, 1)

    # Update the help text to explain both toggles.
    text = text.replace(
        '출석 버튼을 한 번 더 누르면 체크가 해제됩니다.',
        '출석 버튼을 한 번 더 누르면 체크가 해제됩니다. 전체 출석도 한 번 더 누르면 전체 체크가 해제됩니다.',
        1
    )

    # Global button interaction effects.
    if '/* button-feedback-20260917 */' not in text:
        text = text.replace('</style>', button_css + '\n</style>', 1)

    # Quick button selected-state feedback.
    old_update = '''function updateRowSummary(tr,p,isLong=false){
 const el=tr.querySelector("[data-status-summary]");if(!el)return;
 el.textContent=statusSummaryText(p,tr,isLong);
 const complete=isLong||["worship","cell"].filter(t=>trackEnabled(p,t)).every(t=>["present","late","absent"].includes(tr.dataset[t==="worship"?"worship":"cellstate"]||""));
 el.classList.toggle("done",complete&&!isLong);el.classList.toggle("long",isLong||p.participation==="long");
}
'''
    new_update = '''function updateRowSummary(tr,p,isLong=false){
 const el=tr.querySelector("[data-status-summary]");if(!el)return;
 el.textContent=statusSummaryText(p,tr,isLong);
 const complete=isLong||["worship","cell"].filter(t=>trackEnabled(p,t)).every(t=>["present","late","absent"].includes(tr.dataset[t==="worship"?"worship":"cellstate"]||""));
 el.classList.toggle("done",complete&&!isLong);el.classList.toggle("long",isLong||p.participation==="long");
 const quick=tr.querySelector("[data-quick]");
 if(quick){
  const enabled=["worship","cell"].filter(t=>trackEnabled(p,t));
  const on=enabled.length>0&&enabled.every(t=>(t==="worship"?tr.dataset.worship:tr.dataset.cellstate)==="present");
  quick.classList.toggle("on",on);quick.setAttribute("aria-pressed",on?"true":"false");
 }
}
'''
    if old_update in text:
        text = text.replace(old_update, new_update, 1)

    # Add helpers that determine whether every eligible row is already present.
    helper_anchor = '''function quickButtonLabel(p){
 if(p.participation==="worship")return"✓ 예배 출석";
 if(p.participation==="cell")return"✓ 셀 모임 출석";
 return"✓ 출석";
}
'''
    helpers = helper_anchor + '''function allAttendancePresent(){
 const c=cells.find(x=>x.id===selectedCellId);if(!c)return false;
 const ppl=people(c);let eligible=0,all=true;
 document.querySelectorAll("#attBody tr[data-k]").forEach((tr,i)=>{
  if(tr.classList.contains("longrow"))return;
  const p=ppl[i];if(!p)return;
  const tracks=["worship","cell"].filter(t=>trackEnabled(p,t));
  tracks.forEach(t=>{eligible++;if((t==="worship"?tr.dataset.worship:tr.dataset.cellstate)!=="present")all=false});
 });
 return eligible>0&&all;
}
function syncAllPresentButton(){
 const b=$("allPresent");if(!b)return;
 const on=allAttendancePresent();
 b.classList.toggle("toggle-on",on);b.setAttribute("aria-pressed",on?"true":"false");b.textContent=on?"전체 출석 해제":"전체 출석";
}
'''
    if 'function allAttendancePresent(){' not in text and helper_anchor in text:
        text = text.replace(helper_anchor, helpers, 1)

    # Keep the top toggle in sync whenever attendance is rendered.
    text = text.replace(
        "if(!c){body.innerHTML='<tr><td colspan=\"6\">셀을 선택해주세요.</td></tr>';return}",
        "if(!c){body.innerHTML='<tr><td colspan=\"6\">셀을 선택해주세요.</td></tr>';syncAllPresentButton();return}",
        1
    )
    text = text.replace(
        "if(!ppl.length){body.innerHTML='<tr><td colspan=\"6\">등록된 인원이 없습니다.</td></tr>';return}",
        "if(!ppl.length){body.innerHTML='<tr><td colspan=\"6\">등록된 인원이 없습니다.</td></tr>';syncAllPresentButton();return}",
        1
    )
    text = text.replace('  });body.appendChild(frag);\n', '  });body.appendChild(frag);syncAllPresentButton();\n', 1)

    # Detail status toggles should also update the overall button state.
    text = text.replace(
        'setTrackState(tr,b.dataset.track,same?"":b.dataset.state);updateRowSummary(tr,p,false);return;',
        'setTrackState(tr,b.dataset.track,same?"":b.dataset.state);updateRowSummary(tr,p,false);syncAllPresentButton();return;',
        1
    )

    old_all = '$("allPresent").onclick=()=>{if(!canEdit())return;const c=cells.find(x=>x.id===selectedCellId);if(!c)return;const ppl=people(c);document.querySelectorAll("#attBody tr[data-k]").forEach((tr,i)=>{if(tr.classList.contains("longrow"))return;const p=ppl[i];["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,"present")});updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open")})};'
    new_all = '''$("allPresent").onclick=()=>{
 if(!canEdit())return;const c=cells.find(x=>x.id===selectedCellId);if(!c)return;
 const ppl=people(c),clear=allAttendancePresent();
 document.querySelectorAll("#attBody tr[data-k]").forEach((tr,i)=>{
  if(tr.classList.contains("longrow"))return;const p=ppl[i];if(!p)return;
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,clear?"":"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");
 });
 syncAllPresentButton();
};'''
    if old_all in text:
        text = text.replace(old_all, new_all, 1)

    # Preserve the requested auth behavior from the previous revision.
    text = text.replace('getAuth,setPersistence,inMemoryPersistence,','getAuth,setPersistence,browserSessionPersistence,')
    old_persistence = 'try{await setPersistence(auth,inMemoryPersistence)}catch(e){console.error("auth persistence",e)}'
    new_persistence = '''try{
 await setPersistence(auth,browserSessionPersistence);
 const navType=performance.getEntriesByType("navigation")[0]?.type||"navigate";
 const leftBefore=sessionStorage.getItem("youthAttendanceLeft")==="1";
 if(leftBefore&&navType!=="reload")await signOut(auth);
 sessionStorage.removeItem("youthAttendanceLeft");
}catch(e){console.error("auth persistence",e)}
window.addEventListener("pagehide",()=>{
 try{sessionStorage.setItem("youthAttendanceLeft","1")}catch{}
});
window.addEventListener("pageshow",e=>{
 if(!e.persisted)return;
 try{
  if(sessionStorage.getItem("youthAttendanceLeft")==="1"){
   sessionStorage.removeItem("youthAttendanceLeft");
   signOut(auth);
  }
 }catch{}
});'''
    if old_persistence in text:
        text = text.replace(old_persistence, new_persistence, 1)

    path.write_text(text, encoding='utf-8')
