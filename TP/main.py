"""
Intérprete principal del lenguaje de seguridad educativo.

Secuencia de ejecución:
1. El código fuente se tokeniza con `scanner.lexer`.
2. El parser (`scanner.addons.parser`) construye un AST.
3. Las funciones `ejecutar` y `evaluar` recorren el AST y mantienen el estado
   en estructuras globales:
   - `variables_globales`: valores de las variables declaradas.
   - `tipos_de_variables`: tipos asociados a cada identificador.
   - `tabla_funciones`: definiciones de funciones disponibles.
   - `tabla_procedimientos`: definiciones de procedimientos disponibles.

La interpretación se realiza en memoria: cada sentencia produce efectos sobre
estas estructuras y las llamadas a funciones/procedimientos crean contextos
locales que se guardan y restauran automáticamente.
"""

from scanner import lexer
from scanner.addons.parser import parser
import scanner.addons.builtins as builtins

def ejecutar(ast):
    """Despacha la ejecución de cada nodo del AST según su tipo."""
    if not ast:
        return
    # Un nodo siempre es una tupla (tipo, datos...), por ejemplo:
    # ("asignar", "variable", ("num", 10)).
    tipo_nodo = ast[0]

    if tipo_nodo == "programa":
        # El nodo raíz contiene la secuencia completa de sentencias.
        for sentencia in ast[1]:
            ejecutar(sentencia)

    elif tipo_nodo == "asignar":
        _, identificador, expresion = ast
        valor = evaluar(expresion)
        variables_globales[identificador] = valor

    elif tipo_nodo == "declarar_asignar":
        _, tipo_variable, identificador, expresion = ast
        valor = evaluar(expresion)
        variables_globales[identificador] = valor
        tipos_de_variables[identificador] = tipo_variable

    elif tipo_nodo == "declarar_lista_vacia":
        _, tipo_base, identificador = ast
        variables_globales[identificador] = []
        tipos_de_variables[identificador] = ("lista", tipo_base)

    elif tipo_nodo == "mostrar":
        # Evalúa la expresión y la imprime en consola.
        _, expresion = ast
        valor = evaluar(expresion)
        print(valor)

    elif tipo_nodo == "evaluar":
        _, condicion, bloque_si, bloque_no = ast
        if evaluar_condicion(condicion):
            for sentencia in bloque_si:
                ejecutar(sentencia)
        elif bloque_no:
            for sentencia in bloque_no:
                ejecutar(sentencia)

    elif tipo_nodo == "mientras":
        _, condicion, bloque = ast
        while evaluar_condicion(condicion):
            for sentencia in bloque:
                ejecutar(sentencia)

    elif tipo_nodo == "agregar":
        _, expresion_valor, nombre_lista = ast
        valor = evaluar(expresion_valor)
        if nombre_lista in variables_globales and isinstance(variables_globales[nombre_lista], list):
            variables_globales[nombre_lista].append(valor)
        else:
            print(f"Error: '{nombre_lista}' no es una lista")

    elif tipo_nodo == "quitar":
        _, nombre_lista, expresion_indice = ast
        indice = evaluar(expresion_indice)
        if nombre_lista in variables_globales and isinstance(variables_globales[nombre_lista], list):
            if 0 <= indice < len(variables_globales[nombre_lista]):
                variables_globales[nombre_lista].pop(indice)
            else:
                print(f"Error: Índice {indice} fuera de rango en lista '{nombre_lista}'")
        else:
            print(f"Error: '{nombre_lista}' no es una lista")

    elif tipo_nodo == "limpiar":
        _, nombre_lista = ast
        if nombre_lista in variables_globales and isinstance(variables_globales[nombre_lista], list):
            variables_globales[nombre_lista].clear()
        else:
            print(f"Error: '{nombre_lista}' no es una lista")

    elif tipo_nodo == "definir_funcion":
        _, tipo_retorno, nombre, parametros, cuerpo, expresion_retorno = ast
        # Se almacena la firma completa para resolver llamadas posteriores.
        tabla_funciones[nombre] = ("funcion", tipo_retorno, parametros, cuerpo, expresion_retorno)

    elif tipo_nodo == "definir_procedimiento":
        _, nombre, parametros, cuerpo = ast
        tabla_procedimientos[nombre] = ("procedimiento", parametros, cuerpo)

    elif tipo_nodo == "llamada_procedimiento":
        _, nombre, argumentos = ast
        if nombre in tabla_procedimientos:
            # Los procedimientos no devuelven valor; solo generan efectos.
            ejecutar_procedimiento(nombre, argumentos)
        else:
            print(f"Error: Procedimiento '{nombre}' no definido")

def evaluar(expr):
    """Evalúa una expresión y devuelve su resultado en tiempo de ejecución."""
    etiqueta = expr[0]

    if etiqueta == "num": return expr[1]
    if etiqueta == "texto": return expr[1]
    if etiqueta == "var": return variables_globales.get(expr[1], None)
    if etiqueta == "bool": return expr[1]

    if etiqueta == "acceso_lista":
        _, nombre_lista, expresion_indice = expr
        indice = evaluar(expresion_indice)
        if nombre_lista in variables_globales and isinstance(variables_globales[nombre_lista], list):
            if 0 <= indice < len(variables_globales[nombre_lista]):
                return variables_globales[nombre_lista][indice]
            else:
                print(f"Error: Índice {indice} fuera de rango en lista '{nombre_lista}'")
                return None
        else:
            print(f"Error: '{nombre_lista}' no es una lista")
            return None

    if etiqueta == "binop":
        _, operador, expresion_izquierda, expresion_derecha = expr
        operando_izquierdo = evaluar(expresion_izquierda)
        operando_derecho = evaluar(expresion_derecha)
        if operador == "+": 
            # Concatenación de texto o suma numérica
            if isinstance(operando_izquierdo, str) or isinstance(operando_derecho, str):
                return str(operando_izquierdo) + str(operando_derecho)
            return operando_izquierdo + operando_derecho
        if operador == "-": return operando_izquierdo - operando_derecho
        if operador == "*": return operando_izquierdo * operando_derecho
        if operador == "/": 
            if operando_derecho == 0:
                print("Error: División por cero")
                return 0
            return operando_izquierdo / operando_derecho
        # Nota: si llega hasta aquí la operación no está soportada.

    if etiqueta == "probar":
        _, url, tipo, payload = expr
        # Builtin que simula una prueba de seguridad y devuelve un bool.
        return builtins.fn_probar(evaluar(url), evaluar(tipo), evaluar(payload))

    if etiqueta == "reportar":
        _, msg = expr
        # Builtin que genera un reporte; se mantiene para efectos secundarios.
        return builtins.fn_reportar(evaluar(msg))

    if etiqueta == "llamada_funcion":
        _, nombre, argumentos = expr
        if nombre in tabla_funciones:
            return ejecutar_funcion(nombre, argumentos)
        else:
            print(f"Error: Función '{nombre}' no definida")
            return None

def evaluar_condicion(condicion):
    """Evalúa una condición lógica"""
    if not condicion:
        return False
    
    # Las condiciones comparten la misma convención que las expresiones:
    # en la primera posición se indica el tipo de operación a realizar.
    tipo = condicion[0]
    
    if tipo == "comparacion":
        _, op, izq, der = condicion
        l = evaluar(izq)
        r = evaluar(der)
        if op == "==": return l == r
        if op == "!=": return l != r
        if op == "<": return l < r
        if op == ">": return l > r
        if op == "<=": return l <= r
        if op == ">=": return l >= r
    
    elif tipo == "y":
        _, cond1, cond2 = condicion
        return evaluar_condicion(cond1) and evaluar_condicion(cond2)
    
    elif tipo == "o":
        _, cond1, cond2 = condicion
        return evaluar_condicion(cond1) or evaluar_condicion(cond2)
    
    elif tipo == "no":
        _, cond = condicion
        return not evaluar_condicion(cond)
    
    elif tipo == "bool":
        return condicion[1] == "vulnerable"
    
    else:
        # Si es una expresión simple (por ejemplo una variable), se evalúa
        # reutilizando la lógica general y se normaliza el resultado a bool.
        val = evaluar(condicion)
        if isinstance(val, str):
            return val == "vulnerable"
        return bool(val)

def ejecutar_funcion(nombre, argumentos):
    """Ejecuta una función definida por el usuario"""
    if nombre not in tabla_funciones:
        print(f"Error: Función '{nombre}' no definida")
        return None
    
    _, tipo_retorno, parametros, cuerpo, expresion_retorno = tabla_funciones[nombre]
    
    # Crear contexto local
    variables_locales = {}
    tipos_locales = {}
    
    # Asignar argumentos a parámetros
    if len(argumentos) != len(parametros):
        print(f"Error: Número incorrecto de argumentos para función '{nombre}'")
        return None
    
    for i, (tipo_param, nombre_param) in enumerate(parametros):
        valor_argumento = evaluar(argumentos[i])
        variables_locales[nombre_param] = valor_argumento
        tipos_locales[nombre_param] = tipo_param
    
    # Guardar contexto global
    variables_previas = variables_globales.copy()
    tipos_previos = tipos_de_variables.copy()
    
    # Establecer contexto local
    variables_globales.clear()
    variables_globales.update(variables_locales)
    tipos_de_variables.clear()
    tipos_de_variables.update(tipos_locales)
    # A partir de aquí todo acceso a variables se realiza sobre el contexto
    # recién creado hasta que la función finalice.
    
    # Ejecutar cuerpo de la función
    for sentencia in cuerpo:
        ejecutar(sentencia)
    
    # Evaluar expresión de retorno
    valor_retorno = evaluar(expresion_retorno)
    
    # Restaurar contexto global
    variables_globales.clear()
    variables_globales.update(variables_previas)
    tipos_de_variables.clear()
    tipos_de_variables.update(tipos_previos)
    # El retorno se realiza una vez restaurado el entorno anterior.
    
    return valor_retorno

def ejecutar_procedimiento(nombre, argumentos):
    """Ejecuta un procedimiento definido por el usuario"""
    if nombre not in tabla_procedimientos:
        print(f"Error: Procedimiento '{nombre}' no definido")
        return
    
    _, parametros, cuerpo = tabla_procedimientos[nombre]
    
    # Crear contexto local
    variables_locales = {}
    tipos_locales = {}
    
    # Asignar argumentos a parámetros
    if len(argumentos) != len(parametros):
        print(f"Error: Número incorrecto de argumentos para procedimiento '{nombre}'")
        return
    
    for i, (tipo_param, nombre_param) in enumerate(parametros):
        valor_argumento = evaluar(argumentos[i])
        variables_locales[nombre_param] = valor_argumento
        tipos_locales[nombre_param] = tipo_param
    
    # Guardar contexto global
    variables_previas = variables_globales.copy()
    tipos_previos = tipos_de_variables.copy()
    
    # Establecer contexto local
    variables_globales.clear()
    variables_globales.update(variables_locales)
    tipos_de_variables.clear()
    tipos_de_variables.update(tipos_locales)
    
    # Ejecutar cuerpo del procedimiento
    for sentencia in cuerpo:
        ejecutar(sentencia)
    
    # Restaurar contexto global
    variables_globales.clear()
    variables_globales.update(variables_previas)
    tipos_de_variables.clear()
    tipos_de_variables.update(tipos_previos)
    # No se devuelve valor alguno porque los procedimientos solo generan efectos.

# Variables globales
variables_globales = {}       # Almacén de variables y sus valores actuales
tipos_de_variables = {}       # Tipos declarados para cada identificador
tabla_funciones = {}          # Funciones definidas por el usuario
tabla_procedimientos = {}     # Procedimientos definidos por el usuario

if __name__ == "__main__":
    # Leer código desde archivo
    with open("test.bug", "r") as f:
        codigo = f.read()
    
    print(" Aplicando scanner...")
    lexer.input(codigo)
    
    # Mostrar tokens como en el ejemplo de PLY
    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)
    
    print("\n Analizando código...")
    ast = parser.parse(codigo, lexer=lexer)
    
    print(" Ejecutando programa...")
    ejecutar(ast)
