
" try if a path is a racy project
function! s:TryDir(path)
    let l:bopath = a:path   . "/" . "bin"
    let l:bofile = l:bopath . "/" . "build.options"

    if isdirectory( l:bopath )
        return filereadable( l:bofile )
    endif
endfunction

"look into parents and return project dit if any is found, else 0
function! s:FindPrjPath(file)
  let l:file = a:file
  let l:tmppath = l:file
  while len(split(l:tmppath, '/'))>0
      if s:TryDir( l:tmppath )
          return l:tmppath
      endif
      let l:tmppath = '/' . join(split(l:tmppath, '/')[0:-2], '/')
  endwhile
  return 0
endfunction


"Get project name from project path
function! s:GetPrjName(path)
    return split(a:path, '/')[-1]
endfunction

"run racy with specified arguments
function! CallRacy(args)
    let l:oldmakeprg = &makeprg
    let l:racy_command = system("which racy")
    if exists("g:racy_path")
        let l:racy_command = g:racy_path
    endif
    let &makeprg = l:racy_command
    exec "make! " . a:args
    let &makeprg = l:oldmakeprg
endfunction

"get current buffer's project corresponding args for racy
function! GetRacyArgs(extra_args)
    let l:prjpath = s:FindPrjPath(expand("%:p"))
    if type(l:prjpath) == 1
        let l:prjname = s:GetPrjName(l:prjpath)
        return l:prjname . " " . a:extra_args
    else
        return ""
    endif
endfunction

"run racy for current buffer's project
function! Racy(extra_args)
    let l:racy_args = GetRacyArgs(a:extra_args)
    if len(l:racy_args) > 1
        call CallRacy(l:racy_args)
    else
        echo "No project found"
    endif
endfunction

let g:racy_path="~/src/sconspiracy/bin/racy"


function! GetRacyCommand(extra_args)
    return ":Racy " . GetRacyArgs(a:extra_args)
endfunction

command! -nargs=+ Racy :call CallRacy(<q-args>)

nmap <F12> :call Racy("BUILDDEPS=no")<CR>
nmap <S-F12> :call Racy("")<CR>
nmap <expr> <C-F12> GetRacyCommand("")
nmap <expr> <C-S-F12> GetRacyCommand("BUILDDEPS=no")
