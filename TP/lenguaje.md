# Lenguaje de Seguridad Educativo

## Objetivo

Ser un lenguaje de programación en español que permita expresar y automatizar tareas básicas de seguridad (detectar vulnerabilidades simples, validar entradas) de forma clara y accesible, con reglas simples y cercanas al ámbito de seguridad informática

## Alcance

### Incluye:

- **Tipos:** `numero`, `texto`, `vulnerabilidad` (`sqli|xss|rce`), `bool` (`vulnerable|seguro`), `lista<tipo_base>`.
- **Sentencias:** asignación, impresión, condicional (`evaluar`), iteración (`mientras`), funciones, procedimientos, operaciones de lista (`agregar`, `quitar`, `limpiar`).

## Tipos de datos

- **numero** → valor numérico entero.

- **texto** → cadena de caracteres (strings).

- **vulnerabilidad** → sqli | xss | rce (tipos básicos de vulnerabilidades).

- **bool** → vulnerable | seguro.

- **lista<tipo_base>** → lista tipada cuyos elementos son **numero**, **texto**, **vulnerabilidad** o **bool**.

- **lista<tipo_base>** → elementos de `numero | texto | vulnerabilidad | bool`.
  - Se pueden crear vacías con `vacia` o con literal `[]`.
  - **Indexación:** el primer índice es **0**.

## Estructura de programa

Un programa comienza con **`INICIO`** y termina con **`FIN.`**. Todas las sentencias válidas van entre esas dos palabras clave.

### Sentencias principales

### Asignación

- Declaración + asignación:  
  `anotar <tipo> <id> = <valor>`
- Reasignación:  
  `anotar <id> = <nuevo_valor>`
- Listas:
  - Crear: `anotar lista<tipo> <id> = []` o `anotar lista<tipo> <id> = vacia`
  - Acceso: `<lista>[<indice>]`

### Impresión

`mostrar` acepta una expresión de texto que puede concatenar con `+` variables, números, booleanos, accesos a lista o llamadas a función.  
Ej.: `mostrar "Sitio: " + sitio + " | Vulnerabilidad: " + tipo`

### Condicional

`evaluar <condicion>` ejecuta un bloque `si pasa:` y, opcionalmente, un bloque `si no pasa:`.

Negación: `no <condicion>`

Ej:` evaluar <condicion> si pasa: <sentencias> si no pasa <sentencia>`

### Iteración (únicamente mientras)

`mientras <condicion> hacer <sentencias>`
repite mientras la condición sea verdadera.

## Operaciones de lista

- `agregar <valor> a <lista>` (Se agrega al final de lista)

- `quitar en <lista>[<indice>]` (Elimina por índice) - si no tiene índice válido da error

- `limpiar <lista>` (Deja la lista vacía)

## Funciones y procedimientos

- **Funciones:** devuelven un valor con **retornar**. Se aceptan parametros

```
funcion <tipo> <nombre>(parámetros)
    sentencias
    retornar <valor>
finFuncion
```

- **Procedimientos:** no devuelven valor; se invocan como sentencia. Se aceptan parametros

```
procedimiento <nombre>(parámetros)
    sentencias
finProcedimiento
```

> Variables
> y parámetros de funciones/procedimientos son **locales**.

## Comentarios

- De línea: `// comentario`

- De bloque: `/* comentario */`

## Operadores

- **Aritméticos:** +, -, /, \*
  Se admiten paréntesis para agrupar: ( … ).

- **Relacionales:** ==, !=, <, >, <=, >= (se permiten en ambos lados valores/expresiones).

- **Lógicos:** y, o, no.

## Especificaciones léxicas

- Sensible a mayúsculas/minúsculas (**case-sensitive**).

- Comentarios: `// …` y `/* … */`.
- Números enteros no negativos, textos entre comillas `"…"`.
- Operadores y signos: `+ - * / == != < > <= >= ( ) [ ] ,` y lógicos `y`, `o`, `no`.
- Palabras clave: `INICIO`, `FIN.`, `anotar`, `mostrar`, `evaluar`, `si pasa:`, `si no pasa:`, `mientras`, `hacer`, `funcion`, `retornar`, `finFuncion`, `procedimiento`, `finProcedimiento`, `agregar`, `quitar`, `limpiar`, `vacia`, `vulnerable`, `seguro`, `probar`, `reportar`.

## Especificaciones sintácticas

- Programa: `INICIO <sentencias> FIN.`
- Asignación:
  - Declaración: `anotar <tipo> <id> = <valor>`
  - Reasignación: `anotar <id> = <valor>`
  - Listas: `anotar lista<tipo_base> L = []` o `vacia`; acceso `L[i]`
- Impresión: `mostrar <expresion_texto>` (concatenación con `+`).
- Condicional:

```
evaluar <condicion>
    si pasa: <sentencias>
    si no pasa: <sentencias>   // opcional
```

- Iteración: `mientras <condicion> hacer <sentencias>`
- Expresiones: precedencia `* /` > `+ -`; paréntesis para agrupar.

- Funciones: Se debe definir que tipo de dato devolvera la funcion al momento de crearla.

## Especificaciones semánticas

- **Tipos:** verificación estática; declarar tipo al crear variable.
- **vulnerabilidad:** debe estar en `[sqli,xss,rce]`.
- **Listas:** tipo base estricto; error si se inserta tipo distinto.
- **mostrar:** convierte a `texto` al concatenar/mostrar.
- **Ámbitos:** variables/params de funciones/procedimientos son locales.
- **Errores runtime:** índice fuera de rango, división por cero, etc.

## Funciones predefinidas

- **probar**: Evalúa si una entrada es vulnerable. Retorna `vulnerable` si es vulnerable, `seguro` si no es vulnerable.
- **reportar**: Genera un reporte de vulnerabilidad encontrada con el mensaje especificado.

## Función predefinida: probar (modo simulado)

### `probar` (modo simulado)

`probar(texto url, vulnerabilidad tipo, texto payload) -> bool`

**Descripción**

- Función predefinida del lenguaje.
- Simula un test de seguridad (no realiza requests HTTP reales).
- Imprime en consola el detalle de la prueba ejecutada.
- Devuelve `vulnerable` o `seguro` según reglas sobre el **payload**.

## Reglas de decisión

**Para `sqli`** → vulnerable si el payload contiene (**case-insensitive**):

- `' OR`
- `1=1`
- `UNION`
- `--`  
  En otro caso → **seguro**.

**Para `xss`** → vulnerable si el payload contiene:

- `<script>`
- `onerror=`
- `onload=`
- `"><`  
  En otro caso → **seguro**.

#### Para `rce`

**Para `rce`** → vulnerable si el payload contiene:

- `;`
- `&&`
- `|`
- `` ` `` (backtick)
- `$( )`
- `ping -c`  
  En otro caso → **seguro**.

**Log educativo**

`[probar] URL=https://ejemplo.com/login | Tipo=sqli | Payload="admin' OR 1=1--"`

### `reportar`

`reportar(texto mensaje) -> nada`  
Emite un reporte (consola/archivo según implementación del runtime).

## Ejemplo de uso (simple)

```
INICIO

anotar bool r1 = probar("https://ejemplo.com/login", sqli, "admin' OR 1=1--")
anotar bool r2 = probar("https://ejemplo.com/comentarios", xss, "Hola mundo")
anotar bool r3 = probar("https://ejemplo.com/admin", rce, "ping -c 1 127.0.0.1")

mostrar "Login vulnerable? " + r1
mostrar "Comentarios vulnerables? " + r2
mostrar "Admin vulnerable? " + r3

FIN.
```

## Salida simulada

```
[probar] URL=https://ejemplo.com/login | Tipo=sqli | Payload="admin' OR 1=1--"
[probar] URL=https://ejemplo.com/comentarios | Tipo=xss | Payload="Hola mundo"
[probar] URL=https://ejemplo.com/admin | Tipo=rce | Payload="ping -c 1 127.0.0.1"

Login vulnerable? vulnerable
Comentarios vulnerables? seguro
Admin vulnerable? vulnerable
```

## Ejemplo: Scanner básico de vulnerabilidades

> Ajustado a **índice base 0** y a la firma de `probar(url, tipo, payload)`.

## Reglas semánticas

- vulnerabilidad debe estar en [sqli|xss|rce].

- Tipos de listas estrictos (solo tipo_base permitido).

- Variables de función/procedimiento son locales.

- Todo valor se convierte a texto al imprimir/concatenar en mostrar.

## Ejemplo de uso

Salida simulada

### Ejemplo: Scanner básico de vulnerabilidades

```

INICIO

// Listas: sitios y tipos de vulnerabilidades. Se inicializan vacías
anotar lista<texto> sitios = []
anotar lista<vulnerabilidad> tipos = []
anotar lista<bool> resultados = []

// Carga de sitios a testear
agregar "https://ejemplo.com/login" a sitios
agregar "https://ejemplo.com/comentarios" a sitios
agregar "https://ejemplo.com/admin" a sitios

// Carga de tipos de vulnerabilidades
agregar sqli a tipos
agregar xss a tipos
agregar rce a tipos

// Cantidad de tests a realizar
anotar numero cantidad_tests = 3

// Procedimiento: imprime un reporte de vulnerabilidad
procedimiento mostrarReporte(texto sitio, vulnerabilidad tipo, bool estado)
mostrar "Sitio: " + sitio + " | Tipo: " + tipo + " | Estado: " + estado
finProcedimiento

// Función: estado según tipo de vulnerabilidad (bool)
funcion bool testearVulnerabilidad(texto sitio, vulnerabilidad tipo)
evaluar tipo == sqli
si pasa:
retornar probar(sitio, sqli, "admin' OR 1=1--")
si no pasa:
evaluar tipo == xss
si pasa:
retornar probar(sitio, xss, "Hola mundo")
si no pasa:
evaluar tipo == rce
si pasa:
retornar probar(sitio, rce, "ping -c 1 127.0.0.1")
si no pasa:
retornar seguro
finFuncion

// Función: contar vulnerabilidades encontradas
funcion numero contarVulnerabilidades(lista<bool> resultados, numero n)
anotar numero i = 0
anotar numero contador = 0
mientras i < n hacer
evaluar resultados[i] == vulnerable
si pasa:
anotar contador = contador + 1
anotar i = i + 1
retornar contador
finFuncion

// Recorrido con 'mientras' para testear todos los sitios
mostrar "Iniciando escaneo de vulnerabilidades:"
anotar numero i = 0
mientras i < cantidad_tests hacer
anotar texto sitio_actual = sitios[i]
anotar vulnerabilidad tipo_actual = tipos[i]
anotar bool resultado = testearVulnerabilidad(sitio_actual, tipo_actual)
agregar resultado a resultados
mostrarReporte(sitio_actual, tipo_actual, resultado)
anotar i = i + 1

// Resumen del escaneo
anotar numero total_vulnerabilidades = contarVulnerabilidades(resultados, cantidad_tests)
mostrar "Total de vulnerabilidades encontradas: " + total_vulnerabilidades

// Operaciones de lista: quitar y limpiar
mostrar "Quitando último test..."
quitar en sitios[2]
quitar en tipos[2]
quitar en resultados[2]
anotar cantidad_tests = 2

mostrar "Limpiando listas..."
limpiar sitios
limpiar tipos
limpiar resultados
FIN.

```

### Salida

```
Iniciando escaneo de vulnerabilidades:
Sitio: https://ejemplo.com/login | Tipo: sqli | Estado: vulnerable
Sitio: https://ejemplo.com/comentarios | Tipo: xss | Estado: seguro
Sitio: https://ejemplo.com/admin | Tipo: rce | Estado: vulnerable
Total de vulnerabilidades encontradas: 2
Quitando último test...
Limpiando listas...
```

## BNF

```
<programa> ::= INICIO <sentencias> FIN.

<sentencias> ::= <sentencia> <sentencias> | λ

<sentencia> ::= <asignacion> | <impresion> | <condicional> | <iteracion>
| <definicion_funcion>
| <definicion_procedimiento>
| <llamada_procedimiento>
| <operacion_lista>

<asignacion> ::= anotar <tipo> <identificador> = <valor>
| anotar <identificador> = <valor>
| anotar lista<tipo_base> <identificador> = vacia

<tipo> ::= numero | texto | vulnerabilidad | bool | lista<tipo_base>

<tipo_base> ::= numero | texto | vulnerabilidad | bool

<impresion> ::= mostrar <expresion_texto>

<expresion_texto> ::= <valor_texto> | <valor_texto> + <expresion_texto>

<valor_texto> ::= <texto> | <identificador> | <booleano> | <numero>
| <acceso_lista> | <llamada_funcion>

<condicional> ::= evaluar <condicion> <bloque_condicional>

<bloque_condicional> ::= si pasa: <sentencias>
| si pasa: <sentencias> si no pasa: <sentencias>

<condicion> ::= no <condicion>
| <valor> <operador_relacional> <valor>
| <condicion> <operador_logico> <condicion>
| <booleano> | <identificador>

<iteracion> ::= mientras <condicion> hacer <sentencias>

<valor> ::= <valor> <op_suma> <termino> | <termino>
<termino> ::= <termino> <op_mul> <factor> | <factor>
<factor> ::= <numero> | <texto> | <identificador> | <booleano>
| <acceso_lista> | <llamada_funcion> | "(" <valor> ")"

<op_suma> ::= + | -
<op_mul> ::= \* | /

<acceso_lista> ::= <identificador> [ <valor> ]

<operacion_lista> ::= agregar <valor> a <identificador>
| quitar en <identificador> [ <valor> ]
| limpiar <identificador>

<definicion_funcion> ::= funcion <tipo> <identificador> ( <parametros_opt> )
<sentencias>
retornar <valor>
finFuncion

<definicion_procedimiento> ::= procedimiento <identificador> ( <parametros_opt> )
<sentencias>
finProcedimiento

<llamada_funcion> ::= <identificador> ( <argumentos_opt> )
<llamada_procedimiento> ::= <identificador> ( <argumentos_opt> )

<parametros_opt> ::= λ | <lista_parametros>
<lista_parametros> ::= <parametro> | <parametro> , <lista_parametros>
<parametro> ::= <tipo> <identificador>

<argumentos_opt> ::= λ | <lista_argumentos>
<lista_argumentos> ::= <valor> | <valor> , <lista_argumentos>

<booleano> ::= vulnerable | seguro

<vulnerabilidad> ::= sqli | xss | rce

<operador_relacional> ::= == | != | < | > | <= | >=
<operador_logico> ::= y | o

<numero> ::= <digito> { <digito> }
<texto> ::= '"' { <letra> | <digito> } '"'
<identificador> ::= <letra> { <letra> | <digito> | \_ }

<letra> ::= a | b | ... | z | A | B | ... | Z
<digito> ::= 0 | 1 | ... | 9

<comentario_linea> ::= "//" {cualquier_caracter_excepto_salto}
<comentario_bloque> ::= "/*" {cualquier_caracter} "*/"

<vacia> ::= vacia
