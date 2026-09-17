from pathlib import Path

files = [Path('index.html'), Path('app-v4.html')]
for path in files:
    text = path.read_text(encoding='utf-8')

    # Keep the quick attendance button as a simple toggle on each tap.
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
    new_quick = '''if(b.dataset.quick){
  const enabled=["worship","cell"].filter(track=>trackEnabled(p,track));
  const alreadyPresent=enabled.length>0&&enabled.every(track=>(track==="worship"?tr.dataset.worship:tr.dataset.cellstate)==="present");
  enabled.forEach(track=>setTrackState(tr,track,alreadyPresent?"":"present"));
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    if old_quick in text:
        text = text.replace(old_quick, new_quick, 1)

    # Auth behavior:
    # - refresh: keep the login
    # - close the tab/window: session login disappears automatically
    # - navigate away and later return in the same tab: sign out
    text = text.replace(
        'getAuth,setPersistence,inMemoryPersistence,',
        'getAuth,setPersistence,browserSessionPersistence,'
    )

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
    elif 'browserSessionPersistence' in text and 'youthAttendanceLeft' not in text:
        marker = 'try{await setPersistence(auth,browserSessionPersistence)}catch(e){console.error("auth persistence",e)}'
        if marker in text:
            text = text.replace(marker, new_persistence, 1)
    elif 'browserSessionPersistence' not in text:
        raise SystemExit(f'Could not update auth persistence in {path}')

    path.write_text(text, encoding='utf-8')
