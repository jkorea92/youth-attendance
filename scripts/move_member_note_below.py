from pathlib import Path

FILES = [Path('index.html'), Path('app-v4.html')]

old_css = '.member-editor{display:flex;flex-direction:column;gap:8px;margin-top:8px}.member-row{display:grid;grid-template-columns:minmax(110px,1fr) minmax(105px,.8fr) minmax(130px,1.2fr) auto;gap:7px;align-items:center;padding:8px;border:1px solid var(--line);border-radius:11px;background:#fff}.member-row input,.member-row select{min-width:0}'
new_css = '.member-editor{display:flex;flex-direction:column;gap:8px;margin-top:8px}.member-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(120px,.85fr) auto;gap:7px;align-items:center;padding:8px;border:1px solid var(--line);border-radius:11px;background:#fff}.member-row input,.member-row select,.member-row textarea{min-width:0}.member-row [data-member-note]{grid-column:1 / -1;min-height:76px;resize:vertical;line-height:1.45}.member-row .danger{align-self:stretch}'

old_mobile = '@media(max-width:760px){.member-row{grid-template-columns:1fr 1fr}.member-row [data-member-note]{grid-column:1 / -1}.member-row .danger{grid-column:1 / -1}'
new_mobile = '@media(max-width:760px){.member-row{grid-template-columns:minmax(0,1fr) minmax(112px,.9fr)}.member-row [data-member-note]{grid-column:1 / -1;min-height:92px}.member-row .danger{grid-column:1 / -1}'

old_html = 'return `<div class="member-row"><input data-member-name placeholder="이름" value="${esc(x.name)}"><select data-member-part>${opts}</select><input data-member-note placeholder="비고 / 사유" value="${esc(x.note)}"><button type="button" class="danger" data-member-remove>삭제</button></div>`;'
new_html = 'return `<div class="member-row"><input data-member-name placeholder="이름" value="${esc(x.name)}"><select data-member-part>${opts}</select><button type="button" class="danger" data-member-remove>삭제</button><textarea data-member-note rows="3" placeholder="비고 / 사유를 자세히 입력하세요">${esc(x.note)}</textarea></div>`;'

for path in FILES:
    s = path.read_text(encoding='utf-8')
    if old_css not in s:
        raise SystemExit(f'{path}: desktop CSS pattern not found')
    if old_mobile not in s:
        raise SystemExit(f'{path}: mobile CSS pattern not found')
    if old_html not in s:
        raise SystemExit(f'{path}: member row pattern not found')
    s = s.replace(old_css, new_css, 1)
    s = s.replace(old_mobile, new_mobile, 1)
    s = s.replace(old_html, new_html, 1)
    path.write_text(s, encoding='utf-8')

# trigger workflow after it has been installed
