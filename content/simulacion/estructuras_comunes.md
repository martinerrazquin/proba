---
title: Estructuras comunes
weight: 3
toc: false
math: true
---

## Media cumulativa

Suponiendo una muestra $(X_1, X_2, \dots, X_n)$ la estimación acumulativa de la esperanza, es decir todas las estimaciones de $\mathbf{E}[X]$ para $k=1,\dots,n$, se puede hacer con:

```r
cummean <- function(muestra){
    return(
        cumsum(muestra)/1:length(muestra)
    )
}
```

### Extensiones

Extensiones de esto se pueden usar para otros momentos como la varianza, que se puede hacer por ejemplo vía:

```r
# suponiendo una muestra que se llame x
e_x <- cummean(x)
e_x2 <- cummean(x^2)

cumvar_x <- e_x2 - e_x^2
```

Dejamos a cargo del alumno entender cómo funciona el código de arriba.

## Estimación de probabilidad condicional

En términos generales para estimar $P(B|A)$ conviene descomponerlo (siempre que $P(A)>0$) en

$$
\hat{P(B|A)} \approx \frac{\hat{P(A \cap B)}}{\hat{P(A)}} = \frac{\#(A \cap B)}{\#(A)}
$$

que en términos de código resulta simular el experimento muchas veces, generar dos vectores de ocurrencias `ocurre_A` y `ocurre_B` y calcular

```r
estim_P_B_dado_A <- sum(ocurre_A & ocurre_B) / sum(ocurre_A)
```

