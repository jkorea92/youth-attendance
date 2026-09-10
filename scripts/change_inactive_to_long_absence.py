from pathlib import Path

FILES = [Path('index.html'), Path('app-v4.html')]

repls = [
('const PARTICIPATIONS=["both","worship","cell","inactive"];\nconst participationLabel=v=>({both:"예배+셀",worship:"예배만",cell:"셀만",inactive:"출석관리 제외"}[v]||"예배+셀");',
 'const PARTICIPATIONS=["both","worship","cell","long"];\nconst participationLabel=v=>({both:"예배+셀",worship:"예배만",cell:"셀만",long:"장기 결석",inactive:"장기 결석"}[v]||"예배+셀");'),
(' const participation=PARTICIPATIONS.includes(x.participation)?x.participation:"both";\n return{name:String(x.name||"").trim(),participation,note:String(x.note||"").trim()};',
 ' const rawParticipation=x.participation==="inactive"?"long":x.participation;\n const participation=PARTICIPATIONS.includes(rawParticipation)?rawParticipation:"both";\n return{name:String(x.name||"").trim(),participation,note:String(x.note||"").trim()};'),
(' people(c).forEach((p,i)=>{const k=personKey(p,i);if(raw.has(k))valid.add(k)});',
 ' people(c).forEach((p,i)=>{const k=personKey(p,i);if(raw.has(k)||p.participation==="long")valid.add(k)});'),
('셀원별로 예배+셀 / 예배만 / 셀만 / 출석관리 제외를 지정하고 비고를 기록할 수 있습니다.',
 '셀원별로 예배+셀 / 예배만 / 셀만 / 장기 결석을 지정하고 비고에 사유를 기록할 수 있습니다.'),
('const lb=document.createElement("button");lb.type="button";lb.className=`att x${isLong?" on":""}`;lb.textContent=isLong?"장기결석 해제":"장기결석";lb.dataset.long="1";lb.disabled=!editable;tdLong.appendChild(lb);',
 'const managedLong=p.participation==="long";const lb=document.createElement("button");lb.type="button";lb.className=`att x${isLong?" on":""}`;lb.textContent=managedLong?"장기결석":(isLong?"장기결석 해제":"장기결석");lb.dataset.long="1";lb.disabled=!editable||managedLong;tdLong.appendChild(lb);')
]

for path in FILES:
    s = path.read_text(encoding='utf-8')
    for old, new in repls:
        if old not in s:
            raise SystemExit(f'{path}: pattern not found: {old[:70]}')
        s = s.replace(old, new, 1)
    path.write_text(s, encoding='utf-8')

# trigger 2026-09-10
