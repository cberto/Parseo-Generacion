# 📘 Especificación del Lenguaje — **BugBounty**

---

## 🔹 Lenguaje a crear

**BugBounty** es un lenguaje de programación especializado en seguridad, diseñado para detectar, explotar y reportar vulnerabilidades de forma ética y estructurada.  
Su principal particularidad es la **restricción de identificadores a solo vocales**, junto con un **sistema de tipos estático y fuerte**, y una sintaxis simple que permite modelar **funciones de seguridad, payloads, reportes de vulnerabilidades, bucles de testing, condicionales de detección, expresiones de riesgo y manejo de errores de seguridad**.

---

## 🎯 Objetivo

- Brindar un **lenguaje especializado en seguridad** para ejercitar construcción de analizadores (léxico, sintáctico y semántico).
- Permitir expresar programas de testing de seguridad con **tipado estático y control de flujo básico**.
- Incluir **payloads predefinidos** y **manejo de vulnerabilidades** para enriquecer los ejemplos de seguridad.

---

## 📌 Alcance

### Incluye

- Declaración y asignación de variables de seguridad con tipo.
- Funciones de testing con parámetros, payloads por defecto y **retorno obligatorio**.
- Control de flujo:
  - `si / sino / sino si`
  - `bucle (init; cond; inc/dec)`
  - `salir` / `seguir` en bucles.
- Operadores aritméticos, lógicos y de comparación
- **Payloads predefinidos** para vulnerabilidades comunes.
- Manejo de vulnerabilidades:
  - `intenta / captura / siempre`
  - `lanzar`

### Excluye

- Objetos, arreglos, módulos.
- Entrada/salida (solo `print`).
- Excepciones sofisticadas (solo manejo básico).
- Concurrencia.

---

## 🔤 Especificaciones léxicas

### Conjunto de caracteres

- Identificadores → solo vocales minúsculas `a e i o u`.
- Palabras clave → pueden contener consonantes (`funcion`, `bucle`, `probar`, `inyectar`, etc.).
- Insensible a mayúsculas.

---

## ⚙️ Especificaciones sintácticas (BNF)

```bnf
programa       ::= "$" contenido_opt "$$"

contenido_opt  ::= contenido contenido_opt
                 | /* vacío */

contenido      ::= declar_var
                 | asignacion
                 | sentencia_bucle
                 | sentencia_if
                 | sentencia_funcion
                 | invocacion
                 | print_stmt
                 | sentencia_excepcion
                 | lanzar_stmt

                 | salir_stmt
                 | seguir_stmt

tipo           ::= "cad" | "num" | "log" | "url" | "payload" | "vuln"

declar_var     ::= identificador ":" tipo "=" expr
                 | identificador ":" tipo "=" expr ";"

asignacion     ::= identificador "=" expr
                 | identificador "=" expr ";"

print_stmt     ::= "print" "(" expr ")"
                 | "print" "(" expr ")" ";"

sentencia_funcion ::= "funcion" identificador ":" tipo "(" parametros_opt ")" "{" contenido_opt "retorno" expr "}"
                    | "funcion" identificador ":" tipo "(" parametros_opt ")" "{" contenido_opt "retorno" expr ";" "}"

parametros_opt ::= parametro
                 | parametro "," parametro
                 | parametro "," parametro "," parametro
                 | /* vacío */

parametro      ::= identificador ":" tipo
                 | identificador ":" tipo "=" literal

invocacion     ::= identificador "(" argumentos_opt ")"

argumentos_opt ::= expr
                 | expr "," expr
                 | expr "," expr "," expr
                 | /* vacío */

sentencia_bucle ::= "bucle" "(" identificador "=" numero ";" condicion_bucle ";" direccion identificador ")" "{" contenido_opt "}"

condicion_bucle ::= identificador op_comp numero

direccion        ::= "inc" | "dec"

sentencia_if    ::= "si" "(" expr ")" "{" contenido_opt "}" sino_opt

sino_opt        ::= "sino" "{" contenido_opt "}"
                  | "sino" "si" "(" expr ")" "{" contenido_opt "}" sino_opt
                  | /* vacío */





sentencia_excepcion ::= "intenta" "{" contenido_opt "}" captura_lista_opt siempre_opt

captura_lista_opt ::= captura_claus
                     | captura_claus captura_claus
                     | captura_claus captura_claus captura_claus
                     | /* vacío */

captura_claus     ::= "captura" "(" identificador ")" "{" contenido_opt "}"
                     | "captura" "(" identificador ":" tipo ")" "{" contenido_opt "}"

siempre_opt       ::= "siempre" "{" contenido_opt "}"
                     | /* vacío */

lanzar_stmt    ::= "lanzar" expr
                 | "lanzar" expr ";"



salir_stmt     ::= "salir"
                 | "salir" ";"

seguir_stmt    ::= "seguir"
                 | "seguir" ";"

expr            ::= expr_bin
                 | expr_un
                 | primario

expr_bin        ::= expr_bin op_bin primario
                 | primario

expr_un         ::= "no" primario
                 | "no" "(" expr ")"

primario        ::= literal
                 | identificador
                 | invocacion
                 | "(" expr ")"

op_bin          ::= op_arit
                 | op_log_bin
                 | op_comp

op_arit         ::= "+" | "-" | "*" | "/"

op_log_bin      ::= "yy" | "oo"

op_comp         ::= "<" | ">" | "<=" | ">=" | "==" | "!="

literal         ::= numero
                 | logico
                 | cadena

numero          ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
                 | "0" numero
                 | "1" numero
                 | "2" numero
                 | "3" numero
                 | "4" numero
                 | "5" numero
                 | "6" numero
                 | "7" numero
                 | "8" numero
                 | "9" numero

logico          ::= "ver" | "fal"

cadena          ::= "\"" vocales "\""

vocales         ::= "a" | "e" | "i" | "o" | "u"
                 | "a" vocales
                 | "e" vocales
                 | "i" vocales
                 | "o" vocales
                 | "u" vocales

identificador   ::= "a" | "e" | "i" | "o" | "u"
                 | "a" identificador
                 | "e" identificador
                 | "i" identificador
                 | "o" identificador
                 | "u" identificador
```

### Especificaciones semánticas

```
Tipos

cad: cadenas de vocales.

num: enteros.

log: booleanos (ver/fal).

url: URLs válidas para testing de seguridad.

payload: cadenas de ataque predefinidas.

vuln: tipos de vulnerabilidades (sqli, xss, rce, etc.).

Tipado estático y fuerte: las variables mantienen tipo fijo.

Resolución de tipos

**Proyección numérica N(x):**
- num → valor del número
- log → 0 (fal) o 1 (ver)
- cad → longitud de la cadena

**Proyección booleana T(x):**
- num → verdadero si != 0, falso si == 0
- log → valor booleano directo
- cad → verdadero si != "", falso si == ""

Operadores

**Aritméticos (+ - * /) entre numeros **


**Comparación (< > <= >= == !=) → resultado log:**
 comparaciones entre expreciones


**Lógicos binarios (yy oo) → resultado log:**

**Lógico unario (no) → resultado log:**


Funciones

Retorno obligatorio, tipo exacto al declarado.

Parámetros por valor, con payloads por defecto permitidos.

Funciones de seguridad predefinidas (probar_sql, inyectar_xss, etc.).

Cada invocación crea un nuevo entorno.

Control de flujo

si/sino/sino si: condicionales encadenados para detección de vulnerabilidades.

bucle: ejecuta sobre números, con inc/dec para testing iterativo.

salir: termina el bucle actual cuando se detecta una vulnerabilidad.

seguir: pasa a la siguiente iteración del testing.

Manejo de errores

lanzar <expr>: detiene ejecución normal y transfiere control a manejadores de vulnerabilidades.

intenta/captura/siempre: bloques para manejar errores de seguridad.



print

Efecto: muestra en pantalla el valor o reporte de vulnerabilidad.

Retorno: num = cantidad de caracteres impresos.
```

## 📖 Ejemplos

### Testing de SQL Injection

```
funcion probar_sql:log(url:cad, payload:cad) {
  si (payload == "admin' OR 1=1--") {
    retorno ver
  }
  retorno fal
}
print(probar_sql("https://ejemplo.com", "admin' OR 1=1--"))   // ver
```

### Detección de vulnerabilidades

```
url: cad = "https://ejemplo.com/login"
payload: cad = "admin' OR 1=1--"

si (probar_sql(url, payload)) {
  print("Vulnerabilidad SQL detectada")
} sino si (inyectar_xss(url, "<script>alert(1)</script>")) {
  print("Vulnerabilidad XSS detectada")
} sino {
  print("No se encontraron vulnerabilidades")
}
```

### Manejo de vulnerabilidades

```
funcion testear_vuln:log(url:cad) {
  intenta {
    retorno probar_sql(url, "admin' OR 1=1--")
  }
  captura(e: num) {
    print("Error en testing: " + e)
    retorno fal
  }
  siempre {
    print("Testing completado")
  }
}
print(testear_vuln("https://ejemplo.com"))
```

### Operaciones con payloads

```
funcion generar_payload: cad(tipo: cad) {
  si (tipo == "sqli") {
    retorno "admin' OR 1=1--"
  } sino si (tipo == "xss") {
    retorno "<script>alert(1)</script>"
  } sino {
    retorno "payload_default"
  }
}

funcion es_vulnerable: log(response: cad) {
  retorno response == "error" oo response == "vulnerable"
}

url: cad = "https://ejemplo.com"
payload: cad = generar_payload("sqli")
print(es_vulnerable("error"))  // Imprime: ver
```

### Operaciones entre tipos diferentes

```

// Operaciones aritméticas entre tipos
resultado1: num = 5 + "aei" // 5 + 3 = 8 (num + longitud de cad)
resultado2: num = "ou" - ver // 2 - 1 = 1 (longitud de cad - ver)
resultado3: num = fal / "a" // 0 / 1 = 0 (fal / longitud de cad)

// Comparaciones entre tipos
comparacion1: log = 10 > "aei" // 10 > 3 = ver
comparacion2: log = "a" < 5 // 1 < 5 = ver
comparacion3: log = ver == "ou" // 1 == 2 = fal

// Operaciones lógicas entre tipos
logico1: log = 5 yy "aei" // ver yy ver = ver (ambos no vacíos)
logico2: log = fal oo "a" // fal oo ver = ver (al menos uno verdadero)
logico3: log = no "aei" // no ver = fal (cadena no vacía)

// Operaciones de seguridad
vulnerable: log = probar_sql("url", "payload") yy inyectar_xss("url", "script")
severidad: num = calcular_severidad("ALTA") + 1

```


```


PROPOSITO GENERAL: BUG BOUNTY
```