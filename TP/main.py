from scanner import lexer
from scanner.addons.parser import parser
import scanner.addons.builtins as builtins

def ejecutar(ast):
    if not ast: return
    tipo = ast[0]

    if tipo == "programa":
        for stmt in ast[1]:
            ejecutar(stmt)

    elif tipo == "asignar":
        _, var, expr = ast
        val = evaluar(expr)
        memoria[var] = val

    elif tipo == "declarar_asignar":
        _, tipo_var, var, expr = ast
        val = evaluar(expr)
        memoria[var] = val
        tipos[var] = tipo_var

    elif tipo == "declarar_lista_vacia":
        _, tipo_base, var = ast
        memoria[var] = []
        tipos[var] = ("lista", tipo_base)

    elif tipo == "mostrar":
        _, expr = ast
        val = evaluar(expr)
        print(val)

    elif tipo == "evaluar":
        _, condicion, bloque_si, bloque_no = ast
        if evaluar_condicion(condicion):
            for stmt in bloque_si:
                ejecutar(stmt)
        elif bloque_no:
            for stmt in bloque_no:
                ejecutar(stmt)

    elif tipo == "mientras":
        _, condicion, bloque = ast
        while evaluar_condicion(condicion):
            for stmt in bloque:
                ejecutar(stmt)

    elif tipo == "agregar":
        _, valor, lista = ast
        val = evaluar(valor)
        if lista in memoria and isinstance(memoria[lista], list):
            memoria[lista].append(val)
        else:
            print(f"Error: '{lista}' no es una lista")

    elif tipo == "quitar":
        _, lista, indice = ast
        idx = evaluar(indice)
        if lista in memoria and isinstance(memoria[lista], list):
            if 0 <= idx < len(memoria[lista]):
                memoria[lista].pop(idx)
            else:
                print(f"Error: Índice {idx} fuera de rango en lista '{lista}'")
        else:
            print(f"Error: '{lista}' no es una lista")

    elif tipo == "limpiar":
        _, lista = ast
        if lista in memoria and isinstance(memoria[lista], list):
            memoria[lista].clear()
        else:
            print(f"Error: '{lista}' no es una lista")

    elif tipo == "definir_funcion":
        _, tipo_ret, nombre, parametros, cuerpo, retorno = ast
        funciones[nombre] = ("funcion", tipo_ret, parametros, cuerpo, retorno)

    elif tipo == "definir_procedimiento":
        _, nombre, parametros, cuerpo = ast
        procedimientos[nombre] = ("procedimiento", parametros, cuerpo)

    elif tipo == "llamada_procedimiento":
        _, nombre, argumentos = ast
        if nombre in procedimientos:
            ejecutar_procedimiento(nombre, argumentos)
        else:
            print(f"Error: Procedimiento '{nombre}' no definido")

def evaluar(expr):
    et = expr[0]

    if et == "num": return expr[1]
    if et == "texto": return expr[1]
    if et == "var": return memoria.get(expr[1], None)
    if et == "bool": return expr[1]

    if et == "acceso_lista":
        _, lista, indice = expr
        idx = evaluar(indice)
        if lista in memoria and isinstance(memoria[lista], list):
            if 0 <= idx < len(memoria[lista]):
                return memoria[lista][idx]
            else:
                print(f"Error: Índice {idx} fuera de rango en lista '{lista}'")
                return None
        else:
            print(f"Error: '{lista}' no es una lista")
            return None

    if et == "binop":
        _, op, izq, der = expr
        l = evaluar(izq); r = evaluar(der)
        if op == "+": 
            # Concatenación de texto o suma numérica
            if isinstance(l, str) or isinstance(r, str):
                return str(l) + str(r)
            return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": 
            if r == 0:
                print("Error: División por cero")
                return 0
            return l / r

    if et == "probar":
        _, url, tipo, payload = expr
        return builtins.fn_probar(evaluar(url), evaluar(tipo), evaluar(payload))

    if et == "reportar":
        _, msg = expr
        return builtins.fn_reportar(evaluar(msg))

    if et == "llamada_funcion":
        _, nombre, argumentos = expr
        if nombre in funciones:
            return ejecutar_funcion(nombre, argumentos)
        else:
            print(f"Error: Función '{nombre}' no definida")
            return None

def evaluar_condicion(condicion):
    """Evalúa una condición lógica"""
    if not condicion:
        return False
    
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
        # Si es una expresión simple, evaluarla
        val = evaluar(condicion)
        if isinstance(val, str):
            return val == "vulnerable"
        return bool(val)

def ejecutar_funcion(nombre, argumentos):
    """Ejecuta una función definida por el usuario"""
    if nombre not in funciones:
        print(f"Error: Función '{nombre}' no definida")
        return None
    
    _, tipo_ret, parametros, cuerpo, retorno = funciones[nombre]
    
    # Crear contexto local
    memoria_local = {}
    tipos_local = {}
    
    # Asignar argumentos a parámetros
    if len(argumentos) != len(parametros):
        print(f"Error: Número incorrecto de argumentos para función '{nombre}'")
        return None
    
    for i, (tipo_param, nombre_param) in enumerate(parametros):
        valor = evaluar(argumentos[i])
        memoria_local[nombre_param] = valor
        tipos_local[nombre_param] = tipo_param
    
    # Guardar contexto global
    memoria_global = memoria.copy()
    tipos_global = tipos.copy()
    
    # Establecer contexto local
    memoria.clear()
    memoria.update(memoria_local)
    tipos.clear()
    tipos.update(tipos_local)
    
    # Ejecutar cuerpo de la función
    for stmt in cuerpo:
        ejecutar(stmt)
    
    # Evaluar expresión de retorno
    resultado = evaluar(retorno)
    
    # Restaurar contexto global
    memoria.clear()
    memoria.update(memoria_global)
    tipos.clear()
    tipos.update(tipos_global)
    
    return resultado

def ejecutar_procedimiento(nombre, argumentos):
    """Ejecuta un procedimiento definido por el usuario"""
    if nombre not in procedimientos:
        print(f"Error: Procedimiento '{nombre}' no definido")
        return
    
    _, parametros, cuerpo = procedimientos[nombre]
    
    # Crear contexto local
    memoria_local = {}
    tipos_local = {}
    
    # Asignar argumentos a parámetros
    if len(argumentos) != len(parametros):
        print(f"Error: Número incorrecto de argumentos para procedimiento '{nombre}'")
        return
    
    for i, (tipo_param, nombre_param) in enumerate(parametros):
        valor = evaluar(argumentos[i])
        memoria_local[nombre_param] = valor
        tipos_local[nombre_param] = tipo_param
    
    # Guardar contexto global
    memoria_global = memoria.copy()
    tipos_global = tipos.copy()
    
    # Establecer contexto local
    memoria.clear()
    memoria.update(memoria_local)
    tipos.clear()
    tipos.update(tipos_local)
    
    # Ejecutar cuerpo del procedimiento
    for stmt in cuerpo:
        ejecutar(stmt)
    
    # Restaurar contexto global
    memoria.clear()
    memoria.update(memoria_global)
    tipos.clear()
    tipos.update(tipos_global)

# Variables globales
memoria = {}  # Almacén de variables
tipos = {}    # Tipos de variables
funciones = {}  # Funciones definidas
procedimientos = {}  # Procedimientos definidos

if __name__ == "__main__":
    # Leer código desde archivo
    with open("test.bug", "r") as f:
        codigo = f.read()
    
    print("🔍 Aplicando scanner...")
    lexer.input(codigo)
    
    # Mostrar tokens como en el ejemplo de PLY
    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)
    
    print("\n🔍 Analizando código...")
    ast = parser.parse(codigo, lexer=lexer)
    
    print("🚀 Ejecutando programa...")
    ejecutar(ast)
