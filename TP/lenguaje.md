# Lenguaje de Seguridad Educativo

## Índice por TP

- [TP 3](#tp-3)

- [ASD — Derivación a izquierda Descendente](#asd--derivación-a-izquierda-descendente)
  - [ASA — Orden inverso de la derivación a la derecha (reducción ascendente)](#asa--orden-inverso-de-la-derivación-a-la-derecha-reducción-ascendente)
  - [ASA — Derivación a la derecha](#asa--derivación-a-la-derecha)

- [TP 4: ASD con retroceso cadena](#tp-4-asd-con-retroceso-cadena)

- [TP5: Parsing ASCP LL (1) cadena](#tp5-parsing--ascp-ll-1-cadena)

- [TP 6](#tp-6)

  - [Bloque invertido](#bloque-invertido)
  - [Parsing ASA con retroceso cadena](#parsing-asa-con-retroceso-cadena)

- [TP 7](#tp-7)

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

- **lista<tipo_base>** → lista tipada cuyos elementos son `numero`, `texto`, `vulnerabilidad` o `bool`.
  - Se pueden crear vacías con `vacia` o con literal `[]`.
  - **Indexación:** el primer índice es **0**.

## Estructura de programa

Un programa comienza con **`INICIO`** y termina con **`FIN.`**. Todas las sentencias válidas van entre esas dos palabras clave.

### Sentencias principales

### Asignación

- Declaración + asignación:  
  `anotar <tipo> <id> = <valor>`  
  Ej.: `anotar numero intentos = 3`
- Reasignación:  
  `anotar <id> = <nuevo_valor>`  
  Ej.: `anotar intentos = intentos + 1`
- Listas:
  - Crear: `anotar lista<tipo> <id> = []` o `anotar lista<tipo> <id> = vacia`  
    Ej.: `anotar lista<texto> urls = []`
  - Acceso: `<lista>[<indice>]`  
    Ej.: `mostrar urls[0]`

### Impresión

`mostrar` acepta una expresión de texto que puede concatenar con `+` variables, números, booleanos, accesos a lista o llamadas a función.  
Ej.: `mostrar "Sitio: " + sitio + " | Vulnerabilidad: " + tipo`

### Condicional

`evaluar <condicion>` ejecuta un bloque `si pasa:` y, opcionalmente, un bloque `si no pasa:`.

Negación: `no <condicion>`

Ej.:  
```
evaluar resultado == vulnerable
si pasa:
    mostrar "Sitio comprometido"
si no pasa:
    mostrar "Todo ok"
```

### Iteración (únicamente mientras)

`mientras <condicion> hacer <sentencias>` repite mientras la condición sea verdadera.  
Ej.:  
```
anotar numero i = 0
mientras i < 3 hacer
    mostrar "Prueba #" + i
    anotar i = i + 1
```

## Operaciones de lista

- `agregar <valor> a <lista>` (Se agrega al final de lista)  
  Ej.: `agregar "https://ejemplo.com" a urls`

- `quitar en <lista>[<indice>]` (Elimina por índice) — si no tiene índice válido da error  
  Ej.: `quitar en urls[1]`

- `limpiar <lista>` (Deja la lista vacía)  
  Ej.: `limpiar urls`

## Funciones y procedimientos

- **Funciones:** devuelven un valor con **retornar**. Se aceptan parametros

```
funcion <tipo> <nombre>(parámetros)
    sentencias
    retornar <valor>
finFuncion
```
Ej.:
```
funcion bool esCritica(vulnerabilidad tipo)
    evaluar tipo == rce
    si pasa:
        retornar vulnerable
    si no pasa:
        retornar seguro
finFuncion
```

- **Procedimientos:** no devuelven valor; se invocan como sentencia. Se aceptan parametros

```
procedimiento <nombre>(parámetros)
    sentencias
finProcedimiento
```
Ej.:
```
procedimiento mostrarReporte(texto sitio, bool estado)
    mostrar "Sitio: " + sitio + " | Estado: " + estado
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
  Ej.:  
  ```
  anotar numero contador = 0
  ```
- **vulnerabilidad:** debe estar en `[sqli,xss,rce]`.  
  Ej.:  
  ```
  anotar vulnerabilidad tipo = sqli
  ```
- **Listas:** tipo base estricto; error si se inserta tipo distinto.  
  Ej.:  
  ```
  anotar lista<texto> sitios = []
  agregar "https://ejemplo.com" a sitios
  ```
- **mostrar:** convierte a `texto` al concatenar/mostrar.  
  Ej.:  
  ```
  mostrar "Detectado: " + tipo
  ```
- **Ámbitos:** variables/params de funciones/procedimientos son locales.  
  Ej.:  
  ```
  funcion numero sumar(numero a, numero b)
      retornar a + b
  finFuncion
  ```
- **Errores runtime:** índice fuera de rango, división por cero, etc.  
  Ej.:  
  ```
  mostrar lista[10]  # Índice inválido
  ```

## Funciones predefinidas

- **probar**: Evalúa si una entrada es vulnerable. Retorna `vulnerable` si es vulnerable, `seguro` si no es vulnerable.
- **reportar**: Genera un reporte de vulnerabilidad encontrada con el mensaje especificado.

> 💡 **Heurística usada por `probar`**  
> La función analiza el `payload` con expresiones regulares sencillas:  
> - `sqli`: detecta cadenas como `' OR`, `1=1`, `UNION`, `--`. Indican intentos de alterar consultas SQL.  
> - `xss`: busca `<script>`, atributos `onerror=`/`onload=` o la secuencia `"><` para inyectar JavaScript.  
> - `rce`: marca operadores de shell (`;`, `&&`, `|`, `` ` ``), `$(...)` o comandos como `ping -c`.  
> Si aparece alguno de esos patrones, la función devuelve `vulnerable`; si no, `seguro`.  
> Los patrones están definidos en `scanner/addons/builtins.py`.

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
<valor_texto> ::= <texto> | <identificador> | <booleano> | <numero> | <acceso_lista> | <llamada_funcion>
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
<lista_parametros> ::= <parametro> <resto_parametros>
<resto_parametros> ::= , <lista_parametros> | λ
<parametro> ::= <tipo> <identificador>
<argumentos_opt> ::= λ | <lista_argumentos>
<lista_argumentos> ::= <valor> | <valor> , <lista_argumentos>
<booleano> ::= vulnerable | seguro
<vulnerabilidad> ::= sqli | xss | rce
<operador_relacional> ::= == | != | < | > | <= | >=
<operador_logico> ::= y | o
<numero> ::= <digito> <numero> | <digito>
<texto> ::= "<contenido_texto>"
<contenido_texto ::= <identificador>
<identificador> ::= <letra> | <letra> <identificador> <letra> ::= a | b | ... | z | A | B | ... | Z
<digito> ::= 0 | 1 | ... | 9<comentario_linea> ::= "//" {cualquier_caracter_excepto_salto}
<comentario_bloque> ::= "/*" {cualquier_caracter} "*/"
<vacia> ::= vacia

```

## Árbol de derivación

Ej:

```
INICIO

procedimiento p(texto a)
mostrar a
finProcedimiento


FIN.
```

## Árbol de Derivación - Grafico

```mermaid


flowchart TD
  A[Programa] --> A1[INICIO]
  A --> A2[Sentencias]
  A --> A3[FIN.]

  A2 --> B1[Sentencia]
  B1 --> C1[DefinicionProcedimiento]

  C1 --> C2[procedimiento]
  C1 --> C3[Identificador]
  C1 --> C4["("]
  C1 --> C5[ParametrosOpt]
  C1 --> C6[")"]
  C1 --> C7[Sentencias]
  C1 --> C8[finProcedimiento]

  C3 --> C3a["p"]
  C5 --> C5a[ListaParametros]
  C5a --> C5b[Parametro]
  C5b --> C5c[texto]
  C5b --> C5d[Identificador]
  C5d --> C5e["a"]

  C7 --> C9[Sentencia]
  C9 --> C10[Impresion]
  C10 --> C11[mostrar]
  C10 --> C12[ExpresionTexto]
  C12 --> C13[ValorTexto]
  C13 --> C14[Identificador]
  C14 --> C15["a"]
```

# TP 3

## ASD — Derivación a izquierda Descendente

| Cadena de derivación obtenida                                                          | Próxima producción a aplicar                                                                        |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Programa                                                                               | Programa → INICIO Sentencias FIN. .                                                                  |
| INICIO Sentencias FIN. .                                                                | Sentencias → Sentencia                                                                              |
| INICIO Sentencia FIN. .                                                                 | Sentencia → DefinicionProcedimiento                                                                 |
| INICIO DefinicionProcedimiento FIN. .                                                   | DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento |
| INICIO procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento FIN. . | Identificador → p                                                                                   |
| INICIO procedimiento p ( ParametrosOpt ) Sentencias finProcedimiento FIN. .             | ParametrosOpt → ListaParametros                                                                     |
| INICIO procedimiento p ( ListaParametros ) Sentencias finProcedimiento FIN. .           | ListaParametros → Parametro                                                                         |
| INICIO procedimiento p ( Parametro ) Sentencias finProcedimiento FIN. .                 | Parametro → Tipo Identificador                                                                      |
| INICIO procedimiento p ( texto Identificador ) Sentencias finProcedimiento FIN. .       | Identificador → a                                                                                   |
| INICIO procedimiento p ( texto a ) Sentencias finProcedimiento FIN. .                   | Sentencias → Sentencia                                                                              |
| INICIO procedimiento p ( texto a ) Sentencia finProcedimiento FIN. .                    | Sentencia → Impresion                                                                               |
| INICIO procedimiento p ( texto a ) Impresion finProcedimiento FIN. .                    | Impresion → mostrar ExpresionTexto                                                                  |
| INICIO procedimiento p ( texto a ) mostrar ExpresionTexto finProcedimiento FIN. .       | ExpresionTexto → ValorTexto                                                                         |
| INICIO procedimiento p ( texto a ) mostrar ValorTexto finProcedimiento FIN. .           | ValorTexto → Identificador                                                                          |
| INICIO procedimiento p ( texto a ) mostrar Identificador finProcedimiento FIN. .        | Identificador → a                                                                                   |
| INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. .                    | accept                                                                                              |

### ASA — Orden inverso de la derivación a la derecha (reducción ascendente)

| Cadena de derivación obtenida                                                    | Próxima producción a aplicar                                                                        |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. .              | Identificador → a                                                                                   |
| INICIO procedimiento p ( texto a ) mostrar Identificador finProcedimiento FIN. .  | ValorTexto → Identificador                                                                          |
| INICIO procedimiento p ( texto a ) mostrar ValorTexto finProcedimiento FIN. .     | ExpresionTexto → ValorTexto                                                                         |
| INICIO procedimiento p ( texto a ) mostrar ExpresionTexto finProcedimiento FIN. . | Impresion → mostrar ExpresionTexto                                                                  |
| INICIO procedimiento p ( texto a ) Impresion finProcedimiento FIN. .              | Sentencia → Impresion                                                                               |
| INICIO procedimiento p ( texto a ) Sentencia finProcedimiento FIN. .              | Sentencias → Sentencia                                                                              |
| INICIO procedimiento p ( texto Identificador ) Sentencias finProcedimiento FIN. . | Identificador → a                                                                                   |
| INICIO procedimiento p ( texto a ) Sentencias finProcedimiento FIN. .             | Parametro → Tipo Identificador                                                                      |
| INICIO procedimiento p ( Parametro ) Sentencias finProcedimiento FIN. .           | ListaParametros → Parametro                                                                         |
| INICIO procedimiento p ( ListaParametros ) Sentencias finProcedimiento FIN. .     | ParametrosOpt → ListaParametros                                                                     |
| INICIO procedimiento p ( ParametrosOpt ) Sentencias finProcedimiento FIN. .       | DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento |
| INICIO DefinicionProcedimiento FIN. .                                             | Sentencia → DefinicionProcedimiento                                                                 |
| INICIO Sentencia FIN. .                                                           | Sentencias → Sentencia                                                                              |
| INICIO Sentencias FIN. .                                                          | Programa → INICIO Sentencias FIN. .                                                                  |
| Programa                                                                         | accept                                                                                              |

> **Comentario:** En la derivación descendente se arranca desde el símbolo inicial (`Programa`) y se van expandiendo producciones siguiendo el orden de la entrada. Se ve cómo primero se reconoce la definición del procedimiento `p`, luego el bloque de sentencias y finalmente la impresión.

### ASA — Derivación a la derecha

| Cadena de trabajo (input → reducciones)                                                    | Producción aplicada                                                                                 |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| **INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. .**                    | —                                                                                                   |
| INICIO procedimiento p ( texto a ) **mostrar Identificador** finProcedimiento FIN. .        | Identificador → a                                                                                   |
| INICIO procedimiento p ( texto a ) **mostrar ValorTexto** finProcedimiento FIN. .           | ValorTexto → Identificador                                                                          |
| INICIO procedimiento p ( texto a ) **mostrar ExpresionTexto** finProcedimiento FIN. .       | ExpresionTexto → ValorTexto                                                                         |
| INICIO procedimiento p ( texto a ) **Impresion** finProcedimiento FIN. .                    | Impresion → mostrar ExpresionTexto                                                                  |
| INICIO procedimiento p ( texto a ) **Sentencia** finProcedimiento FIN. .                    | Sentencia → Impresion                                                                               |
| INICIO procedimiento p ( texto a ) **Sentencias** finProcedimiento FIN. .                   | Sentencias → Sentencia                                                                              |
| INICIO procedimiento p ( **Tipo** a ) Sentencias finProcedimiento FIN. .                    | Tipo → texto                                                                                        |
| INICIO procedimiento p ( Tipo **Identificador** ) Sentencias finProcedimiento FIN. .        | Identificador → a                                                                                   |
| INICIO procedimiento p ( **Parametro** ) Sentencias finProcedimiento FIN. .                 | Parametro → Tipo Identificador                                                                      |
| INICIO procedimiento p ( **ListaParametros** ) Sentencias finProcedimiento FIN. .           | ListaParametros → Parametro                                                                         |
| INICIO procedimiento p ( **ParametrosOpt** ) Sentencias finProcedimiento FIN. .             | ParametrosOpt → ListaParametros                                                                     |
| INICIO procedimiento **Identificador** ( ParametrosOpt ) Sentencias finProcedimiento FIN. . | Identificador → p                                                                                   |
| INICIO **DefinicionProcedimiento** FIN. .                                                   | DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento |
| INICIO **Sentencia** FIN. .                                                                 | Sentencia → DefinicionProcedimiento                                                                 |
| INICIO **Sentencias** FIN. .                                                                | Sentencias → Sentencia                                                                              |
| **Programa**                                                                               | Programa → INICIO Sentencias FIN. .                                                                  |
| **accept**                                                                                 | —                                                                                                   |

> **Comentario:** La tabla de derivación a la derecha muestra el proceso inverso: partimos de la cadena completa y vamos reduciendo subcadenas a no terminales. Se observa cómo cada coincidencia reemplaza fragmentos hasta colapsar todo en `Programa`.

# Análisis Sintáctico Descendente (ASD)

Programa de entrada:

```
INICIO

procedimiento p(texto a)
mostrar a
finProcedimiento

FIN.
```

---

## GIC (Pila) para el ejemplo

_GIC = ⟨ΣN, ΣT, S, P⟩_

- **ΣN** = { Programa, Sentencias, Sentencia, DefinicionProcedimiento, ParametrosOpt, ListaParametros, Parametro, Tipo, Identificador, Impresion, ExpresionTexto, ValorTexto }
- **ΣT** = { `INICIO`, `FIN.`, `procedimiento`, `finProcedimiento`, `(`, `)`, `texto`, `mostrar`, `p`, `a` }
- **S** = `Programa`
- **P** (solo las necesarias para esta entrada):

```
δ(q0, λ, λ)        => (q1, Z)
δ(q1, λ, λ)        => (q2, Programa)

; Expansiones por λ
δ(q2, λ, Programa)             => (q2, INICIO Sentencias FIN.)

; Bloque global: primera Sentencias se expande en una Sentencia (la definición)
δ(q2, λ, Sentencias)           => (q2, Sentencia Sentencias)
δ(q2, λ, Sentencia)            => (q2, DefinicionProcedimiento)

δ(q2, λ, DefinicionProcedimiento)
  => (q2, procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento)

; Nombre de la función/proc
δ(q2, λ, Identificador)        => (q2, p)

; Parámetros
δ(q2, λ, ParametrosOpt)        => (q2, ListaParametros)
δ(q2, λ, ListaParametros)      => (q2, Parametro)
δ(q2, λ, Parametro)            => (q2, Tipo Identificador)
δ(q2, λ, Tipo)                 => (q2, texto)
δ(q2, λ, Identificador)        => (q2, a)

; Cuerpo del procedimiento: una Impresión
δ(q2, λ, Sentencias)           => (q2, Sentencia Sentencias)
δ(q2, λ, Sentencia)            => (q2, Impresion)
δ(q2, λ, Impresion)            => (q2, mostrar ExpresionTexto)
δ(q2, λ, ExpresionTexto)       => (q2, ValorTexto)
δ(q2, λ, ValorTexto)           => (q2, Identificador)
δ(q2, λ, Identificador)        => (q2, a)

; Fin del cuerpo del procedimiento
δ(q2, λ, Sentencias)           => (q2, λ)

; Fin del bloque global (después de la definición no hay más sentencias)
δ(q2, λ, Sentencias)           => (q2, λ)

; Matcheos de terminales (consumen input)
δ(q2, INICIO, INICIO)                  => (q2, λ)
δ(q2, procedimiento, procedimiento)    => (q2, λ)
δ(q2, p, p)                            => (q2, λ)
δ(q2, (, ()                             => (q2, λ)
δ(q2, texto, texto)                    => (q2, λ)
δ(q2, a, a)                            => (q2, λ)
δ(q2, ), ))                             => (q2, λ)
δ(q2, mostrar, mostrar)                => (q2, λ)
δ(q2, a, a)                            => (q2, λ)
δ(q2, finProcedimiento, finProcedimiento) => (q2, λ)
δ(q2, FIN., FIN.)                        => (q2, λ)

; Aceptación
δ(q2, λ, Z) => (q3, λ)
```

## TP 4: ASD con retroceso cadena

| Pila                                                                                       | Cadena                                                            | Transición                                                                                                          |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| λ                                                                                          | INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. | δ(q0, λ, λ) ⇒ (q1, Z)                                                                                               |
| Z                                                                                          | INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. | δ(q1, λ, λ) ⇒ (q2, Programa)                                                                                        |
| Z Programa                                                                                 | INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. | δ(q2, λ, Programa) ⇒ (q2, INICIO Sentencias FIN.)                                                                    |
| Z FIN. Sentencias INICIO                                                                    | INICIO procedimiento p ( texto a ) mostrar a finProcedimiento FIN. | δ(q2, INICIO, INICIO) ⇒ (q2, λ)                                                                                     |
| Z FIN. Sentencias                                                                           | procedimiento p ( texto a ) mostrar a finProcedimiento FIN.        | δ(q2, λ, Sentencias) ⇒ (q2, Sentencia Sentencias)                                                                   |
| Z FIN. Sentencias Sentencia                                                                 | procedimiento p ( texto a ) mostrar a finProcedimiento FIN.        | δ(q2, λ, Sentencia) ⇒ (q2, DefinicionProcedimiento)                                                                 |
| Z FIN. Sentencias DefinicionProcedimiento                                                   | procedimiento p ( texto a ) mostrar a finProcedimiento FIN.        | δ(q2, λ, DefinicionProcedimiento) ⇒ (q2, procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento) |
| Z FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt ( Identificador procedimiento | procedimiento p ( texto a ) mostrar a finProcedimiento FIN.        | δ(q2, procedimiento, procedimiento) ⇒ (q2, λ)                                                                       |
| Z FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt ( Identificador               | p ( texto a ) mostrar a finProcedimiento FIN.                      | δ(q2, λ, Identificador) ⇒ (q2, p)                                                                                   |
| Z FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt ( p                           | p ( texto a ) mostrar a finProcedimiento FIN.                      | δ(q2, p, p) ⇒ (q2, λ)                                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt (                             | ( texto a ) mostrar a finProcedimiento FIN.                        | δ(q2, (, () ⇒ (q2, λ)                                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt                               | texto a ) mostrar a finProcedimiento FIN.                          | δ(q2, λ, ParametrosOpt) ⇒ (q2, ListaParametros)                                                                     |
| Z FIN. Sentencias finProcedimiento Sentencias ) ListaParametros                             | texto a ) mostrar a finProcedimiento FIN.                          | δ(q2, λ, ListaParametros) ⇒ (q2, Parametro)                                                                         |
| Z FIN. Sentencias finProcedimiento Sentencias ) Parametro                                   | texto a ) mostrar a finProcedimiento FIN.                          | δ(q2, λ, Parametro) ⇒ (q2, Tipo Identificador)                                                                      |
| Z FIN. Sentencias finProcedimiento Sentencias ) Identificador Tipo                          | texto a ) mostrar a finProcedimiento FIN.                          | δ(q2, λ, Tipo) ⇒ (q2, texto)                                                                                        |
| Z FIN. Sentencias finProcedimiento Sentencias ) Identificador texto                         | texto a ) mostrar a finProcedimiento FIN.                          | δ(q2, texto, texto) ⇒ (q2, λ)                                                                                       |
| Z FIN. Sentencias finProcedimiento Sentencias ) Identificador                               | a ) mostrar a finProcedimiento FIN.                                | δ(q2, λ, Identificador) ⇒ (q2, a)                                                                                   |
| Z FIN. Sentencias finProcedimiento Sentencias ) a                                           | a ) mostrar a finProcedimiento FIN.                                | δ(q2, a, a) ⇒ (q2, λ)                                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias )                                             | ) mostrar a finProcedimiento FIN.                                  | δ(q2, ), )) ⇒ (q2, λ)                                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias                                               | mostrar a finProcedimiento FIN.                                    | δ(q2, λ, Sentencias) ⇒ (q2, Sentencia Sentencias)                                                                   |
| Z FIN. Sentencias finProcedimiento Sentencias Sentencia                                     | mostrar a finProcedimiento FIN.                                    | δ(q2, λ, Sentencia) ⇒ (q2, Impresion)                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias Impresion                                     | mostrar a finProcedimiento FIN.                                    | δ(q2, λ, Impresion) ⇒ (q2, mostrar ExpresionTexto)                                                                  |
| Z FIN. Sentencias finProcedimiento Sentencias ExpresionTexto mostrar                        | mostrar a finProcedimiento FIN.                                    | δ(q2, mostrar, mostrar) ⇒ (q2, λ)                                                                                   |
| Z FIN. Sentencias finProcedimiento Sentencias ExpresionTexto                                | a finProcedimiento FIN.                                            | δ(q2, λ, ExpresionTexto) ⇒ (q2, ValorTexto)                                                                         |
| Z FIN. Sentencias finProcedimiento Sentencias ValorTexto                                    | a finProcedimiento FIN.                                            | δ(q2, λ, ValorTexto) ⇒ (q2, Identificador)                                                                          |
| Z FIN. Sentencias finProcedimiento Sentencias Identificador                                 | a finProcedimiento FIN.                                            | δ(q2, λ, Identificador) ⇒ (q2, a)                                                                                   |
| Z FIN. Sentencias finProcedimiento Sentencias a                                             | a finProcedimiento FIN.                                            | δ(q2, a, a) ⇒ (q2, λ)                                                                                               |
| Z FIN. Sentencias finProcedimiento Sentencias                                               | finProcedimiento FIN.                                              | δ(q2, λ, Sentencias) ⇒ (q2, λ)                                                                                      |
| Z FIN. Sentencias finProcedimiento                                                          | finProcedimiento FIN.                                              | δ(q2, finProcedimiento, finProcedimiento) ⇒ (q2, λ)                                                                 |
| Z FIN. Sentencias                                                                           | FIN.                                                               | δ(q2, λ, Sentencias) ⇒ (q2, λ)                                                                                      |
| Z FIN.                                                                                      | FIN.                                                               | δ(q2, FIN., FIN.) ⇒ (q2, λ)                                                                                           |
| Z                                                                                          | λ                                                                 | δ(q2, λ, Z) ⇒ (q3, λ)                                                                                               |
| λ                                                                                          | λ                                                                 | **accept**                                                                                                          |

> **Comentario:** Aquí se ve el análisis descendente con retroceso. La pila muestra los símbolos pendientes, la cadena restante indica qué falta consumir y la transición detalla la función de movimiento. Cada vez que no hay coincidencia inmediata, el autómata expande producciones (por eso aparecen muchas operaciones con λ) hasta que logra consumir la cadena completa y aceptar.

# TP5: Parsing ASCP LL (1) cadena

## Cadena de prueba

```txt
INICIO
procedimiento p(texto a)
    mostrar a
finProcedimiento
FIN.
```

---

## GIC reducido (para el análisis LL(1))

```bnf
Programa → INICIO Sentencias FIN.
Sentencias → Sentencia Sentencias | λ
Sentencia → DefinicionProcedimiento | Impresion
DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento
ParametrosOpt → ListaParametros | λ
ListaParametros → Parametro | Parametro , ListaParametros
Parametro → Tipo Identificador
Tipo → texto | numero | vulnerabilidad | bool
Impresion → mostrar ExpresionTexto
ExpresionTexto → ValorTexto
ValorTexto → Identificador | texto | numero | booleano
Identificador → a | p
```

> **Comentario:** Se toma una versión simplificada de la gramática para construir la tabla LL(1). Solo incluye los símbolos necesarios para analizar la cadena de prueba y evita ambigüedades.

---

## PRIM

| Producción                    | Conjunto                                 |
| ----------------------------- | ---------------------------------------- |
| PRIM(Programa)                | {INICIO}                                 |
| PRIM(Sentencias)              | {procedimiento, mostrar, λ}              |
| PRIM(Sentencia)               | {procedimiento, mostrar}                 |
| PRIM(DefinicionProcedimiento) | {procedimiento}                          |
| PRIM(RestoParametros)         | {,, λ}                                   |
| PRIM(ParametrosOpt)           | {texto, numero, vulnerabilidad, bool, λ} |
| PRIM(ListaParametros)         | {texto, numero, vulnerabilidad, bool}    |
| PRIM(Parametro)               | {texto, numero, vulnerabilidad, bool}    |
| PRIM(Tipo)                    | {texto, numero, vulnerabilidad, bool}    |
| PRIM(Impresion)               | {mostrar}                                |
| PRIM(ExpresionTexto)          | {a, p, texto, numero, booleano}          |
| PRIM(ValorTexto)              | {a, p, texto, numero, booleano}          |
| PRIM(Identificador)           | {a, p}                                   |

> **Comentario:** `PRIM` indica con qué terminales puede comenzar cada no terminal. Se usa para llenar la tabla predictiva.

---

## SIG

| Producción                   | Conjunto                                                |
| ---------------------------- | ------------------------------------------------------- |
| SIG(Programa)                | {$}                                                     |
| SIG(Sentencias)              | {FIN., finProcedimiento}                                 |
| SIG(Sentencia)               | {procedimiento, mostrar, FIN., finProcedimiento}         |
| SIG(DefinicionProcedimiento) | {procedimiento, mostrar, FIN., finProcedimiento}         |
| SIG(ParametrosOpt)           | {)}                                                     |
| SIG(RestoParametros)         | {)}                                                     |
| SIG(ListaParametros)         | {)}                                                     |
| SIG(Parametro)               | {,, )}                                                  |
| SIG(Tipo)                    | {a, p}                                                  |
| SIG(Impresion)               | {procedimiento, mostrar, FIN., finProcedimiento}         |
| SIG(ExpresionTexto)          | {procedimiento, mostrar, FIN., finProcedimiento}         |
| SIG(ValorTexto)              | {procedimiento, mostrar, FIN., finProcedimiento}         |
| SIG(Identificador)           | {(, , ), procedimiento, mostrar, FIN., finProcedimiento} |

> **Comentario:** `SIG` lista los terminales que pueden seguir a cada no terminal. Es clave para manejar las producciones con λ.

## PRED

| Producción                                                                                                | Conjunto                              |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| PRED(Programa → INICIO Sentencias FIN.)                                                                    | {INICIO}                              |
| PRED(Sentencias → Sentencia Sentencias)                                                                   | {procedimiento, mostrar}              |
| PRED(Sentencias → λ)                                                                                      | {FIN., finProcedimiento}               |
| PRED(Sentencia → DefinicionProcedimiento)                                                                 | {procedimiento}                       |
| PRED(Sentencia → Impresion)                                                                               | {mostrar}                             |
| PRED(DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento) | {procedimiento}                       |
| PRED(ParametrosOpt → ListaParametros)                                                                     | {texto, numero, vulnerabilidad, bool} |
| PRED(ParametrosOpt → λ)                                                                                   | {)}                                   |
| PRED(ListaParametros → Parametro RestoParametro)                                                          | {texto, numero, vulnerabilidad, bool} |
| PRED(RestoParametros → , ListaParametros)                                                                 | {,}                                   |
| PRED(RestoParametros → λ)                                                                                 | {)}                                   |
| PRED(Parametro → Tipo Identificador)                                                                      | {texto, numero, vulnerabilidad, bool} |
| PRED(Impresion → mostrar ExpresionTexto)                                                                  | {mostrar}                             |
| PRED(ExpresionTexto → ValorTexto)                                                                         | {a, p, texto, numero, booleano}       |
| PRED(ValorTexto → Identificador)                                                                          | {a, p}                                |
| PRED(ValorTexto → texto)                                                                                  | {texto}                               |
| PRED(ValorTexto → numero)                                                                                 | {numero}                              |
| PRED(ValorTexto → booleano)                                                                               | {booleano}                            |

> **Comentario:** `PRED` combina `PRIM` y `SIG` para saber cuándo usar cada producción durante el parsing LL(1).

---

## Tabla LL(1)

|                             |              INICIO              |                                            procedimiento                                            |              mostrar               |                    texto                    |                   numero                    |               vulnerabilidad                |                    bool                     |              a              |              p              |          booleano           |                  ,                  |   (   |            )            |        FIN.         | finProcedimiento |   $   |
| --------------------------- | :------------------------------: | :-------------------------------------------------------------------------------------------------: | :--------------------------------: | :-----------------------------------------: | :-----------------------------------------: | :-----------------------------------------: | :-----------------------------------------: | :-------------------------: | :-------------------------: | :-------------------------: | :---------------------------------: | :---: | :---------------------: | :----------------: | :--------------: | :---: |
| **Programa**                | Programa → INICIO Sentencias FIN. |                                                error                                                |               error                |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       | error |
| **Sentencias**              |              error               |                                  Sentencias → Sentencia Sentencias                                  | Sentencias → Sentencia Sentencias  |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            |                error                | error |   **Sentencias → λ**    | **Sentencias → λ** |      error       |
| **Sentencia**               |              error               |                                 Sentencia → DefinicionProcedimiento                                 |       Sentencia → Impresion        |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       |
| **DefinicionProcedimiento** |              error               | DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento |               error                |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       |
| **ParametrosOpt**           |              error               |                                                error                                                |               error                |       ParametrosOpt → ListaParametros       |       ParametrosOpt → ListaParametros       |       ParametrosOpt → ListaParametros       |       ParametrosOpt → ListaParametros       |            error            |            error            |            error            |                error                | error |  **ParametrosOpt → λ**  |       error        |      error       | error |
| **ListaParametros**         |              error               |                                                error                                                |               error                | ListaParametros → Parametro RestoParametros | ListaParametros → Parametro RestoParametros | ListaParametros → Parametro RestoParametros | ListaParametros → Parametro RestoParametros |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       | error |
| **RestoParametros**         |              error               |                                                error                                                |               error                |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            | RestoParametros → , ListaParametros | error | **RestoParametros → λ** |       error        |      error       | error |
| **Parametro**               |              error               |                                                error                                                |               error                |       Parametro → Tipo Identificador        |       Parametro → Tipo Identificador        |       Parametro → Tipo Identificador        |       Parametro → Tipo Identificador        |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       | error |
| **Tipo**                    |              error               |                                                error                                                |               error                |                Tipo → texto                 |                Tipo → numero                |            Tipo → vulnerabilidad            |                 Tipo → bool                 |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       | error |
| **Impresion**               |              error               |                                                error                                                | Impresion → mostrar ExpresionTexto |                    error                    |                    error                    |                    error                    |                    error                    |            error            |            error            |            error            |                error                | error |          error          |       error        |      error       | error |
| **ExpresionTexto**          |              error               |                                                error                                                |               error                |         ExpresionTexto → ValorTexto         |         ExpresionTexto → ValorTexto         |                    error                    |                    error                    | ExpresionTexto → ValorTexto | ExpresionTexto → ValorTexto | ExpresionTexto → ValorTexto |                error                | error |          error          |       error        |      error       | error |
| **ValorTexto**              |              error               |                                                error                                                |               error                |             ValorTexto → texto              |             ValorTexto → numero             |                    error                    |                    error                    | ValorTexto → Identificador  | ValorTexto → Identificador  |    ValorTexto → booleano    |                error                | error |          error          |       error        |      error       | error |
| **Identificador**           |              error               |                                                error                                                |               error                |                    error                    |                    error                    |                    error                    |                    error                    |      Identificador → a      |      Identificador → p      |            error            |                error                | error |          error          |       error        |      error       | error |

> **Comentario:** Esta tabla indica qué producción elegir según el símbolo no terminal en la pila y el token actual. La ausencia de conflictos confirma que la gramática (reducida) es LL(1).

## Trazado del parsing LL(1)

| Pila                                                                                       | Cadena                                                                       | Regla o Acción                                                                                      |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| $ Programa                                                                                 | INICIO procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $ | Programa → INICIO Sentencias FIN.                                                                    |
| $ FIN. Sentencias INICIO                                                                    | INICIO procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $ | emparejar(INICIO)                                                                                   |
| $ FIN. Sentencias                                                                           | procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $        | Sentencias → Sentencia Sentencias                                                                   |
| $ FIN. Sentencias Sentencia                                                                 | procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $        | Sentencia → DefinicionProcedimiento                                                                 |
| $ FIN. Sentencias DefinicionProcedimiento                                                   | procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $        | DefinicionProcedimiento → procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento |
| $ FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt ( Identificador procedimiento | procedimiento p ( texto a , bool p ) mostrar a finProcedimiento FIN. $        | emparejar(procedimiento)                                                                            |
| $ FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt ( Identificador               | p ( texto a , bool p ) mostrar a finProcedimiento FIN. $                      | Identificador → p                                                                                   |
| $ FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt (                             | ( texto a , bool p ) mostrar a finProcedimiento FIN. $                        | emparejar(p)                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt                               | texto a , bool p ) mostrar a finProcedimiento FIN. $                          | emparejar(()                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) ParametrosOpt                               | texto a , bool p ) mostrar a finProcedimiento FIN. $                          | ParametrosOpt → ListaParametros                                                                     |
| $ FIN. Sentencias finProcedimiento Sentencias ) ListaParametros                             | texto a , bool p ) mostrar a finProcedimiento FIN. $                          | ListaParametros → Parametro RestoParametros                                                         |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Parametro                   | texto a , bool p ) mostrar a finProcedimiento FIN. $                          | Parametro → Tipo Identificador                                                                      |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Identificador Tipo          | texto a , bool p ) mostrar a finProcedimiento FIN. $                          | Tipo → texto                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Identificador               | a , bool p ) mostrar a finProcedimiento FIN. $                                | emparejar(texto)                                                                                    |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | a , bool p ) mostrar a finProcedimiento FIN. $                                | Identificador → a                                                                                   |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | , bool p ) mostrar a finProcedimiento FIN. $                                  | emparejar(a)                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | , bool p ) mostrar a finProcedimiento FIN. $                                  | RestoParametros → , ListaParametros                                                                 |
| $ FIN. Sentencias finProcedimiento Sentencias ) ListaParametros ,                           | , bool p ) mostrar a finProcedimiento FIN. $                                  | emparejar(,)                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) ListaParametros                             | bool p ) mostrar a finProcedimiento FIN. $                                    | ListaParametros → Parametro RestoParametros                                                         |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Parametro                   | bool p ) mostrar a finProcedimiento FIN. $                                    | Parametro → Tipo Identificador                                                                      |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Identificador Tipo          | bool p ) mostrar a finProcedimiento FIN. $                                    | Tipo → bool                                                                                         |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros Identificador               | p ) mostrar a finProcedimiento FIN. $                                         | emparejar(bool)                                                                                     |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | p ) mostrar a finProcedimiento FIN. $                                         | Identificador → p                                                                                   |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | ) mostrar a finProcedimiento FIN. $                                           | emparejar(p)                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias ) RestoParametros                             | ) mostrar a finProcedimiento FIN. $                                           | RestoParametros → λ                                                                                 |
| $ FIN. Sentencias finProcedimiento Sentencias )                                             | ) mostrar a finProcedimiento FIN. $                                           | emparejar())                                                                                        |
| $ FIN. Sentencias finProcedimiento Sentencias                                               | mostrar a finProcedimiento FIN. $                                             | Sentencias → Sentencia Sentencias                                                                   |
| $ FIN. Sentencias finProcedimiento Sentencias Sentencia                                     | mostrar a finProcedimiento FIN. $                                             | Sentencia → Impresion                                                                               |
| $ FIN. Sentencias finProcedimiento Sentencias Impresion                                     | mostrar a finProcedimiento FIN. $                                             | Impresion → mostrar ExpresionTexto                                                                  |
| $ FIN. Sentencias finProcedimiento Sentencias ExpresionTexto mostrar                        | mostrar a finProcedimiento FIN. $                                             | emparejar(mostrar)                                                                                  |
| $ FIN. Sentencias finProcedimiento Sentencias ExpresionTexto                                | a finProcedimiento FIN. $                                                     | ExpresionTexto → ValorTexto                                                                         |
| $ FIN. Sentencias finProcedimiento Sentencias ValorTexto                                    | a finProcedimiento FIN. $                                                     | ValorTexto → Identificador                                                                          |
| $ FIN. Sentencias finProcedimiento Sentencias Identificador                                 | a finProcedimiento FIN. $                                                     | Identificador → a                                                                                   |
| $ FIN. Sentencias finProcedimiento Sentencias                                               | finProcedimiento FIN. $                                                       | emparejar(a)                                                                                        |
| $ FIN. Sentencias finProcedimiento                                                          | finProcedimiento FIN. $                                                       | Sentencias → λ                                                                                      |
| $ FIN. Sentencias                                                                           | FIN. $                                                                        | emparejar(finProcedimiento)                                                                         |
| $ FIN.                                                                                      | FIN. $                                                                        | Sentencias → λ                                                                                      |
| $                                                                                          | $                                                                            | emparejar(FIN.)                                                                                      |
|                                                                                            |                                                                              | **Aceptar**                                                                                         |

> **Comentario:** El trazado muestra una corrida del algoritmo LL(1). La pila y la cadena se van reduciendo conforme se aplican reglas o se emparejan terminales con la entrada.

---

## Conclusión

El **lenguaje de seguridad educativo** cumple las condiciones **LL(1)** en su núcleo estructural (programas, procedimientos, impresión, parámetros).  
No se presentan conflictos en la tabla predictiva, lo que demuestra que es posible construir un analizador descendente recursivo determinista para este subconjunto.

# TP 6:

### Bloque invertido

```

δ(q0, λ, Z) => (q1, λ)
δ(q1, λ, Programa) => (q2, λ)

; Expansiones por λ (invertidas)
δ(q2, INICIO Sentencias FIN., Programa) => (q2, λ)

; Bloque global: primera Sentencias se expande en una Sentencia (la definición)
δ(q2, Sentencia Sentencias, Sentencias) => (q2, λ)
δ(q2, DefinicionProcedimiento, Sentencia) => (q2, λ)

δ(q2, procedimiento Identificador ( ParametrosOpt ) Sentencias finProcedimiento, DefinicionProcedimiento) => (q2, λ)

; Nombre de la función/proc
δ(q2, p, Identificador) => (q2, λ)

; Parámetros
δ(q2, ListaParametros, ParametrosOpt) => (q2, λ)
δ(q2, Parametro, ListaParametros) => (q2, λ)
δ(q2, Tipo Identificador, Parametro) => (q2, λ)
δ(q2, texto, Tipo) => (q2, λ)
δ(q2, a, Identificador) => (q2, λ)

; Cuerpo del procedimiento: una Impresión
δ(q2, Sentencia Sentencias, Sentencias) => (q2, λ)
δ(q2, Impresion, Sentencia) => (q2, λ)
δ(q2, mostrar ExpresionTexto, Impresion) => (q2, λ)
δ(q2, ValorTexto, ExpresionTexto) => (q2, λ)
δ(q2, Identificador, ValorTexto) => (q2, λ)
δ(q2, a, Identificador) => (q2, λ)

; Fin del cuerpo del procedimiento
δ(q2, λ, Sentencias) => (q2, λ)

; Fin del bloque global (después de la definición no hay más sentencias)
δ(q2, λ, Sentencias) => (q2, λ)

; Matcheos de terminales (consumen input)
δ(q2, INICIO, INICIO) => (q2, λ)
δ(q2, procedimiento, procedimiento) => (q2, λ)
δ(q2, p, p) => (q2, λ)
δ(q2, (, () => (q2, λ)
δ(q2, texto, texto) => (q2, λ)
δ(q2, a, a) => (q2, λ)
δ(q2, ), )) => (q2, λ)
δ(q2, mostrar, mostrar) => (q2, λ)
δ(q2, a, a) => (q2, λ)
δ(q2, finProcedimiento, finProcedimiento) => (q2, λ)
δ(q2, FIN., FIN.) => (q2, λ)

; Aceptación
δ(q2, λ, Z) => (q3, λ)
```

> **Comentario:** El bloque invertido lista las expansiones que haría un parser ascendente invirtiendo el orden. Sirve para verificar consistencia con las derivaciones anteriores.

### Parsing ASA con retroceso cadena

| Pila                                                                                      | Cadena                                                         | Transición                   |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ---------------------------- |
| λ                                                                                         | INICIO procedimiento p(texto a) mostrar a finProcedimiento FIN. | δ(q0, λ, λ) ⇒ (q1, Z)        |
| Z                                                                                         | INICIO procedimiento p(texto a) mostrar a finProcedimiento FIN. | shift                        |
| Z INICIO                                                                                  | procedimiento p(texto a) mostrar a finProcedimiento FIN.        | shift                        |
| Z INICIO procedimiento                                                                    | p(texto a) mostrar a finProcedimiento FIN.                      | shift                        |
| Z INICIO procedimiento p                                                                  | (texto a) mostrar a finProcedimiento FIN.                       | reduce                       |
| Z INICIO procedimiento Identificador                                                      | (texto a) mostrar a finProcedimiento FIN.                       | shift                        |
| Z INICIO procedimiento Identificador (                                                    | texto a) mostrar a finProcedimiento FIN.                        | shift                        |
| Z INICIO procedimiento Identificador (texto                                               | a) mostrar a finProcedimiento FIN.                              | reduce                       |
| Z INICIO procedimiento Identificador (Tipo                                                | a) mostrar a finProcedimiento FIN.                              | shift                        |
| Z INICIO procedimiento Identificador (Tipo a                                              | ) mostrar a finProcedimiento FIN.                               | reduce                       |
| Z INICIO procedimiento Identificador (Tipo Identificador                                  | ) mostrar a finProcedimiento FIN.                               | reduce                       |
| Z INICIO procedimiento Identificador (Parametro                                           | ) mostrar a finProcedimiento FIN.                               | reduce                       |
| Z INICIO procedimiento Identificador (ListaParametros                                     | ) mostrar a finProcedimiento FIN.                               | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt                                       | ) mostrar a finProcedimiento FIN.                               | shift                        |
| Z INICIO procedimiento Identificador (ParametrosOpt )                                     | mostrar a finProcedimiento FIN.                                 | shift                        |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar                             | a finProcedimiento FIN.                                         | shift                        |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar a                           | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Identificador               | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar ValorTexto                  | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar ExpresionTexto              | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Impresion                   | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Sentencia                   | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Sentencia Sentencias        | finProcedimiento FIN.                                           | reduce                       |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Sentencias                  | finProcedimiento FIN.                                           | shift                        |
| Z INICIO procedimiento Identificador (ParametrosOpt ) mostrar Sentencias finProcedimiento | FIN.                                                            | reduce                       |
| Z INICIO DefinicionProcedimiento                                                          | FIN.                                                            | reduce                       |
| Z INICIO Sentencia                                                                        | FIN.                                                            | reduce                       |
| Z INICIO Sentencia Sentencias                                                             | FIN.                                                            | reduce                       |
| Z INICIO Sentencias                                                                       | FIN.                                                            | shift                        |
| Z INICIO Sentencias FIN.                                                                   | λ                                                              | reduce                       |
| Z Programa                                                                                | λ                                                              | δ(q1, λ, Programa) ⇒ (q2, λ) |
| Z                                                                                         | λ                                                              | δ(q2, λ, Z) ⇒ (q3, λ)        |
| λ                                                                                         | λ                                                              | accept                       |

> **Comentario:** Este trazado corresponde al parsing ascendente (shift-reduce) con retroceso. Muestra las operaciones `shift` (desplazar) y `reduce` (reducir) hasta aceptar la cadena.

# TP 7:

### Analisis TT y TS

cadena

```
1: INICIO
2:   procedimiento p(texto a)
3:     mostrar a
4:   finProcedimiento
5: FIN.
```

## Tabla de tipos (TT)

| Linea PRG | Cod | Nombre         | TipoBase | Padre | Dimensión | Mínimo | Máximo | Ámbito | Observaciones                 |
| --------- | --- | -------------- | -------- | ----- | --------- | ------ | ------ | ------ | ----------------------------- |
| L1        | 0   | numero         | -1       | -1    | 1         | -1     | -1     | 0      | primitivo                     |
| L1        | 1   | bool           | -1       | -1    | 1         | -1     | -1     | 0      | primitivo (vulnerable/seguro) |
| L1        | 2   | texto          | -1       | -1    | 1         | -1     | -1     | 0      | primitivo                     |
| L1        | 3   | nada           | -1       | -1    | 1         | -1     | -1     | 0      | primitivo ("void")            |
| L1        | 4   | vulnerabilidad | -1       | -1    | 1         | -1     | -1     | 0      | primitivo (sqli/xss/rce)      |
| L5        | —   | —              | —        | —     | —         | —      | —      | —      | Se eliminan todas las líneas  |

> **Comentario:** La TT (tabla de tipos) enumera los tipos disponibles, sus metadatos (padre, dimensión) y comentarios. Aquí solo se listan los primitivos del lenguaje.

## Tabla de Símbolos (TS)

| Linea PRG | Cod | Nombre   | Categoria | Tipo | NumParMin | NumParMax | ListaPar  | Ámbito | Obervaciones                                             |
| --------- | --- | -------- | --------- | ---- | --------- | --------- | --------- | ------ | -------------------------------------------------------- |
| L1        | 0   | probar   | func      | 1    | 3         | 3         | [2, 4, 2] | 0      | Built-in. `probar(texto, vulnerabilidad, texto) -> bool` |
| L1        | 1   | reportar | func      | 3    | 1         | 1         | [2]       | 0      | Built-in. `reportar(texto) -> nada`                      |
| L2        | 2   | p        | proc      | 3    | 1         | 1         | [2]       | 0      | `procedimiento p(texto) -> nada`                         |
| L2        | 3   | a        | var       | 2    | null      | null      | null      | 1      | Parámetro del procedimiento `p`                          |
| L4        |     |          |           |      |           |           |           |        | Se elimina Cod 3 (fin de ámbito del proc)                |
| L5        |     |          |           |      |           |           |           |        | Se eliminan todas las lineas                             |

> **Comentario:** La TS (tabla de símbolos) guarda información sobre funciones, procedimientos y variables: categoría, tipo, cantidad de parámetros y ámbito. Permite rastrear qué identificadores están disponibles en cada nivel.
