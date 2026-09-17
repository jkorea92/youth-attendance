from pathlib import Path

files = [Path('index.html'), Path('app-v4.html')]
for path in files:
    text = path.read_text(encoding='utf-8')

    text = text.replace(
        '전체 출석을 먼저 적용한 뒤, 지각·결석 등 예외 인원만 세부 수정하면 빠르게 체크할 수 있습니다.',
        '전체 출석을 먼저 적용한 뒤, 지각·결석 등 예외 인원만 세부 수정하면 빠르게 체크할 수 있습니다. 출석 버튼을 빠르게 두 번 누르면 해당 체크가 해제됩니다.'
    )

    text = text.replace('return"✓ 둘 다 출석";', 'return"✓ 출석";')

    clear_button = '    const cb=document.createElement("button");cb.type="button";cb.className="quick-clear";cb.textContent="체크 해제";cb.dataset.clear="1";cb.disabled=!editable;quickWrap.appendChild(cb);\n'
    text = text.replace(clear_button, '')

    old_click = '''if(b.dataset.quick){
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
 if(b.dataset.clear){
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,"")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    new_click = '''if(b.dataset.quick){
  const now=Date.now(),last=Number(b.dataset.lastQuickTap||0),isDouble=now-last<360;
  b.dataset.lastQuickTap=isDouble?"0":String(now);
  ["worship","cell"].forEach(track=>{if(trackEnabled(p,track))setTrackState(tr,track,isDouble?"":"present")});
  updateRowSummary(tr,p,false);tr.querySelector(".att-detail")?.removeAttribute("open");return;
 }
'''
    if old_click in text:
        text = text.replace(old_click, new_click, 1)
    elif 'lastQuickTap' not in text:
        raise SystemExit(f'Could not find quick click block in {path}')

    text = text.replace('  #attBody .quick-clear{width:100%!important;min-width:0!important}\n', '')
    text = text.replace('.quick-clear{width:100%;background:#f2f4f7;color:#475467;border:1px solid #d0d5dd;padding:9px 12px}\n.quick-clear:hover{background:#eaecf0}\n', '')

    if 'touch-action:manipulation' not in text:
        text = text.replace(
            '.quick-present{width:100%;background:#e9f8f0;color:var(--green);border:1px solid #bce5cf;padding:10px 12px}',
            '.quick-present{width:100%;background:#e9f8f0;color:var(--green);border:1px solid #bce5cf;padding:10px 12px;touch-action:manipulation}'
        )

    path.write_text(text, encoding='utf-8')
