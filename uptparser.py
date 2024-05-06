import ply.yacc as yacc
from uptlexer import tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    #('', 'NOT'),
    ('nonassoc', 'EQUAL', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUAL', 'GREATEREQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'EXP'),
    ('right', 'UMINUS'),
)

start = 'Program'

# ---------------- 5) Programs -------------------------
def p_program(p):
   '''Program : ProgramHeader 
              | ProgramBody''' 

def p_ProgramHeader(p):
   'ProgramHeader : PROGRAM ID SEMICOLON' 

def p_ProgramBody(p):
   'ProgramBody : FuncDecls VarDecls Cmd' 

def p_FuncDecls(p):
   '''FuncDecls : empty 
              | Function FuncDecls'''

# ---------------- 4) Functions -------------------------
def p_Function(p):
   '''Function : FunctionHeader 
               | FunctionBody'''
   
def p_FunctionHeader(p):
   '''FunctionHeader : FunctionType FUNCTION ID LPAREN ParamList RPAREN COLON 
               | FunctionBody'''

# 1) Declarations
def p_VarDecls(p):
    '''VarDecls : empty 
                | VarDecl VarDecls'''
    
    p[0] = ('declaration', p[1], p[3])

# def p_expression_plus(p):
#     'expression : expression PLUS INT'
#     p[0] = p[1] + p[3]

# def p_expression_minus(p):
#     'expression : expression MINUS expression'
#     p[0] = p[1] - p[3]

# def p_expression_times(p):
#     'expression : expression TIMES expression'
#     p[0] = p[1] * p[3]

# def p_expression_divide(p):
#     'expression : expression DIVIDE expression'
#     if p[3] == 0:
#         raise ZeroDivisionError("division by zero")
#     p[0] = p[1] / p[3]

# def p_expression_group(p):
#     'expression : LPAREN expression RPAREN'
#     p[0] = p[2]

# def p_expression_number(p):
#     'expression : NUMBER'
#     p[0] = p[1]

def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

# Test the parser
while True:
    try:
        s = input('x = 3 + 4')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)

