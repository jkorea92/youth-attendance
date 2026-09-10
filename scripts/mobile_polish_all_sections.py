from pathlib import Path

FILES=[Path('index.html'),Path('app-v4.html')]
MARK='/* mobile-polish-all-20260910 */'
CSS=r'''

/* mobile-polish-all-20260910 */
@media(max-width:760px){
  html,body{width:100%;max-width:100%;overflow-x:hidden}
  body{-webkit-text-size-adjust:100%;font-size:15px}
  .wrap{width:100%;max-width:100%;padding-left:10px;padding-right:10px}
  header{padding:10px 0}
  .top{gap:8px}
  .brandarea{gap:6px}
  .church-logo{width:min(235px,76vw);margin:0 auto;padding:4px 6px}
  .brand{font-size:16px}.sub{font-size:10.5px}
  .user{font-size:11px;gap:5px}.badge{font-size:10px;padding:4px 7px}.user button{padding:8px 10px;min-height:36px}

  .tabs{width:calc(100vw - 20px);margin:10px 0 12px;padding:4px;gap:3px;border-radius:12px}
  .tab{padding:9px 11px;min-height:38px;font-size:13px}

  .grid{display:block}
  .grid>.card{width:100%;margin-bottom:10px}
  .card{padding:13px;border-radius:14px}
  h2{font-size:24px;line-height:1.25;margin-bottom:16px}h3{font-size:19px;line-height:1.3}
  label{font-size:13px;margin-top:11px}
  input,select,textarea{font-size:16px;width:100%;max-width:100%;min-width:0}
  button{font-size:14px}
  .row{grid-template-columns:minmax(0,1fr);gap:8px}
  .actions{gap:6px;max-width:100%}

  #attend .card:first-child .row{grid-template-columns:1fr}
  #attend .card:first-child .actions{display:grid;grid-template-columns:1fr 1fr;width:100%}
  #allPresent,#saveAtt{width:100%;min-width:0}

  #attend .table{width:100%;max-width:100%;overflow:visible}
  #attBody{width:100%}
  #attBody tr{padding:11px 10px;margin-bottom:10px;overflow:hidden}
  #attBody td{display:grid!important;grid-template-columns:72px minmax(0,1fr)!important;gap:8px;width:100%;max-width:100%;padding:7px 0!important;align-items:start;white-space:normal!important}
  #attBody td::before{min-width:0;white-space:nowrap;line-height:1.35;padding-top:5px}
  #attBody td>*,#attBody td .actions{min-width:0;max-width:100%}
  #attBody td:nth-child(1) b{font-size:17px;line-height:1.35}
  #attBody .part-badge{display:inline-flex;align-items:center;justify-content:center;max-width:100%;white-space:normal;word-break:keep-all;text-align:center;line-height:1.25;padding:6px 9px}
  #attBody .actions{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px;width:100%;max-width:100%}
  #attBody .att{width:100%!important;min-width:0!important;max-width:100%;padding:9px 3px!important;font-size:12px!important;line-height:1.2;white-space:nowrap!important}
  #attBody td:nth-child(6) .actions{grid-template-columns:1fr!important}
  #attBody td:nth-child(6) .att{width:100%!important;min-width:0!important}

  #cells .card[style]{width:100%;max-width:100%}
  .member-row{grid-template-columns:minmax(0,1fr)!important;gap:7px}
  .member-row [data-member-name],.member-row [data-member-part],.member-row [data-member-note],.member-row .danger{grid-column:1/-1!important;width:100%}
  .member-row [data-member-note]{min-height:96px}
  .member-summary-row{grid-template-columns:1fr!important;gap:5px}
  .member-summary-row>*{grid-column:1/-1!important;min-width:0}
  .cell{padding:11px}.celltop{flex-direction:column;align-items:stretch}.celltop>.actions{width:100%}.celltop>.actions button{flex:1}

  #users .table{width:100%;max-width:100%;overflow-x:auto}
  #users table{min-width:620px;font-size:12px}#users th,#users td{padding:8px}

  .roster-grid{grid-template-columns:1fr!important}.roster-group{min-width:0}
  .metrics{display:grid;grid-template-columns:1fr 1fr;gap:6px}.metric{text-align:center;white-space:normal!important;line-height:1.25}
  .name-chip{white-space:normal!important;line-height:1.25}
  .dual-rate{font-size:18px!important}
  .stat{font-size:25px}
}
@media(max-width:390px){
  .wrap{padding-left:8px;padding-right:8px}
  .tabs{width:calc(100vw - 16px)}
  .tab{padding:8px 9px;font-size:12px}
  .card{padding:11px}
  #attBody tr{padding:9px 8px}
  #attBody td{grid-template-columns:64px minmax(0,1fr)!important;gap:6px}
  #attBody .att{font-size:11.5px!important;padding:8px 2px!important}
  .metrics{grid-template-columns:1fr}
}
'''

for path in FILES:
    s=path.read_text(encoding='utf-8')
    if MARK in s:
        continue
    if '</style>' not in s:
        raise SystemExit(f'{path}: no </style>')
    s=s.replace('</style>',CSS+'\n</style>',1)
    path.write_text(s,encoding='utf-8')
