from pathlib import Path
import re

files = [Path('index.html'), Path('app-v4.html')]
for path in files:
    text = path.read_text(encoding='utf-8')

    # Keep the quick-attendance instruction concise and remove the previous double-tap wording.
    text = re.sub(
        r'전체 출석을 먼저 적용한 뒤, 지각·결석 등 예외 인원만 세부 수정하면 빠르게 체크할 수 있습니다\.(?: 출석 버튼을 빠르게 두 번 누르면 해당 체크가 해제됩니다\.)*',
        '전체 출석을 먼저 적용한 뒤, 지각·결석 등 예외 인원만 세부 수정하면 빠르게 체크할 수 있습니다. 출석 버튼을 한 번 더 누르면 체크가 해제됩니다.',
        text
    )

    text = text.replace('return"✓ 둘 다 출석";', 'return"✓ 출석";')

    # A single tap now toggles the quick attendance state. If all enabled tracks are
    # already present, the next tap clears them; otherwise it marks them present.
    old_double = '''if(b.dataset.quick){
  const now=Date.now(),last=Number(b.dataset.lastQuickTap||0),isDouble=now-last<360;
  b.dataset.lastQuickTap=isDouble?"0":String(now);
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,isDouble?"":"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    new_toggle = '''if(b.dataset.quick){
  const enabled=["worship","cell"].filter(track=>trackEnabled(p,track));
  const alreadyPresent=enabled.length>0&&enabled.every(track=>(track==="worship"?tr.dataset.worship:tr.dataset.cellstate)==="present");
  enabled.forEach(track=>setTrackState(tr,track,alreadyPresent?"":"present"));
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    if old_double in text:
        text = text.replace(old_double, new_toggle, 1)
    elif 'const alreadyPresent=enabled.length>0' not in text:
        raise SystemExit(f'Could not find quick attendance block in {path}')

    # Firebase Auth should live only in page memory. Navigating away, closing the tab,
    # or refreshing destroys the session so returning through the link requires login.
    old_import = 'import{getAuth,signInWithEmailAndPassword,createUserWithEmailAndPassword,sendPasswordResetEmail,signOut,onAuthStateChanged}from"https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";'
    new_import = 'import{getAuth,setPersistence,inMemoryPersistence,signInWithEmailAndPassword,createUserWithEmailAndPassword,sendPasswordResetEmail,signOut,onAuthStateChanged}from"https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";'
    if 'inMemoryPersistence' not in text:
        if old_import not in text:
            raise SystemExit(f'Could not find Firebase Auth import in {path}')
        text = text.replace(old_import, new_import, 1)

    auth_init = 'const fb=initializeApp(firebaseConfig),auth=getAuth(fb),db=getFirestore(fb),$=id=>document.getElementById(id);'
    persistence_init = auth_init + '\ntry{await setPersistence(auth,inMemoryPersistence)}catch(e){console.error("auth persistence",e)}'
    if 'setPersistence(auth,inMemoryPersistence)' not in text:
        if auth_init not in text:
            raise SystemExit(f'Could not find Firebase auth initialization in {path}')
        text = text.replace(auth_init, persistence_init, 1)

    path.write_text(text, encoding='utf-8')
