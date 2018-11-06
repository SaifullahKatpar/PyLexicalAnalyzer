import re
class Token(object):
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s(%s) at %s' % (self.type, self.val, self.pos)


class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos
class Lexer(object):
    def __init__(self, rules, skip_whitespace=True):
        self.rules = []
        for regex, type in rules:
            self.rules.append((re.compile(regex), type))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):
        if self.pos >= len(self.buf):
            return None
        if self.skip_whitespace:
            m = self.re_ws_skip.search(self.buf, self.pos)
            if m:
                self.pos = m.start()
            else:
                return None

        for regex, type in self.rules:
            m = regex.match(self.buf, self.pos)
            if m:
                tok = Token(type, m.group(), self.pos)
                self.pos = m.end()
                return tok

        # if we're here, no rule matched
        raise LexerError(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok
rules = [
    ('//.*$',		'COMMENT'),
    ('int|float|long',	'DTYPE'),
    ('[_a-zA-Z][_a-zA-Z0-9]*',    'IDENTIFIER'),
    ('([0-9]*[.])?[0-9]+',             'NUMBER'),
    ('\+\+',              'INC'),
    ('\-\-',              'DEC'),
    ('\+',              'PLUS'),
    ('\-',              'MINUS'),
    ('\*',              'MULTIPLY'),
    ('\/',              'DIVIDE'),
    ('\(',              'LP'),
    ('\)',              'RP'),
    ('==',               'EQUAL'),
    ('=',               'ASSIGN'),
    	 			
]

lx = Lexer(rules, skip_whitespace=True)
inp = input('>>')
while inp!= 'q':
    lx.input(inp)
    try:
         for tok in lx.tokens():
            print(tok)
    except LexerError as err:
         print('LexerError at position %s' % err.pos)
    print('\n\n')
    inp = input('>>')
