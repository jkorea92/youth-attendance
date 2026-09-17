from pathlib import Path

files = [Path('index.html'), Path('app-v4.html')]

reason_css = '''
/* long-absence-reason-20260917 */
.long-reason-inline{
  margin-top:7px;padding:8px 10px;border:1px solid #e2d7fb;border-radius:9px;
  background:#faf8ff;color:#55436f;font-size:12px;line-height:1.45;white-space:normal!important;
}
.long-reason-inline b{color:var(--purple);margin-right:5px}
.long-reason-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:7px}
.long-reason-card{border:1px solid #e2d7fb;border-radius:10px;background:#faf8ff;padding:9px 10px;min-width:0}
.long-reason-name{font-size:12px;font-weight:900;color:var(--purple);margin-bottom:4px}
.long-reason-text{font-size:11px;line-height:1.45;color:#5f5870;white-space:normal;overflow-wrap:anywhere}
.long-reason-empty{color:#98a2b3;font-style:italic}
@media(max-width:760px){
  .long-reason-list{grid-template-columns:1fr}
  .long-reason-inline{font-size:12px;padding:8px 9px}
}
'''

for path in files:
    text = path.read_text(encoding='utf-8')

    if '/* long-absence-reason-20260917 */' not in text:
        text = text.replace('</style>', reason_css + '\n</style>', 1)

    old_status = '''   const ss=document.createElement("span");ss.dataset.statusSummary="1";ss.className="status-summary";tdStatus.appendChild(ss);\n'''
    new_status = '''   const ss=document.createElement("span");ss.dataset.statusSummary="1";ss.className="status-summary";tdStatus.appendChild(ss);\n   if(isLong){\n    const reason=document.createElement("div");reason.className="long-reason-inline";\n    const label=document.createElement("b");label.textContent="사유";reason.appendChild(label);\n    const value=document.createElement("span");value.textContent=(p.note||"").trim()||"사유 미입력";reason.appendChild(value);tdStatus.appendChild(reason);\n   }\n'''
    if old_status in text and 'const value=document.createElement("span");value.textContent=(p.note||"").trim()||"사유 미입력"' not in text:
        text = text.replace(old_status, new_status, 1)

    old_cell_status = '''function cellStatus(c,date){\n const ppl=people(c),ls=knownLongSet(c),long=[];ppl.forEach((person,i)=>{if(ls.has(personKey(person,i)))long.push(person.role==="셀원"?person.name:`${person.name} (${person.role})`)});\n return{total:ppl.length,long,worship:trackStatus(c,date,"worship"),cell:trackStatus(c,date,"cell"),has:!!attendance[attId(date,c.id)]};\n}\n'''
    new_cell_status = '''function cellStatus(c,date){\n const ppl=people(c),ls=knownLongSet(c),long=[],longDetails=[];\n ppl.forEach((person,i)=>{\n  if(!ls.has(personKey(person,i)))return;\n  const name=person.role==="셀원"?person.name:`${person.name} (${person.role})`;\n  long.push(name);longDetails.push({name,reason:(person.note||"").trim()});\n });\n return{total:ppl.length,long,longDetails,worship:trackStatus(c,date,"worship"),cell:trackStatus(c,date,"cell"),has:!!attendance[attId(date,c.id)]};\n}\n'''
    if old_cell_status in text:
        text = text.replace(old_cell_status, new_cell_status, 1)

    chips_anchor = '''function nameChips(list){return list.length?list.map(n=>`<span class="name-chip">${esc(n)}</span>`).join(""):'<span class="roster-empty">없음</span>'}\n'''
    reason_helper = chips_anchor + '''function longReasonCards(list){\n return list.length?`<div class="long-reason-list">${list.map(x=>`<div class="long-reason-card"><div class="long-reason-name">${esc(x.name)}</div><div class="long-reason-text ${x.reason?"":"long-reason-empty"}">${x.reason?`사유: ${esc(x.reason)}`:"사유 미입력"}</div></div>`).join("")}</div>`:'<span class="roster-empty">없음</span>'\n}\n'''
    if 'function longReasonCards(list)' not in text and chips_anchor in text:
        text = text.replace(chips_anchor, reason_helper, 1)

    old_dash_long = '''${s.long.length?`<div class="status-section"><div class="status-section-title">장기결석</div><div class="name-list">${nameChips(s.long)}</div></div>`:""}'''
    new_dash_long = '''${s.long.length?`<div class="status-section"><div class="status-section-title">장기결석 · 사유</div>${longReasonCards(s.longDetails||[])}</div>`:""}'''
    if old_dash_long in text:
        text = text.replace(old_dash_long, new_dash_long, 1)

    path.write_text(text, encoding='utf-8')
