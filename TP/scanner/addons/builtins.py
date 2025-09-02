import re

VULNERABLE = "vulnerable"
SEGURO = "seguro"

# Patrones precompilados
P_SQLI = re.compile(r"(?:' OR|1=1|UNION|--)", re.IGNORECASE)
P_XSS  = re.compile(r"(?:<script>|onerror=|onload=|\"<)", re.IGNORECASE)
P_RCE  = re.compile(r"(?:;|&&|\||`|\$\(|ping -c)", re.IGNORECASE)

def fn_regex(texto: str, patron, flags="i") -> str:
    return VULNERABLE if patron.search(texto) else SEGURO

def fn_probar(url: str, tipo: str, payload: str) -> str:
    print(f"[probar] URL={url} | Tipo={tipo} | Payload={payload}")
    if tipo == 'sqli': return fn_regex(payload, P_SQLI)
    if tipo == 'xss':  return fn_regex(payload, P_XSS)
    if tipo == 'rce':  return fn_regex(payload, P_RCE)
    return SEGURO

def fn_reportar(mensaje: str):
    print(f"[REPORTE] {mensaje}")
