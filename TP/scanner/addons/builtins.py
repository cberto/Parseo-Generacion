"""
Funciones predefinidas del Lenguaje de Seguridad Educativo

Este módulo implementa las funciones built-in del lenguaje:
- probar(): Simula pruebas de vulnerabilidades
- reportar(): Genera reportes de seguridad

Las funciones están diseñadas para fines educativos y no realizan
ataques reales contra sistemas.
"""

import re

# =============================================================================
# CONSTANTES DEL LENGUAJE
# =============================================================================
VULNERABLE = "vulnerable"  # Valor booleano verdadero
SEGURO = "seguro"          # Valor booleano falso

# =============================================================================
# PATRONES DE DETECCIÓN DE VULNERABILIDADES
# =============================================================================
# Patrones precompilados para mejorar rendimiento
# Estos patrones detectan payloads típicos de cada tipo de vulnerabilidad

# SQL Injection: patrones comunes de inyección SQL
P_SQLI = re.compile(r"(?:' OR|1=1|UNION|--)", re.IGNORECASE)

# Cross-Site Scripting: patrones de scripts maliciosos
P_XSS = re.compile(r"(?:<script>|onerror=|onload=|\"<)", re.IGNORECASE)

# Remote Code Execution: patrones de ejecución de comandos
P_RCE = re.compile(r"(?:;|&&|\||`|\$\(|ping -c)", re.IGNORECASE)

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def fn_regex(texto: str, patron, flags="i") -> str:
    """
    Función auxiliar para aplicar patrones regex
    
    Args:
        texto: Cadena a analizar
        patron: Patrón regex compilado
        flags: Flags adicionales (no usado, el patrón ya está compilado)
    
    Returns:
        "vulnerable" si encuentra el patrón, "seguro" en caso contrario
    """
    return VULNERABLE if patron.search(texto) else SEGURO

# =============================================================================
# FUNCIONES PREDEFINIDAS DEL LENGUAJE
# =============================================================================

def fn_probar(url: str, tipo: str, payload: str) -> str:
    """
    Función predefinida 'probar' - Simula pruebas de vulnerabilidades
    
    Esta función simula un test de seguridad sin realizar requests HTTP reales.
    Imprime en consola el detalle de la prueba y devuelve el resultado.
    
    Args:
        url: URL del sitio a probar (solo para logging)
        tipo: Tipo de vulnerabilidad ('sqli', 'xss', 'rce')
        payload: Payload a analizar
    
    Returns:
        "vulnerable" si el payload contiene patrones de ataque
        "seguro" si no se detectan patrones maliciosos
    
    Ejemplo:
        probar("https://ejemplo.com", "sqli", "admin' OR 1=1--")
        # Salida: [probar] URL=https://ejemplo.com | Tipo=sqli | Payload=admin' OR 1=1--
        # Retorna: "vulnerable"
    """
    # Log de la prueba realizada
    print(f"[probar] URL={url} | Tipo={tipo} | Payload={payload}")
    
    # Aplicar el patrón correspondiente según el tipo de vulnerabilidad
    if tipo == 'sqli':
        return fn_regex(payload, P_SQLI)
    elif tipo == 'xss':
        return fn_regex(payload, P_XSS)
    elif tipo == 'rce':
        return fn_regex(payload, P_RCE)
    else:
        # Tipo de vulnerabilidad no reconocido
        return SEGURO

def fn_reportar(mensaje: str):
    """
    Función predefinida 'reportar' - Genera reportes de seguridad
    
    Emite un reporte con el mensaje especificado. En la implementación
    actual solo imprime en consola, pero podría extenderse para escribir
    a archivos o bases de datos.
    
    Args:
        mensaje: Mensaje del reporte a generar
    
    Ejemplo:
        reportar("Vulnerabilidad SQL detectada en login")
        # Salida: [REPORTE] Vulnerabilidad SQL detectada en login
    """
    print(f"[REPORTE] {mensaje}")
