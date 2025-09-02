import ply.yacc as yacc
from ..scanner import tokens
from . import builtins

# Precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
)

# Programa
def p_programa(p):
    'programa : INICIO sentencias FIN'
    p[0] = ("programa", p[2])

def p_sentencias(p):
    '''sentencias : sentencia sentencias
                  | sentencia'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_sentencia_asignacion(p):
    'sentencia : ANOTAR ID ASIGNAR expresion'
    p[0] = ("asignar", p[2], p[4])

def p_sentencia_mostrar(p):
    'sentencia : MOSTRAR expresion'
    p[0] = ("mostrar", p[2])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion'''
    p[0] = ("binop", p[2], p[1], p[3])

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = ("num", p[1])

def p_expresion_texto(p):
    'expresion : TEXTO'
    p[0] = ("texto", p[1])

def p_expresion_id(p):
    'expresion : ID'
    p[0] = ("var", p[1])

def p_expresion_sqli(p):
    'expresion : SQLI'
    p[0] = ("texto", "sqli")

def p_expresion_xss(p):
    'expresion : XSS'
    p[0] = ("texto", "xss")

def p_expresion_rce(p):
    'expresion : RCE'
    p[0] = ("texto", "rce")

def p_expresion_probar(p):
    'expresion : PROBAR LPAREN expresion COMA expresion COMA expresion RPAREN'
    p[0] = ("probar", p[3], p[5], p[7])

def p_expresion_reportar(p):
    'expresion : REPORTAR LPAREN expresion RPAREN'
    p[0] = ("reportar", p[3])

def p_error(p):
    print("Error de sintaxis", p)

parser = yacc.yacc()
