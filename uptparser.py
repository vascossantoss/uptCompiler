import ply.yacc as yacc
from uptlexer import tokens

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Symbol '{name}' already declared")
        self.symbols[name] = var_type

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Symbol '{name}' not declared")
        return self.symbols[name]

def check_expr(expr,symtab):
    if expr[0] == 'INT':
        return symtab[expr[1]] # Atributo sintetizado
    elif expr[0] == '+':
        t1 = check_expr(expr[1],symtab)
        t2 = check_expr(expr[2],symtab)
        if t1 == 'INT' and t2 == 'INT':
            return 'INT'
        else:
            raise Exception('Erro de tipos na soma')

# # Semantic analysis structures
# symbol_table = {}
# functions_table = {}

# Symbol table instance
symtab = SymbolTable()

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQUAL', 'NOTEQUAL', '<', '>', 'LESSEQUAL', 'GREATEREQUAL'),
    ('left', '+', '-'),
    ('left', '*', '/' , '%'),
    ('right', 'EXP'),
    ('right', 'UMINUS'),
)

start = 'Program'

# ---------------- 5) Programs Grammar --------------------------------------

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
   ProgramBody : FuncDecls VarDecls Cmd
   '''
   p[0] = ('programBody', p[1], p[2], p[3])

def p_FuncDecls(p):
   '''
   FuncDecls : empty 
             | Function FuncDecls
   '''
   if len(p) == 3:
    p[0] = ('FuncDecls', p[1], p[2])
   else:
       p[0] = ('FuncDecls', p[1])

# ---------------- 4) Functions Grammar -------------------------

def p_Function(p):
   '''
   Function : FunctionHeader  FunctionBody
   '''
   p[0] = ('Function', p[1], p[2])
   
def p_FunctionHeader(p):
   '''
   FunctionHeader : FunctionType FUNCTION ID '(' ParamList ')' ':' 
   '''
   symtab.declare(p[3], p[1])  # Declare function in symbol table
   p[0] = ('FunctionHeader', p[1], p[3], p[5])

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
    CmdAtrib : ID 
             | Expr
    '''
    p[0] = ('CmdAtrib', p[1])

# grammar was changed
# restrict the "then" part to be a block: "{ ... }". (best option for your project?)
def p_CmdIf(p):
    '''
    CmdIf : IF Expr ':' Cmd 
          | IF Expr ':' Cmd ELSE ':' 
    '''
    if len(p) == 5:
        p[0] = ('CmdIf', p[2], p[4])
    else:
        p[0] = ('CmdIf', p[2], p[4], p[7])
    
def p_CmdWhile(p):
    '''
    CmdWhile : WHILE Expr ':' Cmd 
    '''
    p[0] = ('CmdWhile', p[2], p[4])

def p_CmdFor(p):
    '''
    CmdFor : FOR CmdAtrib TO Expr ':' Cmd 
    '''
    p[0] = ('CmdFor', p[2], p[4], p[6])

def p_CmdBreak(p):
    '''
    CmdBreak : BREAK 
    '''
    p[0] = ('CmdBreak', p[1])

def p_CmdPrint(p):
    '''
    CmdPrint : PRINT '(' ExprList ')' 
    '''
    p[0] = ('CmdPrint', p[3])
    
def p_CmdReturn(p):
    '''
    CmdReturn : RETURN Expr 
    '''
    p[0] = ('CmdReturn', p[2])

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
            p[0] = ('BinOp', p[2], p[1], p[3])
            check_expr(p[0],symtab)
            if p[2] == '/' and p[3] == 0:
                raise Exception("Semantic error: Division by zero")
    else: 
        symtab.lookup(p[1])
        p[0] = ('FunctionCall', p[1], p[3])

def p_BinOp(p):
    '''
    BinOp : '+' 
          | '-'
          | '*'
          | '/'
          | EXP
          | '%'
          | '='
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
    else:
        p[0] = ('VarDecls', p[1])

def p_VarDecl(p):
    '''
    VarDecl : VAR ID ':' Type ';' 
    '''
    symtab.declare(p[2], p[4])  # Register the variable in the symbol table
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

ast = parser.parse('program fact_rec ;int function fact( x: int ): {var p : int;p = 1 ;while x > 1:{ p = p * x; x = x - 1}; return p} var n : int;{ n = read();print(fact(n))}')
print(ast)

# ----------------- Valid UPT Code for testing ----------------------------------------------

# program count; var i: int; { i = 1; while i<= 10 : {print(i); i = i + 1}} 

# program count_for; for i = 1 to 10 : print(i)

# program square_sum ; var s : int; var n : int; var max : int; { max = read(); n = 1; while n <= max:{s = s + n*n; n = n + 1};print(s)}

# program fact_iter ; var p : int ; var n : int ; { p = 1;n = read();while (n > 0):{p = p * n; n = n - 1};print(p)}

# program fact_rec ;int function fact( x: int ): {var p : int;p = 1 ;while x > 1:{ p = p * x; x = x - 1}; return p} var n : int;{ n = read();print(fact(n))}

# ----------------- Invalid UPT Code for testing ----------------------------------------------

# program error1 { var x : int; x = 1; print(x)}

# program error2 ; { var x : int; x = 1; print(x)}

# program error3; var x : int; void dummy ( ) : { print (1) } { x = 1; print(x) } 

# program error4 ; int dummy () : { print (1) } var x : int { x = 1; print(x)};
