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

# ---------------- 5) Programs Grammar -------------------------

def p_program(p):
   '''Program : ProgramHeader 
              | ProgramBody''' 

def p_ProgramHeader(p):
   '''ProgramHeader : PROGRAM ID ';' '''

def p_ProgramBody(p):
   '''ProgramBody : FuncDecls VarDecls Cmd'''

def p_FuncDecls(p):
   '''FuncDecls : empty 
              | Function FuncDecls'''

# ---------------- 4) Functions Grammar -------------------------

def p_Function(p):
   '''Function : FunctionHeader 
               | FunctionBody'''
   
def p_FunctionHeader(p):
   '''FunctionHeader : FunctionType FUNCTION ID '(' ParamList ')' ':' '''

def p_FunctionType(p):
   '''FunctionType : INTEGER 
                   | BOOL
                   | VOID'''
   
def p_FunctionBody(p):
   '''FunctionBody : '{' VarDecls CmdList '}' '''

def p_ParamList(p):
   '''ParamList : empty 
                | ParamList1'''

def p_ParamList1(p):
   '''ParamList1 : Param ',' ParamList1 
                 | Param'''
   
def p_Param(p):
   '''Param : ID ':' Type'''

# ---------------- 3) Commands Grammar -------------------------

def p_Cmd(p):
    '''Cmd : CmdAtrib 
           | CmdIf
           | CmdWhile
           | CmdFor
           | CmdBreak
           | CmdPrint
           | CmdReturn
           | CmdSeq
           '''

def p_CmdAtrib(p):
    '''CmdAtrib : ID 
                | Expr'''
    
def p_CmdIf(p):
    '''CmdIf : IF Expr ':' Cmd 
             | IF Expr ':' Cmd ELSE ':' '''
    
def p_CmdWhile(p):
    '''CmdWhile : WHILE Expr ':' Cmd '''

def p_CmdFor(p):
    '''CmdFor : FOR CmdAtrib TO Expr ':' Cmd '''

def p_CmdBreak(p):
    '''CmdBreak : BREAK '''

def p_CmdPrint(p):
    '''CmdPrint : PRINT '(' ExprList ')' '''
    
def p_CmdReturn(p):
    '''CmdReturn : RETURN Expr '''

def p_CmdSeq(p):
    '''CmdSeq : '{' CmdList '}' '''

def p_CmdList(p):
    '''CmdList : Cmd ';' CmdList 
               | Cmd'''

# ---------------- 2) Expressions Grammar -------------------------

def p_Expr(p):
    '''Expr : INT 
            | TRUE
            | FALSE
            | ID
            | Expr BinOp Expr
            | UnOp Expr
            | '(' Expr ')'
            | ID '(' ExprList ')'
            | READ '(' ')'
           '''
    
def p_BinOp(p):
    '''BinOp : '+' 
             | '-'
             | '*'
             | EXP
             | '%'
             | EQUAL
             | NOTEQUAL
             | '<'
             | '>'
             | LESSEQUAL
             | GREATEREQUAL
             | AND
             | OR
           '''

def p_UnOp(p):
    '''UnOp : '-' 
            | 'NOT' 
            '''
    
def p_ExprList(p):
    '''ExprList : 'empty' 
                | ExprList1 '''
    
def p_ExprList1(p):
    '''ExprList1 : Expr
                 | Expr ',' ExprList1 '''



# ---------------- 1) Declarations Grammar -------------------------

def p_VarDecls(p):
    '''VarDecls : empty 
                | VarDecl VarDecls'''
    

def p_VarDecl(p):
    '''VarDecl : VAR ID ':' Type ';' '''

def p_Type(p):
    '''Type : INTEGER 
                | BOOL'''


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

