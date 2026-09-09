from pathlib import Path

CSS = r'''
/* horizontal-text-fix-20260909 */
html,body,button,input,select,textarea,table,th,td,label,.brand,.sub,.muted,.metric,.name-chip,.badge,.tab,.cell,.card,.actions,.att{
  word-break:keep-all;
  overflow-wrap:normal;
}
button,.att,.tab,.badge,.metric,.name-chip,th,label{
  white-space:nowrap;
}
#attend td:nth-child(1),#attend td:nth-child(2),#attend td:nth-child(4){
  white-space:nowrap;
}
@media(max-width:760px){
  #attBody td{grid-template-columns:88px minmax(0,1fr)}
  #attBody td:nth-child(1),#attBody td:nth-child(2),#attBody td:nth-child(4){white-space:nowrap}
  #attBody .actions{grid-template-columns:repeat(3,minmax(72px,1fr))}
  #attBody .att{font-size:13px;line-height:1.2;white-space:nowrap;word-break:keep-all}
  #attBody td:nth-child(4) .att{min-width:92px;width:auto}
}
@media(max-width:390px){
  #attBody td{grid-template-columns:76px minmax(0,1fr)}
  #attBody .actions{grid-template-columns:repeat(3,minmax(66px,1fr))}
  #attBody .att{font-size:12px}
}
'''

for name in ('index.html','app-v4.html'):
    p = Path(name)
    s = p.read_text(encoding='utf-8')
    marker = '/* horizontal-text-fix-20260909 */'
    if marker not in s:
        s = s.replace('</style>', CSS + '\n</style>', 1)
        p.write_text(s, encoding='utf-8')

# trigger workflow after creation
