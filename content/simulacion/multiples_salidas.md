---
title: Múltiples mediciones
weight: 2
---

## Problema de ejemplo

Siguiendo el esquema de la sección de _primeros pasos_, vamos a utilizar una variación del ejemplo anterior para aprender la dinámica. Igual que antes, primero vamos a ver la solución completa y luego ir construyendo hasta llegar a la misma.

El enunciado es muy similar al anterior, con la modificación en negrita:

_Sea una urna con 30 bolas verdes, 20 rojas y 50 azules. Se extraen al azar 8 bolas de la urna. Calcular la probabilidad de que se extraigan más bolas rojas que azules **sabiendo que se extrajeron exactamente 2 bolas verdes**._

El ćodigo completo que genera la estimación es el siguiente:

```r
urna <- rep(c("V","R","A"), times=c(30,20,50))
Nrep <- 1000

# definimos los 2 eventos
# A: "se extraen más bolas rojas que azules"
# B: "se extraen exactamente 2 bolas verdes"

# definimos una función que simula 1 y nos devuelve si ocurrieron o no los eventos
simular_1 <- function(){
    # extraemos 8 bolas al azar sin reposición
    extr <- sample(urna, size=8, replace=FALSE)

    # contamos cantidad de azules y rojas
    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    # A ocurre si la cantidad de rojas es > a la cantidad de azules
    A <- n_rojas > n_azules

    # contamos cantidad de verdes
    n_verdes <- sum(extr == 'V')

    # B ocurre si la cantidad de verdes es exactamente 2
    B <- n_verdes == 2

    # devolvemos un vector (A,B)
    c(A,B)
}

# resultados va a ser una matriz de dimension 2 x Nrep
resultados <- replicate(Nrep, {
    simular_1()
})

# cada fila es una de las variables, según el orden que devolví
ocurre_A <- resultados[1,]
ocurre_B <- resultados[2,]

# estimación de P(A|B)
mean(ocurre_A[ocurre_B])
```

Como se puede apreciar, el esquema es _casi idéntico_ al visto en los primeros pasos. La diferencia es que ahora _hacer muchas veces el experimento_ va a devolver múltiples resultados y por lo tanto tenemos que sacarlos fila a fila de lo que devuelva el `replicate`.

Repasando la estructura de _primeros pasos_:

1. Lograr simular 1 vez el experimento
2. Obtener muchas realizaciones del experimento
3. Estimar lo que se pide

### Obtener una realización

Recordando que acá lo importante es lograr obtener _todas las mediciones_ para **una** realización del experimento, el código pasa de ser algo así cuando medimos sólo A:

```r
# extraemos 8 bolas al azar sin reposición
extr <- sample(urna, size=8, replace=FALSE)

# contamos cantidad de azules y rojas
n_rojas <- sum(extr == 'R')
n_azules <- sum(extr == 'A')

# A ocurre si la cantidad de rojas es > a la cantidad de azules
A <- n_rojas > n_azules

# devolvemos A
A
```

a ser así al medir A y B (lo que cambia está resaltado):

```r {hl_lines=[11,12,14,15,17,18]}
# extraemos 8 bolas al azar sin reposición
extr <- sample(urna, size=8, replace=FALSE)

# contamos cantidad de azules y rojas
n_rojas <- sum(extr == 'R')
n_azules <- sum(extr == 'A')

# A ocurre si la cantidad de rojas es > a la cantidad de azules
A <- n_rojas > n_azules

# contamos cantidad de verdes
n_verdes <- sum(extr == 'V')

# B ocurre si la cantidad de verdes es exactamente 2
B <- n_verdes == 2

# devolvemos un vector (A,B)
c(A,B)
```

Como se puede apreciar, es casi lo mismo. La única diferencia fuerte está en cómo devolvemos el resultado, que ahora es con un vector.

Una vez que nos aseguramos que el código funcione correctamente, pasándolo a una función tenemos

```r
simular_1 <- function(){
    # extraemos 8 bolas al azar sin reposición
    extr <- sample(urna, size=8, replace=FALSE)

    # contamos cantidad de azules y rojas
    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    # A ocurre si la cantidad de rojas es > a la cantidad de azules
    A <- n_rojas > n_azules

    # contamos cantidad de verdes
    n_verdes <- sum(extr == 'V')

    # B ocurre si la cantidad de verdes es exactamente 2
    B <- n_verdes == 2

    # devolvemos un vector (A,B)
    c(A,B)
}
```

### Obtener muchas realizaciones

Suponiendo que encapsulamos en una función `simular_1()` la realización de un experimento, el resto es muy parecido a como veníamos trabajando para una medición:

{{< tabs items="for,replicate" >}}
  {{< tab >}}

  ```r
  # definimos los vectores vacíos
  ocurre_A <- c()
  ocurre_B <- c()
  
  # de a 1 los rellenamos
  for(i in 1:Nrep){
    # obtenemos una realización, lo guardamos en variable auxiliar
    # resultado es un vector de 2 elementos (A,B)
    resultado <- simular_1()

    # lo guardamos en el i-ésimo lugar del vector de cada uno
    ocurre_A[i] <- resultado[1]
    ocurre_B[i] <- resultado[2]
  }
  ```

  {{< /tab >}}
  {{< tab >}}

  ```r
  # obtenemos Nrep realizaciones, las guardamos en variable auxiliar
  # resultados va a ser una matriz de dimension 2 x Nrep
  resultados <- replicate(Nrep, {
      simular_1()
  })

  # cada fila es una de las variables, según el orden que devolví
  ocurre_A <- resultados[1,]
  ocurre_B <- resultados[2,]
  ```

  {{< /tab >}}
{{< /tabs >}}

### Realizar las estimaciones

Ahora viene la parte más fácil: operar sobre los vectores de ocurrencias de eventos (o de realizaciones si son variables aleatorias). Como R funciona de forma vectorizada, si queremos hacer cuentas con dos eventos simplemente hacemos:

```r
ocurre_A & ocurre_B # intersección
ocurre_A | ocurre_B # unión

ocurre_A[ocurre_B] # condicional A dado B
ocurre_B[ocurre_A] # condicional B dado A
```

Sabemos que si tenemos un vector de ocurrencias de un evento $X$ guardado en una variable `ocurre_X`, la forma de estimar la probabilidad es haciendo `mean(ocurre_X)`. En nuestro caso nos interesa $P(A|B)$, por lo que hacemos:

```r
mean(ocurre_A[ocurre_B])
```


## Sobre condicionales

### Indexado lógico

Cuando uno hace 

```r
ocurre_A[ocurre_B]
```

por atrás lo que ocurre es [*indexado lógico*](https://bookdown.org/ndphillips/YaRrr/logical-indexing.html). La idea es que si a un vector `X` de largo `n` uno le pasa un vector lógico (es decir, con valores TRUE o FALSE) **de igual longitud** `Y`, R interpreta que `X[Y]` significa que el i-ésimo elemento de i, `X[i]` se considera si y sólo si `Y[i]` es TRUE. En términos de código en R, es equivalente a hacer:

```r
X_sub_Y <- c()

for(i in 1:length(X)){
    if( Y[i]==TRUE ){
        X_sub_Y <- c(X_sub_Y, X[i])
    }
}
```

o en Python a hacer:

{{< tabs items="for,list comprehension" >}}
  {{< tab >}}

  ```python
  X_sub_Y = []
  for i in range(len(X)):
    if Y[i] is True:
        X_sub_Y.append(X[i])
  ```

  {{< /tab >}}
  {{< tab >}}

  ```python
  X_sub_Y = [x_i for x_i, y_i in zip(X,Y) if y_i is True]
  ```

  {{< /tab >}}
{{< /tabs >}}

Algo **muy importante** que se debe destacar es que `X[Y]` **no** tiene el mismo largo que `X`. Podría ser que sí solamente si todos los elementos de `Y` son TRUE, pero lo más común es que no.

En el contexto de simulación de experimentos, esto es importante porque al estimar $P(A|B)$, el _verdadero_ `Nrep` en base al cual vamos a estar estimando va a ser _la cantidad de veces que ocurra $B$_ en nuestras `Nrep` realizaciones.

### Condicionando a eventos de probabilidad 0

En la mayoría de los casos de la materia, cuando condicionamos a un evento lo hacemos sujeto a que ese evento tenga probabilidad positiva. A veces, como cuando queremos estimar la función de regresión $E[Y|X=x]$ con $X$ VA continua, esto no ocurre. En esos casos se utilizan estimaciones por ventanas o _kernels_. Para leer más sobre esto revisar el apunte teórico de Jemina, capítulos 10 y 11.
