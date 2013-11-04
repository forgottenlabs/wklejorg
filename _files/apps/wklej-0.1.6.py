#!/usr/bin/env python

""" 
Simple wklej.org paste script
license: GPLv2

version 0.1.5

thanks ch4os for help
"""

from optparse import OptionParser
from ConfigParser import *
import commands
import sys
import xmlrpclib
import os


configdict = SafeConfigParser()
configdict.read(os.path.expanduser('~/.wklejrc'))
try:
    key = configdict.defaults()['key']
except:
    key = ''

syntaxes = [ 
'text', 'apache', 'actionscript', 'actionscript3', 'bash', 'bat', 'bbcode', 'befuge', 'boo', 'brainfuck', 'c-objdump',
'c', 'cheetah', 'clojure', 'common-lisp', 'control', 'cpp', 'cpp-objdump', 'csharp', 'css+django', 'css+ruby', 'css+genshi', 'css+mako',
'css+myghty', 'css+php', 'css+smarty', 'css', 'd-objdump', 'd', 'delphi', 'diff', 'django', 'dpatch', 'dylan', 'erb', 'erlang', 'fortran',
'gas', 'genshi', 'genshitext', 'gnuplot', 'groff', 'haskell', 'html+cheetah', 'html+django', 'html+genshi', 'html+mako', 'html+myghty',
'html+php', 'html+smarty', 'html', 'ini', 'io', 'irc', 'java', 'js+cheetah', 'js+django', 'js+ruby', 'js+genshi', 'js+mako', 'js+myghty',
'js+php', 'js+smarty', 'js', 'jsp', 'literate-haskell', 'lighttpd', 'llvm', 'logtalk', 'lua', 'make', 'basemake', 'mako', 'matlab',
'matlabsession', 'minid', 'moocode', 'mupad', 'myghty', 'mysql', 'nasm', 'nginx', 'numpy', 'objdump', 'objective-c', 'ocaml', 'perl',
'php', 'pot', 'pov', 'py3tb', 'pycon', 'pytb', 'python', 'python3', 'raw', 'ruby', 'rbcon', 'redcode', 'rhtml', 'restructuredtext',
'scala', 'scheme', 'smalltalk', 'smarty', 'sourceslist', 'splus', 'sql', 'sqlite3', 'squidconf', 'tcl', 'tcsh', 'latex', 'trac-wiki',
'vbnet', 'vim', 'xml+cheetah', 'xml+django', 'xml+ruby', 'xml+mako', 'xml+myghty', 'xml+php', 'xml+smarty', 'xml', 'xslt', 'yaml',
]

syntaxy = ""

def getAuthor():
    try:
        author = commands.getoutput('whoami')
    except:
        author = 'Anonim'
    return author


def checkSyntax(syn):
    if syn in syntaxes:
        pass
    else:
        print "WRONG SYNTAX"
        sys.exit(1)

def getTresc(input):
    if input:
        tresc = input
    else:
        print "Input is empty!"
        sys.exit(1)
    return tresc

for i in syntaxes:
    syntaxy = syntaxy + " " + i

usage = """
To paste something: 
$ echo 'something' | wklej -s syntax
$ cat file | wklej -s syntax
$ wklej -s syntax"""
parser = OptionParser(usage=usage)
parser.add_option("-s", "--syntax", dest="syntax", help="Choose one:" + syntaxy, default="text")
parser.add_option("-a", "--author", dest="author", help="", default=getAuthor())
parser.add_option("-p", "--private", action="store_true", dest="private", default=False)

def main(args=sys.argv):
    
    (options, args) = parser.parse_args()
    checkSyntax(options.syntax)

    tresc = getTresc(sys.stdin.read())
    
    rpc_srv = xmlrpclib.ServerProxy("http://wklej.org/xmlrpc/")
    

    if key:
        print options.private
        if options.private:
	        result = rpc_srv.auth_dodaj_prywatny_wpis(tresc, options.syntax, key)
        else:
	        result = rpc_srv.auth_dodaj_wpis(tresc, options.syntax, key)
    else:
        if options.private:
            result = rpc_srv.dodaj_prywatny_wpis(tresc, options.syntax, options.author)
        else:
            result = rpc_srv.dodaj_wpis(tresc, options.syntax, options.author)

    print "http://wklej.org%s" % result

    sys.exit(0)


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
