"""
Analizador Sintáctico (Parser) para el Lenguaje de Seguridad Educativo
Implementación corregida siguiendo las mejores prácticas de PLY
"""

import ply.yacc as yacc
from ..scanner import tokens
from . import builtins

# =============================================================================
# PRECEDENCIA DE OPERADORES
# =============================================================================
# Según la documentación de PLY, la precedencia se define como una tupla
precedence = (
    ('left', 'MAS', 'MENOS'),    # Suma y resta (misma precedencia)
    ('left', 'POR', 'DIV'),      # Multiplicación y división (mayor precedencia)
    ('left', 'IGUAL', 'DIF', 'MENOR', 'MAYOR', 'MENORIG', 'MAYORIG'),  # Comparaciones
    ('left', 'Y'),               # AND lógico
    ('left', 'O'),               # OR lógico
    ('right', 'NO'),             # NOT lógico (asociatividad derecha)
)

# =============================================================================
# REGLAS DE GRAMÁTICA - ESTRUCTURA DEL PROGRAMA
# =============================================================================

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

# =============================================================================
# REGLAS DE GRAMÁTICA - SENTENCIAS
# =============================================================================

def p_sentencia_asignacion_sin_tipo(p):
    'sentencia : ANOTAR ID ASIGNAR expresion'
    p[0] = ("asignar", p[2], p[4])

def p_sentencia_asignacion_con_tipo(p):
    'sentencia : ANOTAR tipo ID ASIGNAR expresion'
    p[0] = ("declarar_asignar", p[2], p[3], p[5])

def p_sentencia_asignacion_lista_vacia(p):
    'sentencia : ANOTAR LISTA MENOR tipo_base MAYOR ID ASIGNAR VACIA'
    p[0] = ("declarar_lista_vacia", p[4], p[6])

def p_sentencia_asignacion_lista_literal(p):
    'sentencia : ANOTAR LISTA MENOR tipo_base MAYOR ID ASIGNAR LBRACKET RBRACKET'
    p[0] = ("declarar_lista_vacia", p[4], p[6])

def p_sentencia_mostrar(p):
    'sentencia : MOSTRAR expresion'
    p[0] = ("mostrar", p[2])

def p_sentencia_evaluar(p):
    'sentencia : EVALUAR condicion PASA sentencias'
    p[0] = ("evaluar", p[2], p[4], None)

def p_sentencia_evaluar_con_else(p):
    'sentencia : EVALUAR condicion PASA sentencias SI NO PASA sentencias'
    p[0] = ("evaluar", p[2], p[4], p[7])

def p_sentencia_mientras(p):
    'sentencia : MIENTRAS condicion HACER sentencias'
    p[0] = ("mientras", p[2], p[4])

def p_sentencia_agregar(p):
    'sentencia : AGREGAR expresion A ID'
    p[0] = ("agregar", p[2], p[4])

def p_sentencia_quitar(p):
    'sentencia : QUITAR EN ID LBRACKET expresion RBRACKET'
    p[0] = ("quitar", p[3], p[5])

def p_sentencia_limpiar(p):
    'sentencia : LIMPIAR ID'
    p[0] = ("limpiar", p[2])

def p_sentencia_definicion_funcion(p):
    'sentencia : FUNCION tipo ID LPAREN parametros_opt RPAREN sentencias RETORNAR expresion FINFUNCION'
    p[0] = ("definir_funcion", p[2], p[3], p[5], p[7], p[9])

def p_sentencia_definicion_procedimiento(p):
    'sentencia : PROCEDIMIENTO ID LPAREN parametros_opt RPAREN sentencias FINPROCEDIMIENTO'
    p[0] = ("definir_procedimiento", p[2], p[4], p[6])

def p_sentencia_llamada_procedimiento(p):
    'sentencia : ID LPAREN argumentos_opt RPAREN'
    p[0] = ("llamada_procedimiento", p[1], p[3])

# =============================================================================
# REGLAS DE GRAMÁTICA - TIPOS DE DATOS
# =============================================================================

def p_tipo(p):
    '''tipo : NUMERO_TIPO
            | TEXTO_TIPO
            | VULNERABILIDAD_TIPO
            | BOOL_TIPO
            | LISTA MENOR tipo_base MAYOR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("lista", p[3])

def p_tipo_base(p):
    '''tipo_base : NUMERO_TIPO
                 | TEXTO_TIPO
                 | VULNERABILIDAD_TIPO
                 | BOOL_TIPO'''
    p[0] = p[1]

# =============================================================================
# REGLAS DE GRAMÁTICA - EXPRESIONES
# =============================================================================

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

def p_expresion_acceso_lista(p):
    'expresion : ID LBRACKET expresion RBRACKET'
    p[0] = ("acceso_lista", p[1], p[3])

def p_expresion_sqli(p):
    'expresion : SQLI'
    p[0] = ("texto", "sqli")

def p_expresion_xss(p):
    'expresion : XSS'
    p[0] = ("texto", "xss")

def p_expresion_rce(p):
    'expresion : RCE'
    p[0] = ("texto", "rce")

def p_expresion_vulnerable(p):
    'expresion : VULNERABLE'
    p[0] = ("bool", "vulnerable")

def p_expresion_seguro(p):
    'expresion : SEGURO'
    p[0] = ("bool", "seguro")

def p_expresion_probar(p):
    'expresion : PROBAR LPAREN expresion COMA expresion COMA expresion RPAREN'
    p[0] = ("probar", p[3], p[5], p[7])

def p_expresion_reportar(p):
    'expresion : REPORTAR LPAREN expresion RPAREN'
    p[0] = ("reportar", p[3])

def p_expresion_llamada_funcion(p):
    'expresion : ID LPAREN argumentos_opt RPAREN'
    p[0] = ("llamada_funcion", p[1], p[3])

def p_expresion_parentesis(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]

# =============================================================================
# REGLAS DE GRAMÁTICA - CONDICIONES Y OPERADORES LÓGICOS
# =============================================================================

def p_condicion_comparacion(p):
    '''condicion : expresion IGUAL expresion
                 | expresion DIF expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIG expresion
                 | expresion MAYORIG expresion'''
    p[0] = ("comparacion", p[2], p[1], p[3])

def p_condicion_logica_and(p):
    'condicion : condicion Y condicion'
    p[0] = ("y", p[1], p[3])

def p_condicion_logica_or(p):
    'condicion : condicion O condicion'
    p[0] = ("o", p[1], p[3])

def p_condicion_negacion(p):
    'condicion : NO condicion'
    p[0] = ("no", p[2])

def p_condicion_expresion(p):
    'condicion : expresion'
    p[0] = p[1]

# =============================================================================
# REGLAS DE GRAMÁTICA - FUNCIONES Y PROCEDIMIENTOS
# =============================================================================

def p_parametros_opt(p):
    '''parametros_opt : parametros
                      | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []

def p_parametros(p):
    '''parametros : parametro
                  | parametro COMA parametros'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parametro(p):
    'parametro : tipo ID'
    p[0] = (p[1], p[2])

def p_argumentos_opt(p):
    '''argumentos_opt : argumentos
                      | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_empty(p):
    'empty :'
    pass

# =============================================================================
# MANEJO DE ERRORES Y CONSTRUCCIÓN DEL PARSER
# =============================================================================

def p_error(p):
    if p:
        print(f"Error de sintaxis en token '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")

# Construir el analizador sintáctico
parser = yacc.yacc()
