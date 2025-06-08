---
title: Estructuras comunes
weight: 4
---

## Media acumulativa

Suponiendo una muestra $(X_1, X_2, \dots, X_n)$ la estimación acumulativa de la esperanza, es decir todas las estimaciones de $\mathbf{E}[X]$ para $k=1,\dots,n$, se puede hacer con:

```r
cummean <- function(muestra){
    return(
        cumsum(muestra)/1:length(muestra)
    )
}
```

Esto suele ser especialmente útil para, vía `plot`, mostrar cómo una estimación converge al valor teórico (generalmente señalado con un `abline` horizontal de otro color).

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
\widehat{P(B|A)} \approx \frac{\widehat{P(A \cap B)}}{\widehat{P(A)}} = \frac{\\#(A \cap B)}{\\#(A)}
$$

que en términos de código resulta simular el experimento muchas veces, generar dos vectores de ocurrencias `ocurre_A` y `ocurre_B` y calcular

```r
estim_P_B_dado_A <- sum(ocurre_A & ocurre_B) / sum(ocurre_A)
```

Otra forma de hacerlo, cubierta en la página de *Múltiples mediciones*, es directamente truncando:

```r
estim_P_B_dado_A <- mean(ocurre_B[ocurre_A])
```

En la mayoría de los casos no hay diferencia y podés usar la que más natural te resulte.
