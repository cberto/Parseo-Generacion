# 📘 Especificación del Lenguaje — **MiLenguaje**

---

## 🔹 Lenguaje a crear

**MiLenguaje** es un lenguaje de programación didáctico y esotérico, diseñado para practicar análisis léxico, sintáctico y semántico.  
Su principal particularidad es la **restricción de identificadores a solo vocales**, junto con un **sistema de tipos estático y fuerte**, y una sintaxis simple que permite modelar **funciones, asignaciones, bucles, condicionales, expresiones y manejo de errores**.

---

## 🎯 Objetivo

- Brindar un **lenguaje minimalista** para ejercitar construcción de analizadores (léxico, sintáctico y semántico).
- Permitir expresar programas estructurados con **tipado estático y control de flujo básico**.
- Incluir **recursividad** y **manejo de errores** para enriquecer los ejemplos académicos.

---

## 📌 Alcance

### Incluye

- Declaración y asignación de variables con tipo.
- Funciones con parámetros, valores por defecto y **retorno obligatorio**.
- Control de flujo:
  - `si / sino / sino si`
  - `bucle (init; cond; inc/dec)`
  - `salir` / `seguir` en bucles.
- Operadores aritméticos, lógicos y de comparación
- **Recursividad** directa e indirecta.
- Manejo de errores:
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
- Palabras clave → pueden contener consonantes (`funcion`, `bucle`, etc.).
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

tipo           ::= "cad" | "num" | "log"

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

Parámetros por valor, con defaults permitidos.

Recursión permitida (directa o mutua).

Cada invocación crea un nuevo entorno.

Control de flujo

si/sino/sino si: condicionales encadenados.

bucle: ejecuta sobre números, con inc/dec.

salir: termina el bucle actual.

seguir: pasa a la siguiente iteración.

Manejo de errores

lanzar <expr>: detiene ejecución normal y transfiere control a manejadores.

intenta/captura/siempre: bloques para manejar errores.



print

Efecto: muestra en pantalla el valor.

Retorno: num = cantidad de caracteres impresos.
```

## 📖 Ejemplos

### Recursividad

```
funcion fa:num(n:num) {
  si (n <= 1) {
    retorno 1
  }
  retorno n * fa(n - 1)
}
print(fa(5))   // 120
```

### Condicional extendido

```
num: num = 2

si (num > 3) {
  print(a)
} sino si (num == 2) {
  print(e)
} sino {
  print(i)
}


```

### Manejo de errores

```
funcion eu:num(x:num) {
  intenta {
    retorno 10 / x
  }
  captura(e: num) {
    print(e)
    retorno 0
  }
  siempre {
    print(a)
  }
}
print(eu(0))
```

### Operaciones con cadenas

```
funcion saludar: cad(nombre: cad) {
  retorno "aei " + nombre
}

funcion esVocal: log(c: cad) {
  retorno c == "a" oo c == "e" oo c == "i" oo c == "o" oo c == "u"
}

mensaje: cad = "aei"
print(saludar(mensaje))  // Imprime: aei aei
print(esVocal("a"))      // Imprime: ver

### Operaciones entre tipos diferentes

```

// Operaciones aritméticas entre tipos
resultado1: num = 5 + "aei" // 5 + 3 = 8 (num + longitud de cad)
resultado2: num = "ou" - ver // 2 - 1 = 1 (longitud de cad \* ver)
resultado3: num = fal / "a" // 0 / 1 = 0 (fal / longitud de cad)

// Comparaciones entre tipos
comparacion1: log = 10 > "aei" // 10 > 3 = ver
comparacion2: log = "a" < 5 // 1 < 5 = ver
comparacion3: log = ver == "ou" // 1 == 2 = fal

// Operaciones lógicas entre tipos
logico1: log = 5 yy "aei" // ver yy ver = ver (ambos no vacíos)
logico2: log = fal oo "a" // fal oo ver = ver (al menos uno verdadero)
logico3: log = no "aei" // no ver = fal (cadena no vacía)

```


```
