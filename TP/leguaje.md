# Lenguaje a crear
## Objetivo
Ser un lenguaje de programación en español que permita expresar y automatizar tareas de seguridad (detectar vulnerabilidades, generar payloads, crear reportes) de forma clara y accesible, con reglas simples y cercanas al ámbito de seguridad informática

## Alcance
### Incluye:

-  Tipos: numero, url (texto), payload (texto), vulnerabilidad (sqli|xss|rce|lfi), bool (vulnerable|seguro), lista<tipo_base>.

-  Sentencias: asignación, impresión, condicional (evaluar), iteración (mientras), funciones, procedimientos, operaciones de lista (agregar, quitar en, limpiar).

## Tipos de datos

- **numero** → valor numérico entero.

- **url** → texto (URLs válidas para testing de seguridad). Debe seguir el formato: `http://` o `https://` seguido de dominio válido.

- **payload** → texto (cadenas de ataque predefinidas).

- **regex** → expresión regular para validación de patrones de seguridad.

- **vulnerabilidad** → sqli | xss | rce | lfi (tipos de vulnerabilidades).

- **bool** → vulnerable | seguro.

- **lista<tipo_base>** → lista tipada cuyos elementos son **numero**, **url**, **payload**, **vulnerabilidad**, **bool** o **regex**.

  - No existen literales de lista; se crean vacías con **vacia** y se completan con operaciones.

  - El primer indice de la lista es 1.

## Estructura de programa

Un programa comienza con **INICIO** y termina con **FIN.**. Todas las sentencias válidas van entre esas dos palabras clave.

### Sentencias principales
### Asignación

- Declaración + asignación: ```anotar <tipo> <variable> = <valor>```

- Modificación: ```anotar <variable> = <nuevo_valor>```

- Listas:

  - Crear: ```anotar lista<tipo_base> <lista> = vacia```

  - Acceso: ```<lista>[<indice>]```

### Impresión

**mostrar** acepta una expresión de texto que puede concatenar varias partes con + (variables, números, booleanos, accesos a lista, llamadas a función).
Ej.: ```mostrar "Sitio: " + url + " | Vulnerabilidad: " + tipo```

### Condicional

```evaluar <condicion>``` ejecuta un bloque ```si pasa:``` y, opcionalmente, un bloque ```si no pasa:```.

Negación: ```no <condicion>```



### Iteración (únicamente mientras)

```mientras <condicion> hacer``` repite mientras la condición sea verdadera.

## Operaciones de lista
- ```agregar <valor> a <lista>``` (Se agrega al final de lista)

- ```quitar en <lista>[<indice>]``` (Elimina por índice)

- ```limpiar <lista>``` (Deja la lista vacía)

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

## Comentarios

- De línea: ```// comentario```

- De bloque: ```/* comentario */```

## Operadores

- **Aritméticos:** +, -, *, / con precedencia: * / > + - (asociatividad izquierda).
Se admiten paréntesis para agrupar: ( … ).

- **Relacionales:** ==, !=, <, >, <=, >= (se permiten en ambos lados valores/expresiones).

- **Lógicos:** y, o, y prefijo no.

## Especificaciones léxicas
- Sensibilidad a mayúsculas/minúsculas: sí.

- Comentarios: ```// …``` (línea), ```/* … */``` (bloque).

- Léxicos básicos: números enteros no negativos; textos entre comillas "…".

- Operadores y signos: ```+ - * / == != < > <= >= ( ) [ ] , ``` y lógicos ```y```, ```o```, ```no```.

- Palabras clave principales: ```INICIO```, ```FIN.```, ```anotar```, ```mostrar```, ```evaluar```, ```si pasa:```, ```si no pasa:```, ```mientras```, ```hacer```, ```funcion```, ```retornar```, ```finFuncion```, ```procedimiento```, ```finProcedimiento```, ```agregar```, ```quitar```, ```en```, ```limpiar```, ```entre```, ```vacia```, ```vulnerable```, ```seguro```, ```probar```, ```inyectar```, ```reportar```, ```pasa```, ```salir```, ```validar_url```, ```coincidir_regex```.
 
## Especificaciones sintácticas
-  Programa: INICIO <sentencias> FIN.

-  Asignación:

  -  Declaración: ```anotar <tipo> <id> = <valor>```

  -  Modificación: ```anotar <id> = <valor>```

  -  Listas: ```anotar lista<tipo_base> L = vacia```; acceso ```L[i]```

- Impresión: mostrar <expresion_texto> (concatenación con +).

-  Condicional:
```
evaluar <condicion>
    si pasa: <sentencias>
    si no pasa: <sentencias>   // opcional
```
-  Iteración: ```mientras <condicion> hacer <sentencias>```.

-  Funciones: Se debe definir que tipo de dato devolvera la funcion al momento de crearla.

-  Expresiones: precedencia * / > + -; paréntesis para agrupar.

-  Indexación de listas: 1-based (primer elemento es índice 1).
 
## Especificaciones semánticas
-  **Tipos:** verificación estática; se declara al momento de crear la variable

-  **vulnerabilidad:** texto en [sqli|xss|rce|lfi]; asignar fuera de rango es error.

-  **Listas:** tipo base estricto; se declara al momento de crear la lista, se puede inicializar vacia
  
-  **mostrar:** acepta una expresión de texto que puede concatenar varias partes con + (variables, números, booleanos, accesos a lista, llamadas a función).

-  **Ámbitos:** variables de funciones/procedimientos son locales.

## Funciones predefinidas

- **pasa**: Evalúa si una condición es verdadera. Retorna `vulnerable` si es verdadero, `seguro` si es falso.
- **reportar**: Genera un reporte de vulnerabilidad encontrada con el mensaje especificado.
- **salir**: Termina la ejecución del programa o sale de un bucle.
- **validar_url**: Verifica si una cadena es una URL válida. Retorna `vulnerable` si es válida, `seguro` si no.
- **coincidir_regex**: Evalúa si un texto coincide con una expresión regular. Retorna `vulnerable` si coincide, `seguro` si no.

## Reglas semánticas

- vulnerabilidad debe estar en [sqli|xss|rce|lfi].

- Tipos de listas estrictos (solo tipo_base permitido).

- Variables de función/procedimiento son locales.

- Todo valor se convierte a texto al imprimir/concatenar en mostrar.

## Ejemplos de uso

### Ejemplo 1: Scanner de SQL Injection con iteración
```
INICIO
    anotar url objetivo = "https://ejemplo.com/login"
    anotar numero contador = 1
    anotar lista<texto> payloads = vacia
    
    agregar payloads en "admin' OR 1=1--"
    agregar payloads en "admin' UNION SELECT 1,2,3--"
    agregar payloads en "'; DROP TABLE users; --"
    
    mientras contador <= 3 hacer
        anotar payload = payloads[contador]
        mostrar "Probando payload " + contador + ": " + payload
        
        evaluar probar_sql(objetivo, payload)
            si pasa:
                mostrar "¡Vulnerabilidad SQL detectada!"
                reportar "SQL Injection en " + objetivo
            si no pasa:
                mostrar "Payload " + contador + " no vulnerable"
        
        anotar contador = contador + 1
    
    mostrar "Escaneo SQL completado"
FIN.
```

### Ejemplo 2: Detector de XSS con condicionales
```
INICIO
    anotar url sitio = "https://ejemplo.com/comentarios"
    anotar vulnerabilidad tipo = xss
    anotar payload xss_payload = "<script>alert(1)</script>"
    
    mostrar "Iniciando test de " + tipo + " en " + sitio
    
    evaluar inyectar_xss(sitio, xss_payload)
        si pasa:
            mostrar "¡XSS detectado!"
            anotar bool resultado = vulnerable
        si no pasa:
            mostrar "No se detectó XSS"
            anotar bool resultado = seguro
    
    evaluar resultado == vulnerable
        si pasa:
            mostrar "Sitio vulnerable a Cross-Site Scripting"
            reportar "XSS en " + sitio
        si no pasa:
            mostrar "Sitio seguro contra XSS"
FIN.
```

### Ejemplo 3: Test de autenticación con funciones
```
INICIO
    anotar url admin = "https://ejemplo.com/admin"
    anotar numero intentos = 0
    
    funcion testear_auth: bool(url: texto)
        mostrar "Probando bypass de autenticación en " + url
        retornar vulnerable
    finFuncion
    
    mientras intentos < 5 hacer
        anotar intentos = intentos + 1
        mostrar "Intento " + intentos + " de 5"
        
        evaluar testear_auth(admin)
            si pasa:
                mostrar "¡Bypass de autenticación exitoso!"
                reportar "Auth Bypass en " + admin
                salir
            si no pasa:
                mostrar "Autenticación segura en intento " + intentos
    
    mostrar "Test de autenticación completado"
FIN.
```

## Ejemplo Completo: Scanner de Vulnerabilidades
```
INICIO

// Listas: URLs y tipos de vulnerabilidades. Se inicializan vacías
anotar lista<url> sitios = vacia
anotar lista<vulnerabilidad> tipos = vacia
anotar lista<bool> resultados = vacia

// Carga de sitios a testear
agregar "https://ejemplo.com/login" a sitios
agregar "https://ejemplo.com/comentarios" a sitios
agregar "https://ejemplo.com/admin" a sitios

// Carga de tipos de vulnerabilidades
agregar sqli a tipos
agregar xss a tipos
agregar rce a tipos

// [https://ejemplo.com/login, https://ejemplo.com/comentarios, https://ejemplo.com/admin]
// [sqli, xss, rce]

// Cantidad de tests a realizar
anotar numero cantidad_tests = 3

// Procedimiento: imprime un reporte de vulnerabilidad
procedimiento mostrarReporte(url sitio, vulnerabilidad tipo, bool estado)
    mostrar "Sitio: " + sitio + " | Tipo: " + tipo + " | Estado: " + estado
finProcedimiento

// Función: estado según tipo de vulnerabilidad (bool)
funcion bool testearVulnerabilidad(url sitio, vulnerabilidad tipo)
    evaluar tipo == sqli
        si pasa:
            retornar probar_sql(sitio, "admin' OR 1=1--")
        si no pasa:
            evaluar tipo == xss
                si pasa:
                    retornar inyectar_xss(sitio, "<script>alert(1)</script>")
                si no pasa:
                    evaluar tipo == rce
                        si pasa:
                            retornar probar_rce(sitio, "ping -c 1 127.0.0.1")
                        si no pasa:
                            retornar seguro
finFuncion

// Función: contar vulnerabilidades encontradas
funcion numero contarVulnerabilidades(lista<bool> resultados, numero n)
    anotar numero i = 1
    anotar numero contador = 0
    mientras i <= n hacer
        evaluar resultados[i] == vulnerable
            si pasa:
                anotar contador = contador + 1
        anotar i = i + 1
    retornar contador
finFuncion

// Recorrido con 'mientras' para testear todos los sitios
mostrar "Iniciando escaneo de vulnerabilidades:"
anotar numero i = 1
mientras i <= cantidad_tests hacer
    anotar url sitio_actual = sitios[i]
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
quitar en sitios[3]
quitar en tipos[3]
quitar en resultados[3]
anotar cantidad_tests = 2

mostrar "Limpiando listas..."
limpiar sitios
limpiar tipos
limpiar resultados
FIN.
```

## Salida
```
Iniciando escaneo de vulnerabilidades:
Sitio: https://ejemplo.com/login | Tipo: sqli | Estado: vulnerable
Sitio: https://ejemplo.com/comentarios | Tipo: xss | Estado: seguro
Sitio: https://ejemplo.com/admin | Tipo: rce | Estado: vulnerable
Total de vulnerabilidades encontradas: 2
Quitando último test...
Limpiando listas...
```

### Ejemplo 4: Validación de URLs y Expresiones Regulares
```
INICIO
    anotar url sitio_test = "https://ejemplo.com/login"
    anotar regex patron_sql = ".*' OR 1=1.*"
    anotar regex patron_xss = ".*<script>.*"
    
    mostrar "Validando URL: " + sitio_test
    
    evaluar validar_url(sitio_test)
        si pasa:
            mostrar "URL válida - procediendo con tests"
            
            evaluar coincidir_regex("admin' OR 1=1--", patron_sql)
                si pasa:
                    mostrar "Patrón SQL detectado en payload"
                    reportar "SQL Injection pattern encontrado"
                si no pasa:
                    mostrar "Payload no coincide con patrón SQL"
            
            evaluar coincidir_regex("<script>alert(1)</script>", patron_xss)
                si pasa:
                    mostrar "Patrón XSS detectado en payload"
                    reportar "XSS pattern encontrado"
                si no pasa:
                    mostrar "Payload no coincide con patrón XSS"
        si no pasa:
            mostrar "URL inválida - abortando tests"
FIN.
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

<tipo> ::= numero | url | payload | vulnerabilidad | bool | lista<tipo_base>

<tipo_base> ::= numero | url | payload | vulnerabilidad | bool | regex

<impresion> ::= mostrar <expresion_texto>

<expresion_texto> ::= <valor_texto> | <valor_texto> + <expresion_texto>

<valor_texto> ::= <texto> | <identificador> | <booleano> | <numero>
                | <acceso_lista> | <llamada_funcion>

<condicional> ::= evaluar <condicion> <bloque_condicional>

<bloque_condicional> ::= si pasa: <sentencias>
                       | si pasa: <sentencias> si no pasa: <sentencias>

<condicion> ::= no <condicion>
              | <identificador> entre <valor> y <valor>
              | <valor> <operador_relacional> <valor>
              | <condicion> <operador_logico> <condicion>
              | <booleano> | <identificador>

<iteracion> ::= mientras <condicion> hacer <sentencias>

<valor>   ::= <valor> <op_suma> <termino> | <termino>
<termino> ::= <termino> <op_mul> <factor> | <factor>
<factor>  ::= <numero> | <texto> | <identificador> | <booleano>
            | <acceso_lista> | <llamada_funcion> | "(" <valor> ")"

<op_suma> ::= + | -
<op_mul>  ::= * | /

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

<operador_relacional> ::= == | != | < | > | <= | >=
<operador_logico> ::= y | o

<numero> ::= <digito> { <digito> }
<texto> ::= '"' { <letra> | <digito> } '"'
<identificador> ::= <letra> { <letra> | <digito> | _ }

<letra> ::= a | b | ... | z | A | B | ... | Z
<digito> ::= 0 | 1 | ... | 9

<comentario_linea>  ::= "//" {cualquier_caracter_excepto_salto}
<comentario_bloque> ::= "/*" {cualquier_caracter} "*/"
```
