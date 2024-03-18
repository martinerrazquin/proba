---
title: Clases
next: clases/1_1
---

En esta sección, al menos por ahora, van a estar las cosas referidas a la primera parte de la materia, previa al parcial. Esto está en etapa muy temprana de construcción, así que aún no tengo idea si la segunda parte va a continuarse acá o en otra sección.

{{< callout type="info" >}}
  Hay un [*bug*](https://es.wikipedia.org/wiki/Error_de_software) que *a veces* al navegar entre las clases, descarga automáticamente un archivo HTML **vacío** (0 bytes). Si bien esto es 100% inofensivo, la única manera que encontré de reproducirlo es *si se cambia entre páginas muy rápido, antes que carguen por completo*. Si molesta, dale un ratito a que cargue del todo una página antes de cambiar a otra, o si querés buscar algo podes usar el buscador de arriba a la derecha.
{{< /callout >}}


Acá dejo un código en R completamente random, porque sí.

```r {filename="ejemplo.r"}
Nrep <- 10000
x <- c()

for(i in 1:Nrep){
    tiros <- sample(1:4, 2, replace=F)
    x[i] <- sum(tiros)
}

mean(x > 4)
```
