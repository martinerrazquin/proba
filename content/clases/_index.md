---
title: Clases
next: clases/1_1
---

Acá tiene que ir una explicación de las cosas de clases y demás.

## Esto es un subtítulo, que no me importa.

Y esto es código para copypastear.

```r {filename="ejemplo.r"}
Nrep <- 10000
x <- c()

for(i in 1:Nrep){
    tiros <- sample(1:4, 2, replace=F)
    x[i] <- sum(tiros)
}

mean(x > 4)
```
