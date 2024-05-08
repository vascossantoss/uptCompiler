import ply.yacc as yacc
from uptlexer import tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQUAL', 'NOTEQUAL', '<', '>', 'LESSEQUAL', 'GREATEREQUAL'),
    ('left', '+', '-'),
    ('left', '*', 'DIVIDE' , '%'),
    ('right', 'EXP'),
    ('right', 'UMINUS'),
)

start = 'Program'

# ---------------- 5) Programs Grammar -------------------------

def p_program(p):
   '''
   Program : ProgramHeader ProgramBody
   ''' 
   p[0] = ('program', p[1], p[2])

def p_ProgramHeader(p):
   '''
   ProgramHeader : PROGRAM ID ';' 
   '''
   p[0] = ('programHeader', p[1], p[2])

def p_ProgramBody(p):
   '''
   ProgramBody : FuncDecls VarDecls Cmds
   '''
   p[0] = ('programBody', p[1], p[2], p[3])

def p_FuncDecls(p):
   '''
   FuncDecls : empty 
             | Function FuncDecls
   '''
   if len(p) == 3:
    p[0] = ('FuncDecls', p[1], p[2])

# ---------------- 4) Functions Grammar -------------------------

def p_Function(p):
   '''
   Function : FunctionHeader 
            | FunctionBody
   '''
   p[0] = ('Function', p[1], p[2])
   
def p_FunctionHeader(p):
   '''
   FunctionHeader : FunctionType FUNCTION ID '(' ParamList ')' ':' 
   '''
   p[0] = ('FunctionHeader', p[1], p[2], p[3], p[5])

def p_FunctionType(p):
   '''
   FunctionType : INTEGER 
                | BOOL
                | VOID
   '''
   p[0] = ('FunctionType', p[1])
   
def p_FunctionBody(p):
   '''
   FunctionBody : '{' VarDecls CmdList '}' 
   '''
   p[0] = ('FunctionBody', p[2], p[3])

def p_ParamList(p):
   '''
   ParamList : empty 
             | ParamList1
   '''
   p[0] = ('ParamList', p[1])

def p_ParamList1(p):
   '''
   ParamList1 : Param ',' ParamList1 
              | Param
   '''
   if len(p) == 4:
    p[0] = ('ParamList1', p[1], p[3])
   else:
       p[0] = ('ParamList1', p[1])
       
   
def p_Param(p):
   '''
   Param : ID ':' Type
   '''
   p[0] = ('Param', p[1], p[3])

# ---------------- 3) Commands Grammar -------------------------

def p_Cmds(p):
    '''
    Cmds : CmdSeq
         | Cmd
    '''
    p[0] = ('cmds', p[1])

def p_Cmd(p):
    '''
    Cmd : CmdAtrib 
        | CmdIf
        | CmdWhile
        | CmdFor
        | CmdBreak
        | CmdPrint
        | CmdReturn
        | CmdSeq
    '''
    p[0] = p[1]

def p_CmdAtrib(p):
    '''
    CmdAtrib : ID '=' Expr
    '''
    p[0] = ('CmdAtrib', p[1], p[2], p[3])

def p_CmdIf(p):
    '''
    CmdIf : IF Expr ':' Cmd 
          | IF Expr ':' Cmd ELSE ':' 
    '''
    p[0] = ('CmdIf', p[1], p[2], p[4])
    
def p_CmdWhile(p):
    '''
    CmdWhile : WHILE Expr ':' Cmds 
    '''
    p[0] = ('CmdWhile', p[1], p[2], p[4])

def p_CmdFor(p):
    '''
    CmdFor : FOR CmdAtrib TO Expr ':' Cmd 
    '''
    p[0] = ('CmdFor', p[1], p[2], p[4])

def p_CmdBreak(p):
    '''
    CmdBreak : BREAK 
    '''
    p[0] = ('CmdBreak', p[1])

def p_CmdPrint(p):
    '''
    CmdPrint : PRINT '(' ExprList ')' 
    '''
    p[0] = ('CmdPrint', p[1], p[3])
    
def p_CmdReturn(p):
    '''
    CmdReturn : RETURN Expr 
    '''
    p[0] = ('CmdReturn', p[1], p[2])

def p_CmdSeq(p):
    '''
    CmdSeq : '{' CmdList '}' 
    '''
    p[0] = ('CmdSeq', p[2])

def p_CmdList(p):
    '''
    CmdList : Cmd ';' CmdList 
            | Cmd
    '''
    if len(p) == 4:
        p[0] = ('cmdList', p[1], p[3])
    else:
        p[0] = ('cmdList', p[1])

# ---------------- 2) Expressions Grammar -------------------------

def p_Expr(p):
    '''
    Expr : INT 
         | TRUE
         | FALSE
         | ID
         | Expr BinOp Expr
         | UnOp Expr  %prec UMINUS
         | '(' Expr ')'
         | ID '(' ExprList ')'
         | READ '(' ')'
    '''
     
    if p[1] == '-':
        p[0] = ('UnOp', -p[2])
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ('Group', p[2])
        elif p[2] == '(':
            p[0] = ('Read')
        else:
            p[0] = ('BinOp', p[1], p[2], p[3])
    else: 
        p[0] = ('FunctionCall', p[1], p[3])

def p_BinOp(p):
    '''
    BinOp : '+' 
          | '-'
          | '*'
          | DIVIDE
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
    p[0] = p[1]

def p_UnOp(p):
    '''
    UnOp : '-' 
         | NOT 
    '''
    p[0] = p[1]
      
def p_ExprList(p):
    '''
    ExprList : empty 
             | ExprList1 
    '''
    p[0] = ('exprList', p[1])
    
def p_ExprList1(p):
    '''
    ExprList1 : Expr
              | Expr ',' ExprList1 
    '''
    if len(p) == 4:
        p[0] = ('exprList1', p[1], p[3])
    else:
        p[0] = ('exprList1', p[1])

# ---------------- 1) Declarations Grammar -------------------------

def p_VarDecls(p):
    '''
    VarDecls : empty 
             | VarDecl VarDecls
    '''
    if len(p) == 3:
        p[0] = ('VarDecls', p[1], p[2])

def p_VarDecl(p):
    '''
    VarDecl : VAR ID ':' Type ';' 
    '''
    p[0] = ('VarDecl', p[2], p[4])

def p_Type(p):
    '''
    Type : INTEGER 
         | BOOL
    '''
    p[0] = ('Type', p[1])

# ---------------- 1) Other Grammar -------------------------

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)

# ---------------- Test the parser by printing the AST -------------------------

parser = yacc.yacc()

ast = parser.parse('program count; var i: int; { i = 1; while i <= 10: {print(i); i = i + 1}}')
print(ast)


# --------------------------------------Ignore code below----------------------------------------------------------------

# def p_expr_uminus(p):
#     'expression : MINUS expression %prec UMINUS'
#     p[0] = -p[2]

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

# # Test the parser
# while True:
#     try:
#         s = input('program count; var i: int; { i = 1; while i <= 10: {print(i); i = i + 1}}')
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser.parse(s)
#     print(result)

# other way to test the parser
# parser = yacc.yacc( debug=True)
# try:
#     input = open("input3.txt", "r") 
# except EOFError:
#     print("End of file Error")
# result = parser.parse(input.read())



# if result is not None:
#         print(result) 