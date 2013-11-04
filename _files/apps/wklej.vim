" wklej.vim:    Vim plugin for wklej.org
" Maintainer:   Pawel Kilian <pkilian@wklej.org>
" Version:      0.1

" Usage:
"   :Wklej    create a paste from the current buffer of selection - public
"   :Wklejp   create a paste from the current buffer of selection - private

" If you want to paste on ctrl + p just add this to your vimrc:
" 	map ^P :Wklej<CR>
" (where ^P is entered using ctrl + v, ctrl + p in vim)
"
" If you want you can setup a nick for your pastes
" In ~/.vimrc add: let g:nick = "YOUR_NICK"
" and thats it
"

function! s:WklejInit()
python << EOF

import vim
import re
from xmlrpclib import ServerProxy
srv = ServerProxy('http://wklej.org/xmlrpc/', allow_none=True)

new_paste = srv.dodaj_wpis
new_paste_prv = srv.dodaj_prywatny_wpis

language_mapping = {
    'python':           'python',
    'php':              'html+php',
    'smarty':           'smarty',
    'tex':              'tex',
    'rst':              'rst',
    'cs':               'csharp',
    'haskell':          'haskell',
    'xml':              'xml',
    'html':             'html',
    'xhtml':            'html',
    'htmldjango':       'html+django',
    'django':           'html+django',
    'htmljinja':        'html+django',
    'jinja':            'html+django',
    'lua':              'lua',
    'scheme':           'scheme',
    'mako':             'html+mako',
    'c':                'c',
    'cpp':              'cpp',
    'javascript':       'js',
    'jsp':              'jsp',
    'ruby':             'ruby',
    'bash':             'bash',
    'sh':               'bash',
    'bat':              'bat',
    'd':                'd',
    'genshi':           'html+genshi',
    'vim':              'vim'
}

language_reverse_mapping = {}
for key, value in language_mapping.iteritems():
    language_reverse_mapping[value] = key

def make_utf8(code):
    enc = vim.eval('&fenc') or vim.eval('&enc')
    return code.decode(enc, 'ignore').encode('utf-8')

EOF
endfunction

if !exists("g:nick")
    let g:nick = "Anonim"
endif


function! s:Wklej(line1,line2,count,...)
call s:WklejInit()
python << endpython
rng_start = int(vim.eval('a:line1')) - 1
rng_end = int(vim.eval('a:line2'))
if int(vim.eval('a:count')):
    code = '\n'.join(vim.current.buffer[rng_start:rng_end])
else:
    code = '\n'.join(vim.current.buffer)
code = make_utf8(code)
author = vim.eval("g:nick")
syntax = language_mapping.get(vim.eval('&ft'), 'text')
wklej_id = new_paste(code, syntax, author)
url = 'http://wklej.org%s' % wklej_id
print 'Pasted to %s' % (url)
endpython
endfunction




function! s:Wklejp(line1,line2,count,...)
call s:WklejInit()
python << endpython
rng_start = int(vim.eval('a:line1')) - 1 
rng_end = int(vim.eval('a:line2'))
if int(vim.eval('a:count')):
    code = '\n'.join(vim.current.buffer[rng_start:rng_end])
else:
    code = '\n'.join(vim.current.buffer)
code = make_utf8(code)
author = vim.eval("g:nick")
syntax = language_mapping.get(vim.eval('&ft'), 'text')
wklej_id = new_paste_prv(code, syntax, author)
url = 'http://wklej.org%s' % wklej_id
print 'Pasted to %s' % (url)
endpython
endfunction

command! -range=0 -nargs=* Wklej :call s:Wklej(<line1>,<line2>,<count>,<f-args>)
command! -range=0 -nargs=* Wklejp :call s:Wklejp(<line1>,<line2>,<count>,<f-args>)

