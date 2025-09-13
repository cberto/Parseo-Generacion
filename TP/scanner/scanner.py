"""
Analizador Léxico (Scanner) para el Lenguaje de Seguridad Educativo
Implementación corregida siguiendo las mejores prácticas de PLY
"""

import ply.lex as lex

# =============================================================================
# PALABRAS RESERVADAS DEL LENGUAJE
# =============================================================================
reserved = {
    'INICIO': 'INICIO',
    'anotar': 'ANOTAR',
    'mostrar': 'MOSTRAR',
    'evaluar': 'EVALUAR',
    'si': 'SI',
    'pasa:': 'PASA',
    'no': 'NO',
    'mientras': 'MIENTRAS',
    'hacer': 'HACER',
    'y': 'Y',
    'o': 'O',
    'funcion': 'FUNCION',
    'retornar': 'RETORNAR',
    'finFuncion': 'FINFUNCION',
    'procedimiento': 'PROCEDIMIENTO',
    'finProcedimiento': 'FINPROCEDIMIENTO',
    'agregar': 'AGREGAR',
    'a': 'A',
    'quitar': 'QUITAR',
    'en': 'EN',
    'limpiar': 'LIMPIAR',
    'vacia': 'VACIA',
    'vulnerable': 'VULNERABLE',
    'seguro': 'SEGURO',
    'sqli': 'SQLI',
    'xss': 'XSS',
    'rce': 'RCE',
    'probar': 'PROBAR',
    'reportar': 'REPORTAR',
    'numero': 'NUMERO_TIPO',
    'texto': 'TEXTO_TIPO',
    'vulnerabilidad': 'VULNERABILIDAD_TIPO',
    'bool': 'BOOL_TIPO',
    'lista': 'LISTA'
}

# =============================================================================
# DEFINICIÓN DE TOKENS
# =============================================================================
tokens = [
    # Tokens especiales
    'FIN',              # Fin del programa (FIN.)
    'ID',               # Identificadores de variables/funciones
    'NUMERO',           # Números enteros
    'TEXTO',            # Cadenas de texto entre comillas
    
    # Operadores aritméticos
    'MAS',              # Suma (+)
    'MENOS',            # Resta (-)
    'POR',              # Multiplicación (*)
    'DIV',              # División (/)
    
    # Operadores de comparación
    'IGUAL',            # Igualdad (==)
    'DIF',              # Desigualdad (!=)
    'MENOR',            # Menor que (<)
    'MAYOR',            # Mayor que (>)
    'MENORIG',          # Menor o igual (<=)
    'MAYORIG',          # Mayor o igual (>=)
    
    # Operadores de asignación y agrupación
    'ASIGNAR',          # Asignación (=)
    'LPAREN',           # Paréntesis izquierdo (()
    'RPAREN',           # Paréntesis derecho ())
    'LBRACKET',         # Corchete izquierdo ([)
    'RBRACKET',         # Corchete derecho (])
    'COMA',             # Separador de argumentos (,)
] + list(reserved.values())

# =============================================================================
# EXPRESIONES REGULARES PARA SÍMBOLOS SIMPLES
# =============================================================================
# Según la documentación de PLY, los tokens simples se definen como variables
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_IGUAL = r'=='
t_DIF = r'!='
t_MENORIG = r'<='
t_MAYORIG = r'>='
t_MENOR = r'<'
t_MAYOR = r'>'
t_ASIGNAR = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMA = r','

# =============================================================================
# CARACTERES IGNORADOS
# =============================================================================
# Espacios, tabs y saltos de línea
t_ignore = ' \t\r\n'

# =============================================================================
# FUNCIONES DE RECONOCIMIENTO DE TOKENS COMPLEJOS
# =============================================================================

def t_FIN(t):
    r'FIN\.'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TEXTO(t):
    r'\"([^"\\\n]|(\\.))*\"'
    t.value = t.value[1:-1]  # Quitar las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENTLINE(t):
    r'//.*'
    pass  # No retorna nada, se ignora

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error léxico: Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

# =============================================================================
# CONSTRUCCIÓN DEL LEXER
# =============================================================================
lexer = lex.lex()
