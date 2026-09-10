from pathlib import Path
import re

FILES=[Path('index.html'),Path('app-v4.html')]
for path in FILES:
    s=path.read_text(encoding='utf-8')
    s=s.replace('퍼스백양장로교회 청년부 출석체크','퍼스백양장로교회 청년부 출석관리')
    s=s.replace('>청년부 출석체크<','>청년부 출석관리<')
    s=re.sub(r'\s*<div class="sub">퍼스백양장로교회\s*·\s*온라인 공동 출석관리</div>','',s)
    path.write_text(s,encoding='utf-8')
    print(f'{path}: updated')
