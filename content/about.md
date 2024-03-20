---
title: About
type: about
---

Algún día acá irá algo. Como por ahora no tengo nada para poner, dejo un código en R medio random.

```r {filename="ejemplo.r"}
Nrep <- 10000
x <- c()

for(i in 1:Nrep){
    tiros <- sample(1:4, 2, replace=F)
    x[i] <- sum(tiros)
}

mean(x > 4)
```
