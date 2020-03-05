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

fun! s:Regist(installer, uninstaller, client_lib, client_path, engine_name) " called after vim started.
  call ECY#install#RegisterClient(a:engine_name, a:client_lib, a:client_path)
  call ECY#install#RegisterInstallFunction(a:engine_name, function(a:installer))
  call ECY#install#RegisterUnInstallFunction(a:engine_name, function(a:uninstaller))
endf

" ==============================================================================
" you can just copy the above. What you need to modify is the following.
" ==============================================================================

" a plugin name can not contain space or any symbols.
let s:your_plugin_name = 'latex'

" must put these outside a function
" s:current_file_dir look like: /home/myplug/plugin_for_ECY
let  s:current_file_dir = expand( '<sfile>:p:h:h:h' )
let  s:current_file_dir = tr(s:current_file_dir, '\', '/')

fun! s:MyInstaller() " called by user. Maybe only once.
  " checked. Must return 'status':0, then return python Server.
  return {'status':'0',
        \'description':"ok", 'lib':
        \'ECY_vimtex.server.vimtex', 
        \'name': s:your_plugin_name, 
        \'path': s:current_file_dir
        \}
endf

fun! s:MyUnInstaller() " called by user. Maybe only once.
  return {'status': '0', 'name': s:your_plugin_name}
endf

fun! ECY_vimtex#GetCandidate()
  if !g:loaded_ECY_vimtex || !g:use_vimtex
    return []
  endif
  let l:start_col = vimtex#complete#omnifunc(1, '')
  if l:start_col < 0
    return []
  endif
  return vimtex#complete#omnifunc(0, '')
endf

fun! s:Init()
  try
    call vimtex#complete#omnifunc(0,'')
    let g:use_vimtex = get(g:,'use_vimtex', v:true)
  catch 
    let g:use_vimtex = v:false
  endtry

  if !g:use_vimtex
    let g:ECY_vimtex_texlab_path = get(g:,'ECY_vimtex_texlab_path', 'texlab')
  endif
endf

call s:Init()
" (installer, uninstaller, client_lib, client_path, engine_name)
call s:Regist(
      \'s:MyInstaller',
      \'s:MyUnInstaller',
      \'ECY_vimtex.client.vimtex',
      \s:current_file_dir,
      \s:your_plugin_name)

let g:loaded_ECY_vimtex = v:true
