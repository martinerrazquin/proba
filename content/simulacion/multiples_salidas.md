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

a ser así al medir A y B:

```r
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
  # definimos el vector vacío
  ocurre_A <- c()
  ocurre_B <- c()
  
  # de a 1 lo rellenamos
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
