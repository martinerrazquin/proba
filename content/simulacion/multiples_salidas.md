---
title: Múltiples mediciones
weight: 4
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

# ver "estructuras comunes"
sum(ocurre_A & ocurre_B) / sum(ocurre_B)
```

Como se puede apreciar, el esquema es _casi idéntico_ al visto en los primeros pasos. La diferencia es que ahora _hacer muchas veces el experimento_ va a devolver múltiples resultados y por lo tanto tenemos que sacarlos fila a fila de lo que devuelva el `replicate`.

