from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from twisted.web.template import XMLString, Element, renderer, tags, renderElement

import sys

from parsley import makeGrammar

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


class Main(Resource):

    def __init__(self):
        Resource.__init__(self)

    def render(self, request):
        return renderElement(request, Page())


class Page(Element):
    def __init__(self):
        self.loader = XMLString('''
                                <div xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">
                                Output:
                                <div t:render="header"></div>
                                </div>
                                ''')

    @renderer
    def header(self, request, tag):
        text = """
        blah

        blah
        *blah*
        """

        BlogGrammar = makeGrammar(blog_grammar, {"tags": tags})
        #output = BlogGrammar("*Hello!*").paragraphs()
        output = BlogGrammar(text).paragraphs()
        return tag(output)


log.startLogging(sys.stdout)
root = Main()
root.putChild('', root)
reactor.listenTCP(8084, Site(root))
reactor.run()
