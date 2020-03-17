let g:loaded_ECY_vimtex = v:false
fun! s:HasECY()
  if exists('g:loaded_easycomplete') && g:loaded_easycomplete == v:true
    return v:true
  endif
  return v:false
endf

if !s:HasECY()
  finish
endif

" a plugin name can not contain space or any symbols.
let s:your_plugin_name = 'latex'

" must put these outside a function
" s:current_file_dir look like: /home/myplug/plugin_for_ECY
let s:current_file_dir = expand( '<sfile>:p:h:h:h' )
let s:current_file_dir = tr(s:current_file_dir, '\', '/')
let s:client_full_path = s:current_file_dir . '/ECY_vimtex/client/vimtex.py'
let s:server_full_path = s:current_file_dir . '/ECY_vimtex/server/vimtex.py'

"{{{
fun! s:MyInstaller() " called by user. Maybe only once.
  " checked. Must return 'status':0, then return python Server.
  return {'status':'0', 'description':"ok"}
endf

fun! s:MyUnInstaller() " called by user. Maybe only once.
  return {'status': '0', 'name': s:your_plugin_name}
endf
"}}}

fun! ECY_vimtex#GetCandidate()
"{{{ won't be called if g:vimtex_complete_enabled == false
  if !g:loaded_ECY_vimtex || !g:has_vimtex
    return []
  endif
  let l:start_col = vimtex#complete#omnifunc(1, '')
  if l:start_col < 0
    return []
  endif
  try
    let l:candidates = vimtex#complete#omnifunc(0, '')
  catch 
    let l:candidates = []
  endtry
  return l:candidates
"}}}
endf

fun! s:Init()
"{{{
  try
    call vimtex#complete#omnifunc(1,'')
    let g:has_vimtex = v:true
  catch 
    let g:has_vimtex = v:false
  endtry
  let g:vimtex_complete_enabled = get(g:,'vimtex_complete_enabled', v:true) " default to use texlab completion
  let g:ECY_use_taxlab = get(g:,'ECY_use_taxlab', v:true) " if user have
  let g:ECY_vimtex_texlab_path = get(g:,'ECY_vimtex_texlab_path', 'texlab')
"}}}
endf
call s:Init()

call ECY#install#AddEngineInfo(s:your_plugin_name, s:client_full_path,
      \s:server_full_path, function('s:MyInstaller'), function('s:MyUnInstaller'))

let g:loaded_ECY_vimtex = v:true
