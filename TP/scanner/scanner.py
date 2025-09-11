import ply.lex as lex


# Palabras reservadas
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
    'funcion': 'FUNCION',
    'retornar': 'RETORNAR',
    'finFuncion': 'FINFUNCION',
    'procedimiento': 'PROCEDIMIENTO',
    'finProcedimiento': 'FINPROCEDIMIENTO',
    'agregar': 'AGREGAR',
    'quitar': 'QUITAR',
    'limpiar': 'LIMPIAR',
    'vacia': 'VACIA',
    'vulnerable': 'VULNERABLE',
    'seguro': 'SEGURO',
    'sqli': 'SQLI',
    'xss': 'XSS',
    'rce': 'RCE',
    'probar': 'PROBAR',
    'reportar': 'REPORTAR'
}

# Lista de tokens
tokens = [
    'FIN',
    'ID',
    'NUMERO',
    'TEXTO',
    'MAS', 'MENOS', 'POR', 'DIV',
    'IGUAL', 'DIF', 'MENOR', 'MAYOR', 'MENORIG', 'MAYORIG',
    'ASIGNAR',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'COMA'
] + list(reserved.values())

# Expresiones regulares simples
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIV       = r'/'
t_IGUAL     = r'=='
t_DIF       = r'!='
t_MENORIG   = r'<='
t_MAYORIG   = r'>='
t_MENOR     = r'<'
t_MAYOR     = r'>'
t_ASIGNAR   = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMA      = r','

# Tokens más complejos
def t_FIN(t):
    r'FIN\.'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TEXTO(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignorar espacios, tabs y saltos de línea
t_ignore = ' \t\r\n'


# Ignorar comentarios
def t_COMMENTLINE(t):
    r'//.*'
    pass

def t_COMMENTBLOCK(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    pass

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

