---
title: Funciones útiles
weight: 3
---

{{< callout type="warning" >}}
 Página en construcción: le faltan cosas!
{{< /callout >}}

{{< callout type="info" >}}
 Siempre recordá que podés acceder a la documentación de una función usando ? o help. Por ejemplo, para ver la documentación de la función sample podés escribir `?sample` o `help(sample)`
{{< /callout >}}

## Para generar secuencias

### a:b

El operador `:` sirve para generar todos los números desde el primero hasta el segundo, saltando de a 1 o -1. Es _similar_ al `range` de Python, pero es más flexible e incluye al segundo elemento. En los siguientes ejemplos se indica con un comentario el resultado

```r
1:6 # 1 2 3 4 5 6

4:1 # 4 3 2 1

-5:-2 # -5 -4 -3 -2
```

También funciona con variables y mezclando variables con constantes:
```r
# Definimos las variables
a <- 4
b <- 6

a:b # 4 5 6

a:1 # 4 3 2 1

b:10 # 6 7 8 9 10

3:b # 3 4 5 6

(a-1):(b+2) # 3 4 5 6 7 8
```


### seq

```r

```


### rep

En la mayoría de los casos vamos a utilizar rep bajo una estructura específica que es pasarle un vector de valores a repetir y un vector (de igual longitud) de cuántas veces repetir cada valor. Es muy útil para armar urnas que tienen muchas bolitas!

```r
rep(1/5, times=5) # repite 5 veces 1/5

rep(c('A','V'), times=c(1000,50)) # repite 1000 veces 'A' y 50 veces 'V'

rep(c('equil','no equil'), times=c(2,1)) # repite 2 veces 'equil' y 1 vez 'no equil'

# un dado con dos caras 1, dos caras 2 y una cara 5...
rep(c(1,2,5), times=c(2,2,1))
```

## Para generar números al azar

### sample

Esta función es muy importante porque muchas acciones se pueden pensar como sacar bolas al azar de una urna. Por ejemplo, tirar un dado de 6 caras y observar el resultado es equivalente a sacar 1 bola al azar de una urna que tiene las bolas numeradas 1,2,3,4,5,6. Si quisiera tirar dos veces el mismo dado, sería equivalente a sacar 2 bolas al azar _con reposición_ de la urna. Incluso si fuera un dado desequilibrado, la función `sample` tiene un parámetro para controlar la probabilidad de cada resultado.


El siguiente ejemplo sirve para simular tirar 3 veces un dado de 4 caras que tiene probabilidades 0.3 de salir el 1 y el 4, y 0.15 de salir el 2 y el 3.

```r
sample(
    1:4, # el primer parámetro siempre es la "urna"
    size = 3, # cantidad de extracciones
    replace = TRUE, # si es con reposición o no
    prob = c(0.3,0.15,0.15,0.3) # proba de cada resultado de la urna
)
```

* Si no aclaramos el `size` se asume que se hace una cantidad de extracciones igual a la cantidad de elementos de la urna.
* Si no aclaramos el `replace` se asume que se hace _sin reposición_ (¡como en Proba!).
* Si no aclaramos el `prob` se asume que se hace _al azar_, es decir que todos los resultados son equiprobables.

### distribuciones conocidas

Para cada distribución de las "famosas" existen varias funciones de utilidad que empiezan con las letras _r_, _p_, _d_ o _q_ y siguen con el nimbre de la distribución. En particular, las que empiezan con _r_ sirven para simular valores de esa distribución. Los parámetros que utilizan son siempre cuántos _Nrep_ valores queremos (este siempre es el primero) y los parámetros de la distribución.


```r

runif(1000) # 1000 valores de U(0,1)

runif(10, -3, 5) # 10 valores de U(-3,5)

rnorm(7) # 7 valores de normal estándar

rexp(10000, 3) # 10000 valores de Exp(3)
```

Puede que algunas tengan una definición un poco diferente o usen parametrizaciones diferentes, por lo que es importante siempre chequear la documentación. Por ejemplo, la Geométrica y la Pascal están definidas como la cantidad de _fracasos_ en vez de la cantidad de _intentos_ hasta 1 y $k$ éxitos respectivamente. También la Normal está parametrizada con la media y el desvío estándar en vez de la media y la varianza.


## Para hacer algo muchas veces

### replicate

```r
```

### sapply

Esta función busca cubrir el problema de que queremos hacer algo _para muchos valores de entrada diferentes_. Por ejemplo, supongamos que tenemos una función `estimar_p_A(Nrep)` que estima la probabilidad de cierto evento $A$ simulando _Nrep_ realizaciones del experimento. Si nos piden estimar esa probabilidad para _Nrep_ que puede valer 10, 50, 100 y 1000 podemos simplemente hacer lo siguiente:

```r
Nreps <- c(10, 50, 100, 1000)

estimaciones <- sapply(Nreps, estimar_p_A)
```

La función `sapply` recibe dos parámetros: el primero es un vector de valores que va a tomar la entrada y el segundo es la función a a llamar. En los contextos simples de la materia podemos considerar que el código de arriba es equivalente a haber hecho lo siguiente:

```r
Nreps <- c(10, 50, 100, 1000)

estimaciones <- c()
for (i in 1:length(Nreps)){
    # veo cual Nrep me toca usar ahora
    Nrep <- Nreps[i]

    # hago 1 estimacion
    estimacion <- estimar_p_A(Nrep)

    # la guardo en el i-esimo lugar
    estimaciones[i] <- estimacion
}
```
