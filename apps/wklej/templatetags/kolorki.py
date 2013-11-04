#-*- coding: utf-8 -*-

from pygments import highlight
from pygments.lexers import get_lexer_by_name, RstLexer
from pygments.formatters import HtmlFormatter

from django import template
register = template.Library()


@register.tag(name='code')
def do_code(parser, token):
    code = token.split_contents()[-1]
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(code, nodelist)


class CodeNode(template.Node):
    def __init__(self, lang, code):
        self.lang = lang
        self.nodelist = code

    def render(self, context):
        try:
            language = template.Variable(self.lang).resolve(context)
        except:
            language = self.lang

        code = self.nodelist.render(context)
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = RstLexer()

        # just before return, add chosen lexer as a template variable:
        return highlight(code, lexer, HtmlFormatter(
            linenos="pre",
            cssclass="syntax",
            anchorlines=True,
            #linenospecial='2',
            #hl_lines=[1,5,6,2,4,12],
        ))
