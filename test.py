from parsley import makeGrammar
from twisted.web.template import tags

blog_grammar = """
crlf = '\r' '\n' -> tags.br()
not_crlf = ~crlf anything
crlfs = crlf

single_star = '*' ~'*'
double_star = '*' '*'

bold = double_star (~double_star nested_decos)+:b double_star -> tags.b(*b)

italics = single_star (~single_star nested_decos)+:i single_star -> tags.i(*i)

underline = '_' (~'_' nested_decos)+:u '_' -> tags.u(*u)

decorations = bold | italics | underline

nested_decos = decorations | not_crlf

entities = crlfs | decorations

paragraphs = (entities | anything)*:l -> tags.p(*l)
"""

#BlogGrammar = makeGrammar(blog_grammar, {"tags": tags})
BlogGrammar = makeGrammar(blog_grammar, {"tags": tags})

g = BlogGrammar("**Hello, world!**")
#result, error = g.paragraphs(tags)
print g.paragraphs()
