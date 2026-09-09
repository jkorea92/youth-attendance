import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, collection, onSnapshot, query, where } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";

export const firebaseConfig = {
  apiKey: "AIzaSyBLQ7I3EO4g5VPnY35WZfNpbf3XvWjKit8",
  authDomain: "youth-attendance-7d46c.firebaseapp.com",
  projectId: "youth-attendance-7d46c",
  storageBucket: "youth-attendance-7d46c.firebasestorage.app",
  messagingSenderId: "210019623751",
  appId: "1:210019623751:web:6b2597c947e1b96c156262"
};

const OWNER_EMAIL = "jaehokorea92@gmail.com";

function injectSignupUI(){
  const loginView=document.getElementById("loginView");
  if(!loginView || document.getElementById("showSignupBtn")) return;

  const intro=loginView.querySelector(".muted");
  if(intro) intro.textContent="기존 계정으로 로그인하거나, 처음 사용하는 경우 계정을 신청하세요.";

  const loginMsg=document.getElementById("loginMsg");
  const wrap=document.createElement("div");
  wrap.innerHTML=`
    <button id="showSignupBtn" class="soft" style="width:100%;margin-top:8px">처음이신가요? 계정 신청</button>
    <div id="signupBox" class="hidden" style="margin-top:16px;padding-top:14px;border-top:1px solid var(--line)">
      <h3 style="margin:0 0 6px">계정 신청</h3>
      <div class="muted">가입 후에는 승인 대기 상태가 되며, 관리자가 역할과 담당 셀을 지정하면 사용할 수 있습니다.</div>
      <label>이름</label><input id="signupName" autocomplete="name" placeholder="예: 홍길동">
      <label>이메일</label><input id="signupEmail" type="email" autocomplete="email">
      <label>비밀번호</label><input id="signupPassword" type="password" autocomplete="new-password" placeholder="6자 이상">
      <label>비밀번호 확인</label><input id="signupPassword2" type="password" autocomplete="new-password">
      <label style="display:flex;align-items:center;gap:7px;font-weight:500;margin-top:8px;cursor:pointer"><input id="showSignupPassword" type="checkbox" style="width:auto;margin:0"> 비밀번호 보기</label>
      <button id="signupBtn" class="primary" style="width:100%;margin-top:12px">계정 만들기</button>
      <button id="cancelSignupBtn" class="soft" style="width:100%;margin-top:8px">취소</button>
      <div id="signupMsg" class="status"></div>
    </div>`;
  loginView.insertBefore(wrap, loginMsg);

  const $=id=>document.getElementById(id);
  $("showSignupBtn").onclick=()=>{
    $("signupBox").classList.remove("hidden");
    $("signupEmail").value=$("email")?.value?.trim()||"";
    $("signupMsg").textContent="";
  };
  $("cancelSignupBtn").onclick=()=>{
    $("signupBox").classList.add("hidden");
    $("signupMsg").textContent="";
  };
  $("showSignupPassword").onchange=()=>{
    const t=$("showSignupPassword").checked?"text":"password";
    $("signupPassword").type=t;
    $("signupPassword2").type=t;
  };

  $("signupBtn").onclick=async()=>{
    const name=$("signupName").value.trim();
    const email=$("signupEmail").value.trim();
    const pw=$("signupPassword").value;
    const pw2=$("signupPassword2").value;
    const msg=$("signupMsg");
    if(!name){msg.textContent="이름을 입력해주세요.";return;}
    if(!email){msg.textContent="이메일을 입력해주세요.";return;}
    if(pw.length<6){msg.textContent="비밀번호는 6자 이상이어야 합니다.";return;}
    if(pw!==pw2){msg.textContent="비밀번호가 일치하지 않습니다.";return;}

    msg.textContent="계정을 만드는 중...";
    try{
      const signupApp=initializeApp(firebaseConfig,"signupApp_"+Date.now());
      const signupAuth=getAuth(signupApp);
      const cred=await createUserWithEmailAndPassword(signupAuth,email,pw);
      const signupDb=getFirestore(signupApp);
      const role=email.toLowerCase()===OWNER_EMAIL?"admin":"pending";
      await setDoc(doc(signupDb,"users",cred.user.uid),{
        email,name,role,cellId:"",createdAt:Date.now(),updatedAt:Date.now()
      });
      await signOut(signupAuth);
      msg.textContent=role==="admin"?"관리자 계정으로 등록되었습니다. 이제 로그인해주세요.":"계정 신청이 완료되었습니다. 관리자가 승인하면 사용할 수 있습니다.";
      $("email").value=email;
      $("signupPassword").value="";
      $("signupPassword2").value="";
    }catch(e){
      console.error("Firebase signup error:",e);
      const code=e?.code||"unknown-error";
      const messages={
        "auth/email-already-in-use":"이미 가입된 이메일입니다. 로그인해주세요.",
        "auth/invalid-email":"이메일 형식을 확인해주세요.",
        "auth/weak-password":"비밀번호는 6자 이상으로 설정해주세요.",
        "auth/operation-not-allowed":"Firebase에서 이메일/비밀번호 가입이 활성화되어 있지 않습니다.",
        "auth/network-request-failed":"네트워크 연결을 확인해주세요.",
        "auth/too-many-requests":"요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
      };
      msg.textContent=`${messages[code]||"계정 생성에 실패했습니다."} (${code})`;
    }
  };

  const usersHelp=document.querySelector("#users p.muted");
  if(usersHelp) usersHelp.textContent="사용자가 로그인 화면의 ‘계정 신청’에서 직접 가입하면 승인 대기로 목록에 나타납니다. 여기서 역할과 담당 셀을 지정하면 사용할 수 있습니다.";
}

function installDashboardAttendance(){
  if(document.getElementById('dashboardAttendanceStyle')) return;
  const style=document.createElement('style');
  style.id='dashboardAttendanceStyle';
  style.textContent=`
    .dash-cell-attendance{display:grid;gap:12px;margin-top:14px}
    .dash-cell-row{border:1px solid #e6eaf0;border-radius:15px;padding:14px 15px;background:#fbfcfe}
    .dash-cell-top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
    .dash-cell-name{font-weight:900;font-size:15px}
    .dash-cell-rate{font-size:21px;font-weight:900;color:#3559db}
    .dash-cell-meta{font-size:11px;color:#98a2b3;margin-top:3px}
    .dash-statuses{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
    .dash-pill{border-radius:999px;padding:5px 9px;font-size:11px;font-weight:800}
    .dash-present{background:#e9f8f0;color:#178457}.dash-late{background:#fff7e6;color:#b7791f}.dash-absent{background:#fff0ee;color:#c0392b}.dash-unchecked{background:#f0f3f8;color:#667085}
    .dash-progress{height:7px;background:#edf1f6;border-radius:999px;overflow:hidden;margin-top:11px}.dash-progress>span{display:block;height:100%;background:linear-gradient(90deg,#3559db,#6b85ed);border-radius:999px}
  `;
  document.head.appendChild(style);

  let stopFns=[];
  let cellData=[];
  let attData=[];
  let rendering=false;

  const peopleCount=c=>(c?.leader?1:0)+(c?.helper?1:0)+(Array.isArray(c?.members)?c.members.length:0);
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
  const stats=records=>{
    const vals=Object.values(records||{});
    const present=vals.filter(v=>v==='present').length;
    const late=vals.filter(v=>v==='late').length;
    const absent=vals.filter(v=>v==='absent').length;
    const checked=present+late+absent;
    return {present,late,absent,checked,rate:checked?Math.round(present/checked*100):null};
  };

  function renderDashboard(){
    const summary=document.getElementById('summary');
    const rateEl=document.getElementById('rate');
    if(!summary||!rateEl||rendering) return;
    rendering=true;
    try{
      const dates=attData.map(a=>a.date).filter(Boolean).sort();
      const latestDate=dates.at(-1)||'';
      const latestRecords=attData.filter(a=>a.date===latestDate);
      let gp=0,gl=0,ga=0;
      latestRecords.forEach(a=>{const s=stats(a.records);gp+=s.present;gl+=s.late;ga+=s.absent});
      const gd=gp+gl+ga;
      rateEl.textContent=gd?Math.round(gp/gd*100)+'%':'-';
      const note=rateEl.parentElement?.querySelector('.stat-note');
      if(note) note.textContent=latestDate?`${latestDate} 기준 · 지각은 출석률에 포함되지 않음`:'최근 저장된 출석 기준';

      if(!cellData.length){summary.innerHTML='<div class="empty">표시할 셀이 없습니다.</div>';return;}
      summary.innerHTML='<div class="dash-cell-attendance">'+cellData.map(c=>{
        const recs=attData.filter(a=>a.cellId===c.id&&a.date).sort((a,b)=>String(a.date).localeCompare(String(b.date)));
        const latest=recs.at(-1);
        const s=stats(latest?.records);
        const total=peopleCount(c);
        const unchecked=Math.max(0,total-s.checked);
        const rate=s.rate===null?'-':s.rate+'%';
        const width=s.rate===null?0:s.rate;
        return `<div class="dash-cell-row">
          <div class="dash-cell-top"><div><div class="dash-cell-name">${esc(c.name)}</div><div class="dash-cell-meta">${latest?.date?esc(latest.date)+' 기준':'아직 저장된 출석 기록 없음'} · 전체 ${total}명</div></div><div class="dash-cell-rate">${rate}</div></div>
          <div class="dash-progress"><span style="width:${width}%"></span></div>
          <div class="dash-statuses"><span class="dash-pill dash-present">출석 ${s.present}</span><span class="dash-pill dash-late">지각 ${s.late}</span><span class="dash-pill dash-absent">결석 ${s.absent}</span>${unchecked?`<span class="dash-pill dash-unchecked">미체크 ${unchecked}</span>`:''}</div>
        </div>`;
      }).join('')+'</div>';
    }finally{rendering=false;}
  }

  function clearSubs(){stopFns.forEach(f=>{try{f()}catch{}});stopFns=[];cellData=[];attData=[];}

  const wait=setInterval(()=>{
    if(!getApps().length) return;
    clearInterval(wait);
    const app=getApp();
    const auth=getAuth(app);
    const db=getFirestore(app);
    onAuthStateChanged(auth,async user=>{
      clearSubs();
      if(!user) return;
      try{
        const ps=await getDoc(doc(db,'users',user.uid));
        const p=ps.exists()?ps.data():{};
        const admin=(user.email||'').toLowerCase()===OWNER_EMAIL||p.role==='admin';
        if(admin){
          stopFns.push(onSnapshot(collection(db,'cells'),s=>{cellData=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
          stopFns.push(onSnapshot(collection(db,'attendance'),s=>{attData=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
        }else if(p.cellId){
          stopFns.push(onSnapshot(doc(db,'cells',p.cellId),s=>{cellData=s.exists()?[{id:s.id,...s.data()}]:[];setTimeout(renderDashboard,0)}));
          stopFns.push(onSnapshot(query(collection(db,'attendance'),where('cellId','==',p.cellId)),s=>{attData=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
        }
      }catch(e){console.error('Dashboard attendance enhancement error:',e)}
    });

    const summary=document.getElementById('summary');
    if(summary){
      const mo=new MutationObserver(()=>{
        if(rendering) return;
        if(cellData.length && !summary.querySelector('.dash-cell-attendance')) setTimeout(renderDashboard,20);
      });
      mo.observe(summary,{childList:true,subtree:true});
    }
  },100);
}

queueMicrotask(injectSignupUI);
setTimeout(installDashboardAttendance,0);
