---
title: Primeros pasos
weight: 1
toc: false
math: true
---

## Problema de ejemplo

Vamos a basarnos en un problema de ejemplo para aprender la dinámica. El enunciado es el siguiente:

*Sea una urna con 30 bolas verdes, 20 rojas y 50 azules. Se extraen al azar 8 bolas de la urna. Calcular la probabilidad de que se extraigan más bolas rojas que azules.*

El ćodigo que genera la estimación es el siguiente:


```r
urna <- rep(c("V","R","A", times=c(30,20,50)))
Nrep <- 1000



# A: "se extraen más bolas rojas que azules"
ocurre_A <- replicate(Nrep, {
    simular_1()
})

```



En términos generales, el esquema de trabajo general que vamos a seguir es:

1. Lograr simular 1 vez el experimento
2. Obtener muchas realizaciones del experimento
3. Estimar lo que se pide


{{% steps %}}

### Obtener una realización

Esta es la parte más difícil
