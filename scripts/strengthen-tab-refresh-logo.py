from pathlib import Path

FILES=[Path('index.html'),Path('app-v4.html')]

for path in FILES:
    s=path.read_text(encoding='utf-8')

    s=s.replace(
        '<div id="homeBrand" class="brandarea" role="button" tabindex="0" aria-label="대시보드로 이동">',
        '<button type="button" id="homeBrand" class="brandarea home-brand-btn" aria-label="대시보드로 이동">',
        1
    )
    s=s.replace(
        '<div class="brandcopy"><div class="brand">청년부 출석관리</div></div></div><div id="userBox"',
        '<div class="brandcopy"><div class="brand">청년부 출석관리</div></div></button><div id="userBox"',
        1
    )

    css='''\n/* stronger-tab-logo-fix-20260910 */\n#homeBrand.home-brand-btn{\n  appearance:none;-webkit-appearance:none;border:0;background:transparent;color:inherit;padding:0;margin:0;\n  text-align:inherit;font:inherit;cursor:pointer;border-radius:12px;\n}\n#homeBrand.home-brand-btn:hover{background:rgba(255,255,255,.06)}\n#homeBrand.home-brand-btn:active{transform:translateY(1px)}\n'''
    if '/* stronger-tab-logo-fix-20260910 */' not in s:
        s=s.replace('</style>',css+'\n</style>',1)

    old='''function activeTabId(){return document.querySelector(".tab.active")?.dataset.tab||"dash"}\nfunction refreshTabState(tabId){\n try{\n  if(tabId==="dash")renderDash();\n  else if(tabId==="attend")renderAttendance();\n  else if(tabId==="cells"){resetCellForm();renderCells();}\n  else if(tabId==="users")renderUsers();\n }catch(e){console.error("tab refresh",tabId,e)}\n}\nfunction switchTab(tabId){\n const previous=activeTabId();\n if(previous!==tabId)refreshTabState(previous);\n const target=[...document.querySelectorAll(".tab")].find(x=>x.dataset.tab===tabId&&!x.classList.contains("hidden"));\n if(!target)return;\n document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===target));\n document.querySelectorAll(".panel").forEach(x=>x.classList.toggle("active",x.id===tabId));\n if(tabId==="dash")renderDash();\n}\ndocument.querySelectorAll(".tab").forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));\n$("homeBrand").onclick=()=>switchTab("dash");\n$("homeBrand").onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();switchTab("dash")}};'''

    new='''function activeTabId(){return document.querySelector(".tab.active")?.dataset.tab||"dash"}\nfunction resetTabState(tabId){\n try{\n  if(tabId==="attend"){\n   $("attMsg").textContent="";\n   $("attDate").value=today();\n   if(isAdmin()){selectedCellId="";$("attCell").value="";}else if(profile?.cellId){selectedCellId=profile.cellId;$("attCell").value=profile.cellId;}\n   renderAttendance();\n  }else if(tabId==="cells"){\n   resetCellForm();\n   renderCells();\n  }else if(tabId==="users"){\n   renderUsers();\n  }else if(tabId==="dash"){\n   $("dashDate").value=today();\n   renderDash();\n  }\n }catch(e){console.error("tab reset",tabId,e)}\n}\nfunction switchTab(tabId){\n const previous=activeTabId();\n if(previous!==tabId)resetTabState(previous);\n const target=[...document.querySelectorAll(".tab")].find(x=>x.dataset.tab===tabId&&!x.classList.contains("hidden"));\n if(!target)return;\n document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===target));\n document.querySelectorAll(".panel").forEach(x=>x.classList.toggle("active",x.id===tabId));\n if(tabId==="dash")renderDash();\n else if(tabId==="attend")renderAttendance();\n else if(tabId==="cells")renderCells();\n else if(tabId==="users")renderUsers();\n window.scrollTo({top:0,behavior:"instant"});\n}\ndocument.querySelectorAll(".tab").forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));\n$("homeBrand").onclick=()=>switchTab("dash");'''

    if old in s:
        s=s.replace(old,new,1)
    else:
        raise SystemExit(f'{path}: old tab block not found')

    path.write_text(s,encoding='utf-8')
    print(f'{path}: patched')
