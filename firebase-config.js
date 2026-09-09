import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";

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

queueMicrotask(injectSignupUI);
