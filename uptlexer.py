import ply.lex as lex

reserved = {
    'program' : 'PROGRAM',
    'function' : 'FUNCTION',
    'int' : 'INTEGER',
    'bool' : 'BOOL',
    'void' : 'VOID',
    'var' : 'VAR',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'to' : 'TO',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'break' : 'BREAK',
    'print' : 'PRINT',
    'read' : 'READ',
    'return' : 'RETURN',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
}

literals = ['+','-','*','/', '%', '<', '>', '=', ',', ':', ';', '(', ')', '{', '}']

# List of token names.   This is always required
tokens = [
   'EXP',
   'EQUAL',
   'NOTEQUAL',
   'LESSEQUAL',
   'GREATEREQUAL',
   'ID',
   'INT',
 ] + list(reserved.values())

# Regular expression rules for simple tokens
t_EXP = r'\*\*'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_ignore  = ' \t'
t_ignore_COMMENT  = r'(\#.*|\(\*[\s\S]*?\*\))'

def t_ID(t):
    r'\b[a-zA-Z][a-zA-Z_0-9]*\b'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_INT(t):
    r'\b\d+\b'
    #r'[-+]?[0-9]+'
    t.value = int(t.value)    
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()