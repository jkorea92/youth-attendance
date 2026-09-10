from pathlib import Path

FILES=[Path('index.html'),Path('app-v4.html')]
MARK='/* mobile-overflow-final-20260910 */'
CSS=r'''

/* mobile-overflow-final-20260910 */
@media(max-width:760px){
  html,body{width:100%;max-width:100%;overflow-x:hidden!important}
  body{position:relative}
  header,.wrap,.panel,.grid,.card,.cell,.table,.auth,.tabs{max-width:100%!important;min-width:0!important}
  .wrap{width:100%!important}
  .grid{width:100%;grid-template-columns:minmax(0,1fr)!important}
  .s4,.s12{grid-column:1/-1!important;min-width:0!important}
  .card,.cell{width:100%!important;min-width:0!important;overflow:hidden}
  input,select,textarea,button{max-width:100%!important;min-width:0!important;box-sizing:border-box}
  input[type="date"]{-webkit-appearance:none;appearance:none;width:100%!important;min-width:0!important;max-width:100%!important;display:block}
  #attDate,#dashDate{width:100%!important;min-width:0!important;max-width:100%!important}

  /* header / tabs */
  .brandarea,.brandcopy,.user{min-width:0!important;max-width:100%!important}
  .brand,.sub{max-width:100%;overflow:hidden;text-overflow:ellipsis}
  .tabs{display:flex!important;width:100%!important;overflow-x:auto!important;overflow-y:hidden!important;flex-wrap:nowrap!important;-webkit-overflow-scrolling:touch}
  .tab{flex:0 0 auto!important;min-width:max-content!important}

  /* attendance form */
  #attend .card{overflow:hidden!important}
  #attend .row{grid-template-columns:minmax(0,1fr)!important;width:100%}
  #attend .row>*{min-width:0!important;max-width:100%!important}
  #allPresent,#saveAtt{flex:1 1 0!important;width:auto!important;min-width:0!important}

  /* attendance people cards */
  #attend .table{width:100%!important;overflow:visible!important}
  #attend table,#attend tbody{width:100%!important;max-width:100%!important}
  #attBody tr{width:100%!important;max-width:100%!important;min-width:0!important;overflow:hidden!important;padding:12px!important}
  #attBody td{grid-template-columns:76px minmax(0,1fr)!important;width:100%!important;max-width:100%!important;min-width:0!important;gap:8px!important;padding:8px 0!important;white-space:normal!important;overflow:visible!important}
  #attBody td>*{min-width:0!important;max-width:100%!important}
  #attBody .actions{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important;width:100%!important;max-width:100%!important;min-width:0!important}
  #attBody .att{width:100%!important;min-width:0!important;max-width:100%!important;padding:10px 4px!important;font-size:12px!important;line-height:1.15!important;white-space:nowrap!important}
  #attBody td:nth-child(6) .att{width:100%!important;min-width:0!important}
  .part-badge{max-width:100%;white-space:normal!important;overflow-wrap:anywhere!important;text-align:center}

  /* cell management */
  .member-row{display:grid!important;grid-template-columns:minmax(0,1fr)!important;width:100%!important;max-width:100%!important}
  .member-row>*{grid-column:1/-1!important;width:100%!important;min-width:0!important;max-width:100%!important}
  .member-row [data-member-note]{min-height:96px!important}
  .member-summary-row{grid-template-columns:minmax(0,1fr)!important}
  .member-summary-row>*{grid-column:1/-1!important;min-width:0!important;max-width:100%!important}
  #cellList .celltop{width:100%;min-width:0}
  #cellList .celltop>div{min-width:0;max-width:100%}
  #cellList .actions{width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
  #cellList .actions button{width:100%}

  /* dashboard */
  #dashboard .metrics{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;width:100%}
  #dashboard .metric{min-width:0!important;white-space:normal!important;text-align:center}
  #dashboard .celltop{display:grid!important;grid-template-columns:minmax(0,1fr)!important}
  #dashboard .celltop>div{min-width:0!important;max-width:100%!important}
  .roster-grid{grid-template-columns:minmax(0,1fr)!important}
  .name-chip{max-width:100%;white-space:normal!important;overflow-wrap:anywhere!important}

  /* users / data */
  #users .table,#data .table{width:100%!important;max-width:100%!important;overflow-x:auto!important;-webkit-overflow-scrolling:touch}
  #users table{min-width:640px!important;width:640px!important;max-width:none!important}
  #data button,#csv{max-width:100%!important}
}
@media(max-width:430px){
  .wrap{padding-left:10px!important;padding-right:10px!important}
  .card{padding:13px!important;border-radius:15px}
  #attBody tr{padding:10px!important}
  #attBody td{grid-template-columns:64px minmax(0,1fr)!important;gap:6px!important}
  #attBody .att{font-size:11px!important;padding:9px 2px!important}
  #dashboard .metrics{grid-template-columns:minmax(0,1fr)!important}
  .user{gap:5px!important}
  #userEmail{max-width:55vw!important}
}
@media(max-width:360px){
  #attBody td{grid-template-columns:58px minmax(0,1fr)!important}
  #attBody .att{font-size:10.5px!important}
  .tab{padding:9px 10px!important}
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
