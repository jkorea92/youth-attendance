from pathlib import Path

FILES=[Path('index.html'),Path('app-v4.html')]
MARK='/* password-checkbox-align-20260910 */'
CSS=r'''

/* password-checkbox-align-20260910 */
#showPw{
  width:22px!important;
  height:22px!important;
  min-width:22px!important;
  min-height:22px!important;
  max-width:22px!important;
  max-height:22px!important;
  margin:0!important;
  padding:0!important;
  flex:0 0 22px!important;
  vertical-align:middle;
}
#loginView label:has(#showPw){
  display:inline-flex!important;
  align-items:center!important;
  justify-content:flex-start!important;
  gap:10px!important;
  width:auto!important;
  max-width:100%!important;
  margin:14px 0 4px!important;
  font-size:14px!important;
  line-height:1.3!important;
  white-space:nowrap!important;
}
@media(max-width:760px){
  #showPw{width:21px!important;height:21px!important;min-width:21px!important;min-height:21px!important;max-width:21px!important;max-height:21px!important;flex-basis:21px!important}
  #loginView label:has(#showPw){gap:9px!important;margin-top:13px!important;font-size:14px!important}
}
'''

for path in FILES:
    s=path.read_text(encoding='utf-8')
    if MARK in s:
        print(f'{path}: already patched')
        continue
    if '</style>' not in s:
        raise SystemExit(f'{path}: </style> not found')
    s=s.replace('</style>',CSS+'\n</style>',1)
    path.write_text(s,encoding='utf-8')
    print(f'{path}: patched')
