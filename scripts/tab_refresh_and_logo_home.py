from pathlib import Path

FILES=[Path('index.html'),Path('app-v4.html')]

for path in FILES:
    s=path.read_text(encoding='utf-8')

    old_header='<header><div class="wrap top"><div class="brandarea"><img src="assets/church-logo.svg?v=vector-20260909" alt="퍼스백양장로교회 로고" class="church-logo"><div class="brandcopy"><div class="brand">청년부 출석관리</div></div></div><div id="userBox" class="user hidden">'
    new_header='<header><div class="wrap top"><div id="homeBrand" class="brandarea" role="button" tabindex="0" aria-label="대시보드로 이동"><img src="assets/church-logo.svg?v=vector-20260909" alt="퍼스백양장로교회 로고" class="church-logo"><div class="brandcopy"><div class="brand">청년부 출석관리</div></div></div><div id="userBox" class="user hidden">'
    if old_header in s:
        s=s.replace(old_header,new_header,1)

    css_marker='/* brand-home-click-20260910 */'
    if css_marker not in s:
        css='''\n/* brand-home-click-20260910 */\n#homeBrand{cursor:pointer;user-select:none}\n#homeBrand:focus-visible{outline:3px solid rgba(255,255,255,.85);outline-offset:5px;border-radius:12px}\n'''
        s=s.replace('</style>',css+'\n</style>',1)

    old_tabs='document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===b));document.querySelectorAll(".panel").forEach(x=>x.classList.toggle("active",x.id===b.dataset.tab))});'
    new_tabs='''function activeTabId(){return document.querySelector(".tab.active")?.dataset.tab||"dash"}\nfunction refreshTabState(tabId){\n try{\n  if(tabId==="dash")renderDash();\n  else if(tabId==="attend")renderAttendance();\n  else if(tabId==="cells"){resetCellForm();renderCells();}\n  else if(tabId==="users")renderUsers();\n }catch(e){console.error("tab refresh",tabId,e)}\n}\nfunction switchTab(tabId){\n const previous=activeTabId();\n if(previous!==tabId)refreshTabState(previous);\n const target=[...document.querySelectorAll(".tab")].find(x=>x.dataset.tab===tabId&&!x.classList.contains("hidden"));\n if(!target)return;\n document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===target));\n document.querySelectorAll(".panel").forEach(x=>x.classList.toggle("active",x.id===tabId));\n if(tabId==="dash")renderDash();\n}\ndocument.querySelectorAll(".tab").forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));\n$("homeBrand").onclick=()=>switchTab("dash");\n$("homeBrand").onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();switchTab("dash")}};'''
    if old_tabs in s:
        s=s.replace(old_tabs,new_tabs,1)
    elif 'function switchTab(tabId)' not in s:
        raise SystemExit(f'{path}: tab handler pattern not found')

    path.write_text(s,encoding='utf-8')
    print(f'{path}: patched')
