import { getApps, getApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";
import { getFirestore, doc, getDoc, updateDoc, collection, onSnapshot, query, where } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-firestore.js";

export const firebaseConfig = {
  apiKey: "AIzaSyBLQ7I3EO4g5VPnY35WZfNpbf3XvWjKit8",
  authDomain: "youth-attendance-7d46c.firebaseapp.com",
  projectId: "youth-attendance-7d46c",
  storageBucket: "youth-attendance-7d46c.firebasestorage.app",
  messagingSenderId: "210019623751",
  appId: "1:210019623751:web:6b2597c947e1b96c156262"
};

const OWNER_EMAIL = "jaehokorea92@gmail.com";

function installAttendanceEnhancements(){
  if(document.getElementById('attendanceEnhancementStyle')) return;

  const style=document.createElement('style');
  style.id='attendanceEnhancementStyle';
  style.textContent=`
    .long-absent-btn{border:1px solid #c7b8ff!important;background:#f5f1ff!important;color:#6941c6!important;white-space:nowrap}
    .long-absent-btn.on{background:#6941c6!important;color:#fff!important;border-color:#6941c6!important}
    #attBody tr.long-absent-row td{background:#fbf9ff}
    #attBody tr.long-absent-row td:first-child strong:after{content:" · 장기결석";font-size:10px;color:#6941c6;font-weight:800}
    .metric.long{background:#f3efff;color:#6941c6}
    .dash-long{background:#f3efff;color:#6941c6}
  `;
  document.head.appendChild(style);

  let db=null,auth=null,currentUser=null,currentProfile=null;
  let cellUnsub=null,currentCellId='',longAbsentSet=new Set();
  let dashboardCells=[],dashboardAttendance=[],dashboardUnsubs=[],dashboardRendering=false;

  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
  const people=c=>[...(c?.leader?[{name:c.leader,role:'리더'}]:[]),...(c?.helper?[{name:c.helper,role:'헬퍼'}]:[]),...(c?.members||[]).map(name=>({name,role:'셀원'}))];
  const keyFor=(p,i)=>`${p.role}:${p.name}:${i}`;

  function isEditableRow(row){
    const b=row.querySelector('.att.p');
    return !!b && !b.disabled;
  }

  function enforceLongRows(){
    document.querySelectorAll('#attBody tr[data-k]').forEach(row=>{
      const key=row.dataset.k;
      const active=longAbsentSet.has(key);
      row.classList.toggle('long-absent-row',active);
      const btn=row.querySelector('.long-absent-btn');
      if(btn){
        btn.classList.toggle('on',active);
        btn.textContent=active?'장기결석 해제':'장기결석';
        btn.disabled=!isEditableRow(row) && !active;
      }
      row.querySelectorAll('.att.p,.att.l,.att.a').forEach(b=>{
        if(active){
          b.classList.remove('on');
          b.disabled=true;
        }else if(currentProfile && ['admin','leader','helper'].includes(currentProfile.role)){
          b.disabled=false;
        }
      });
      if(active) row.dataset.s='';
    });
  }

  function ensureLongAbsentColumn(){
    const head=document.querySelector('#attend table thead tr');
    if(head && !head.querySelector('.long-absent-head')){
      const th=document.createElement('th');
      th.className='long-absent-head';
      th.textContent='장기결석';
      head.appendChild(th);
    }
    document.querySelectorAll('#attBody tr[data-k]').forEach(row=>{
      if(row.querySelector('.long-absent-cell')) return;
      const td=document.createElement('td');
      td.className='long-absent-cell';
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='att long-absent-btn';
      btn.textContent='장기결석';
      btn.addEventListener('click',async e=>{
        e.preventDefault();e.stopPropagation();
        if(!db||!currentCellId||!currentUser||!currentProfile) return;
        if(!['admin','leader','helper'].includes(currentProfile.role)) return;
        const key=row.dataset.k;
        const next=new Set(longAbsentSet);
        if(next.has(key)) next.delete(key); else next.add(key);
        try{
          await updateDoc(doc(db,'cells',currentCellId),{
            longAbsentKeys:[...next],
            longAbsentUpdatedAt:Date.now(),
            longAbsentUpdatedBy:currentUser.email||''
          });
        }catch(err){
          console.error('Long absence update error:',err);
          alert('장기결석 상태를 저장하지 못했습니다. Firestore 보안 규칙을 확인해주세요.');
        }
      });
      td.appendChild(btn);row.appendChild(td);
    });
    enforceLongRows();
  }

  function watchSelectedCell(){
    const select=document.getElementById('attCell');
    const cellId=select?.value||'';
    if(cellId===currentCellId) { ensureLongAbsentColumn(); return; }
    currentCellId=cellId;longAbsentSet=new Set();
    if(cellUnsub){try{cellUnsub()}catch{} cellUnsub=null;}
    if(!db||!cellId){ensureLongAbsentColumn();return;}
    cellUnsub=onSnapshot(doc(db,'cells',cellId),snap=>{
      const data=snap.exists()?snap.data():{};
      longAbsentSet=new Set(Array.isArray(data.longAbsentKeys)?data.longAbsentKeys:[]);
      ensureLongAbsentColumn();
      setTimeout(renderDashboard,0);
    },err=>console.error('Long absence listener error:',err));
  }

  document.addEventListener('click',e=>{
    const btn=e.target.closest?.('button.att.p,button.att.l,button.att.a');
    if(btn && btn.classList.contains('on') && !btn.disabled){
      e.preventDefault();
      e.stopImmediatePropagation();
      const row=btn.closest('tr[data-k]');
      if(row){
        row.dataset.s='';
        row.querySelectorAll('.att.p,.att.l,.att.a').forEach(x=>x.classList.remove('on'));
      }
      return;
    }
    if(e.target.closest?.('#allPresent')) setTimeout(enforceLongRows,0);
  },true);

  const attBody=document.getElementById('attBody');
  if(attBody){
    const mo=new MutationObserver(()=>{ensureLongAbsentColumn();watchSelectedCell()});
    mo.observe(attBody,{childList:true,subtree:true});
  }
  document.getElementById('attCell')?.addEventListener('change',()=>setTimeout(watchSelectedCell,0));

  function clearDashboardSubs(){dashboardUnsubs.forEach(fn=>{try{fn()}catch{}});dashboardUnsubs=[];dashboardCells=[];dashboardAttendance=[];}
  function statusForCell(c,date){
    const list=people(c),longSet=new Set(Array.isArray(c.longAbsentKeys)?c.longAbsentKeys:[]);
    const recDoc=dashboardAttendance.find(a=>a.cellId===c.id&&a.date===date),rec=recDoc?.records||{};
    let present=0,late=0,absent=0,longAbsent=0;
    list.forEach((p,i)=>{
      const k=keyFor(p,i);
      if(longSet.has(k)){longAbsent++;return;}
      const s=rec[k];
      if(s==='present')present++; else if(s==='late')late++; else if(s==='absent')absent++;
    });
    const activeTotal=Math.max(0,list.length-longAbsent);
    const missing=Math.max(0,activeTotal-present-late-absent);
    return{total:list.length,activeTotal,present,late,absent,longAbsent,missing,hasRecord:!!recDoc};
  }
  function renderDashboard(){
    const summary=document.getElementById('summary'),rateEl=document.getElementById('rate'),rateNote=document.getElementById('rateNote');
    if(!summary||!rateEl||dashboardRendering) return;
    dashboardRendering=true;
    try{
      const date=document.getElementById('dashDate')?.value||'';
      if(!date) return;
      let activeTotal=0,present=0,late=0,absent=0,longAbsent=0,missing=0;
      dashboardCells.forEach(c=>{const x=statusForCell(c,date);activeTotal+=x.activeTotal;present+=x.present;late+=x.late;absent+=x.absent;longAbsent+=x.longAbsent;missing+=x.missing});
      const rate=activeTotal?Math.round(present/activeTotal*100):0;
      rateEl.textContent=activeTotal?rate+'%':'-';
      if(rateNote) rateNote.textContent=`${date} · 출석 ${present} · 지각 ${late} · 결석 ${absent} · 장기결석 ${longAbsent} · 미체크 ${missing}`;
      summary.innerHTML=dashboardCells.length?dashboardCells.map(c=>{
        const x=statusForCell(c,date),r=x.activeTotal?Math.round(x.present/x.activeTotal*100):0;
        return `<div class="cell"><div class="celltop"><div><strong>${esc(c.name)}</strong><div class="muted" style="margin-top:4px">${date} 기준 · 전체 ${x.total}명 · 출석대상 ${x.activeTotal}명</div></div><div class="cell-rate">${x.hasRecord?r+'%':'-'}</div></div><div class="attendance-metrics"><span class="metric p">출석 ${x.present}</span><span class="metric l">지각 ${x.late}</span><span class="metric a">결석 ${x.absent}</span><span class="metric long">장기결석 ${x.longAbsent}</span><span class="metric m">미체크 ${x.missing}</span></div><div class="progress"><span style="width:${x.hasRecord?r:0}%"></span></div></div>`;
      }).join(''):'<div class="empty">표시할 셀이 없습니다.</div>';
    }finally{dashboardRendering=false;}
  }

  document.getElementById('dashDate')?.addEventListener('change',()=>setTimeout(renderDashboard,0));
  const summary=document.getElementById('summary');
  if(summary){
    const mo=new MutationObserver(()=>{
      if(!dashboardRendering && dashboardCells.length) setTimeout(renderDashboard,10);
    });
    mo.observe(summary,{childList:true,subtree:true});
  }

  const wait=setInterval(()=>{
    if(!getApps().length) return;
    clearInterval(wait);
    const app=getApp();auth=getAuth(app);db=getFirestore(app);
    onAuthStateChanged(auth,async user=>{
      currentUser=user;currentProfile=null;
      clearDashboardSubs();
      if(cellUnsub){try{cellUnsub()}catch{} cellUnsub=null;}
      currentCellId='';longAbsentSet=new Set();
      if(!user) return;
      try{
        const ps=await getDoc(doc(db,'users',user.uid));
        currentProfile=ps.exists()?ps.data():{};
        const admin=(user.email||'').toLowerCase()===OWNER_EMAIL||currentProfile.role==='admin';
        if(admin){
          dashboardUnsubs.push(onSnapshot(collection(db,'cells'),s=>{dashboardCells=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
          dashboardUnsubs.push(onSnapshot(collection(db,'attendance'),s=>{dashboardAttendance=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
        }else if(currentProfile.cellId){
          dashboardUnsubs.push(onSnapshot(doc(db,'cells',currentProfile.cellId),s=>{dashboardCells=s.exists()?[{id:s.id,...s.data()}]:[];setTimeout(renderDashboard,0)}));
          dashboardUnsubs.push(onSnapshot(query(collection(db,'attendance'),where('cellId','==',currentProfile.cellId)),s=>{dashboardAttendance=s.docs.map(d=>({id:d.id,...d.data()}));setTimeout(renderDashboard,0)}));
        }
        setTimeout(()=>{watchSelectedCell();ensureLongAbsentColumn();renderDashboard()},50);
      }catch(err){console.error('Attendance enhancement profile error:',err)}
    });
  },80);
}

setTimeout(installAttendanceEnhancements,0);
