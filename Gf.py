# -*- coding: utf-8 -*-
"""
    pygments.lexers.GF
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
 LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, include, do_insertions
from pygments.token import Text, Comment, Operator, Keyword, Name, \
     String, Number, Punctuation, Literal, Generic


__all__ = ['GfLexer']



class GfLexer(RegexLexer):
    """
    A GF lexer.

    """
    name = 'GF'
    aliases = ['gf', 'Gf']
    filenames = ['*.gf']
    mimetypes = ['text/x-gf']

    reserved = ['cat','fun','lin','lincat','def','let','in',
                'variant', 'data', 'oper','_']
    
    tokens = {
        'root': [
            # Whitespace:
            (r'\s+', Text),
            #(r'--\s*|.*$', Comment.Doc),
            (r'--(?![!#$%&*+./<=>?@\^|_~]).*?$', Comment.Single),
            (r'{-', Comment.Multiline, 'comment'),
            # Lexemes:
            #  Identifiers
            (r'\babstract\b', Keyword.Reserved, 'module'),
            (r'\bconcrete\b', Keyword.Reserved, 'module'),
            (r'\berror\b', Name.Exception),
            (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
            (r'^[_a-z][\w\']*', Name.Function),
            (r'[_a-z][\w\']*', Name),
            (r'[A-Z][\w\']*', Keyword.Type),
            #  Operators
            (r'\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Name.Function), # lambda operator
            (r'(<-|::|->|=>|=)(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word), # specials
            (r':[:!#$%&*+.\\/<=>?@^|~-]*', Keyword.Type), # Constructor operators
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator), # Other operators
            #  Numbers
            (r'\d+[eE][+-]?\d+', Number.Float),
            (r'\d+\.\d+([eE][+-]?\d+)?', Number.Float),
            (r'0[oO][0-7]+', Number.Oct),
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'\d+', Number.Integer),
            #  Character/String Literals
            (r"'", String.Char, 'character'),
            (r'"', String, 'string'),
            #  Special
            (r'\[\]', Keyword.Type),
            (r'\(\)', Name.Builtin),
            (r'[][(),;`{}]', Punctuation),
        ],
        'import': [
            # Import statements
            (r'\s+', Text),
            (r'"', String, 'string'),
            # after "funclist" state
            (r'\)', Punctuation, '#pop'),
            (r'qualified\b', Keyword),
            # import X as Y
            (r'([A-Z][a-zA-Z0-9_.]*)(\s+)(as)(\s+)([A-Z][a-zA-Z0-9_.]*)',
             bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
            # import X hiding (functions)
            (r'([A-Z][a-zA-Z0-9_.]*)(\s+)(hiding)(\s+)(\()',
             bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
            # import X (functions)
            (r'([A-Z][a-zA-Z0-9_.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            # import X
            (r'[a-zA-Z0-9_.]+', Name.Namespace, '#pop'),
        ],
        'module': [
            (r'\s+', Text),
            (r'([A-Z][a-zA-Z0-9_.]*)(\s+)(\()',
             bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
            (r'[A-Z][a-zA-Z0-9_.]*', Name.Namespace, '#pop'),
        ],
        'funclist': [
            (r'\s+', Text),
            (r'[A-Z][a-zA-Z0-9_]*', Keyword.Type),
            (r'[_a-z][\w\']+', Name.Function),
            (r'--.*$', Comment.Single),
            (r'{-', Comment.Multiline, 'comment'),
            (r',', Punctuation),
            (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
            # (HACK, but it makes sense to push two instances, believe me)
            (r'\(', Punctuation, ('funclist', 'funclist')),
            (r'\)', Punctuation, '#pop:2'),
        ],
        'comment': [
            # Multiline Comments
            (r'[^-{}]+', Comment.Multiline),
            (r'{-', Comment.Multiline, '#push'),
            (r'-}', Comment.Multiline, '#pop'),
            (r'[-{}]', Comment.Multiline),
        ],
        'character': [
            # Allows multi-chars, incorrectly.
            (r"[^\\']", String.Char),
            (r"\\", String.Escape, 'escape'),
            ("'", String.Char, '#pop'),
        ],
        'string': [
            (r'[^\\"]+', String),
            (r"\\", String.Escape, 'escape'),
            ('"', String, '#pop'),
        ],
        'escape': [
            (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
            (r'\^[][A-Z@\^_]', String.Escape, '#pop'),
            (r'o[0-7]+', String.Escape, '#pop'),
            (r'x[\da-fA-F]+', String.Escape, '#pop'),
            (r'\d+', String.Escape, '#pop'),
            (r'\s+\\', String.Escape, '#pop'),
        ],
    }


line_re = re.compile('.*?\n')
bird_re = re.compile(r'(>[ \t]*)(.*\n)')

