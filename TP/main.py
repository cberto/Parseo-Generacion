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

    elif tipo == "mostrar":
        _, expr = ast
        val = evaluar(expr)
        print(val)

def evaluar(expr):
    et = expr[0]

    if et == "num": return expr[1]
    if et == "texto": return expr[1]
    if et == "var": return memoria.get(expr[1], None)

    if et == "binop":
        _, op, izq, der = expr
        l = evaluar(izq); r = evaluar(der)
        if op == "+": return l + r
        if op == "-": return l - r
        if op == "*": return l * r
        if op == "/": return l / r

    if et == "probar":
        _, url, tipo, payload = expr
        return builtins.fn_probar(evaluar(url), evaluar(tipo), evaluar(payload))

    if et == "reportar":
        _, msg = expr
        return builtins.fn_reportar(evaluar(msg))

memoria = {}

if __name__ == "__main__":
    codigo = """
    INICIO
    anotar sitio = "https://ejemplo.com/login"
    mostrar "=== Test de Vulnerabilidades ==="
    mostrar "Probando: " + sitio
    
    // Test SQL Injection
    mostrar "Test SQL Injection:"
    mostrar probar("https://ejemplo.com/login", sqli, "admin' OR 1=1--")
    
    // Test XSS
    mostrar "Test XSS:"
    mostrar probar("https://ejemplo.com/comentarios", xss, "<script>alert('XSS')</script>")
    
    // Test RCE
    mostrar "Test RCE:"
    mostrar probar("https://ejemplo.com/admin", rce, "ping -c 1 127.0.0.1")
    
    // Test seguro
    mostrar "Test seguro:"
    mostrar probar("https://ejemplo.com/login", sqli, "admin123")
    
    mostrar "=== Fin de Tests ==="
    FIN.
    """
    ast = parser.parse(codigo, lexer=lexer)
    ejecutar(ast)
