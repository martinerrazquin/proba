---
title: Primeros pasos
weight: 1
---

## Problema de ejemplo

Vamos a basarnos en un problema de ejemplo para aprender la dinámica. Primero vamos a ver la solución completa y luego ir construyendo hasta llegar a la misma.

El enunciado es el siguiente:

_Sea una urna con 30 bolas verdes, 20 rojas y 50 azules. Se extraen al azar 8 bolas de la urna. Calcular la probabilidad de que se extraigan más bolas rojas que azules._

El ćodigo completo que genera la estimación es el siguiente:

```r
urna <- rep(c("V","R","A"), times=c(30,20,50))
Nrep <- 1000

# definimos una función que simula 1 y nos devuelve si ocurrió o no el evento
simular_1 <- function(){
    # extraemos 8 bolas al azar sin reposición
    extr <- sample(urna, size=8, replace=FALSE)

    # contamos cantidad de azules y rojas
    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    n_rojas > n_azules
}

# A: "se extraen más bolas rojas que azules"
ocurre_A <- replicate(Nrep, {
    simular_1()
})

# estimamos
mean(ocurre_A)
```

En términos generales, el esquema de trabajo general que vamos a seguir es:

1. Lograr simular 1 vez el experimento
2. Obtener muchas realizaciones del experimento
3. Estimar lo que se pide

### Obtener una realización

Esta es la parte más difícil porque requiere entender qué se está haciendo y qué se quiere observar del experimento.

Para empezar, necesitamos definir una urna de donde sacar las bolas. Si la urna fuera de 3 bolas azules, 2 rojas y 1 verde uno podría simplemente definir la urna _a mano_ así:

```r
urna <- c('A','A','A','R','R','V')
```

El problema es que al momento que la cantidad de bolas de la urna aumenta, se vuelve muy difícil definirlo a mano, además de ser muy propenso a errores. Para eso utilizamos la función `rep`, cuyo argumento `times` nos permite indicarle cuántas veces repetir cada elemento del vector de valores:

```r
urna <- rep(c("V","R","A"), times=c(30,20,50))
```

Ahora necesitamos extraer 8 bolitas de la urna. Lo vamos a hacer al azar, y como no aclara, las extracciones son _sin reposición_. Para esto usamos la función `sample` y sus parámetros `size` y `replace`.

```r
extr <- sample(urna, size=8, replace=FALSE)
```

Una vez extraídas las bolitas, necesitamos contar cuántas rojas y cuántas azules hay. Acá es importante entender cómo se ve un vector de extracción:

```r
R R R V V A V V
```

Como R vectoriza las operaciones por default, cuando uno hace una comparación respecto de un valor, por ejemplo `extr == 'V'` resulta un vector lógico con valores TRUE o FALSE según el resultado:

```r
FALSE FALSE FALSE TRUE TRUE FALSE TRUE TRUE
```

En el fondo, para R **un TRUE es un 1 y un FALSE es un 0**. De esta manera, calcular el `sum()` de un vector lógico cuenta la cantidad de valores TRUE, es decir la frecuencia absoluta. Al mismo tiempo, calcular el `mean()` entonces calcula la frecuencia relativa, que es la que vamos a utilizar para estimar probabilidades.

Retomando, la cantidad de bolitas rojas extraídas entonces va a ser la cantidad de veces que da TRUE la comparación con `=='R'`:

```r
n_rojas <- sum(extr == 'R')
```

Y aplicamos lo mismo para las bolitas azules. Definiendo el evento $A$: _"Se extraen más bolitas rojas que azules"_ y siendo que nos piden estimar $P(A)$, en el código _medir si ocurrió A_ es el resultado de la comparación

```r
n_rojas > n_azules
```

Opcionalmente, podemos meter todo adentro de una función que simplemente devuelva los resultados que nos interesa medir, para que luego sea más fácil de leer el código. **Es muy importante testear que el código funcione antes de meterlo en una función.**

```r
simular_1 <- function(){
    # extraemos 8 bolas al azar sin reposición
    extr <- sample(urna, size=8, replace=FALSE)

    # contamos cantidad de azules y rojas
    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    n_rojas > n_azules
}
```

Recordar que en una función, el último renglón se devuelve _por default_, por lo que es lo mismo que si escribiéramos `return(n_rojas > n_azules)`. Da lo mismo, así que escribilo como mejor lo entiendas vos.

### Obtener muchas realizaciones

Para estimar cualquier cosa no alcanza una muestra de tamaño 1, necesitamos que sea una muestra _grande_ (y cuanto más grande mejor la estimación **siempre**). Para ordenarnos y controlar desde un único punto cuántas repeticiones hacemos, vamos a definir una variable `Nrep` que vamos a usar para esto.

```r
Nrep <- 1000
```

Además, como la urna es algo que siempre va a ser igual para todos los experimentos y _no la vamos a alterar_, la podemos definir una sola vez y listo, así que la vamos a crear en la misma "sección" de cosas iniciales junto con el `Nrep`:

```r
urna <- rep(c("V","R","A"), times=c(30,20,50))
Nrep <- 1000
```

{{< callout type="info" >}}
 Tip: al principio conviene usar un `Nrep` _chico_, por ejemplo 5 o 10, para testear que todo funcione bien. Cuando estamos seguros de que el código hace lo que queremos que haga, cambiamos el valor a algo razonable como 1000 o 10000.
{{< /callout >}}

Algo bueno es que una vez establecido el código para generar una realización del experimento, generar muchas es extremadamente sencillo. Hay muchas formas de hacer esto, de las cuales nosotros vamos a considerar dos _estilos_, uno usando un ciclo `for` y otro usando `replicate`. Vos usá el que más cómodo te resulte. En general, el `for` (estilo imperativo) suele gustarle más a los que ya están acostumbrados a programar pero en otro lenguaje, mientras que el `replicate` (estilo funcional) suele serle más intuitivo a aquellos que prefieren ver esto como un flujo de datos.

{{< tabs items="for,replicate" >}}
  {{< tab >}}

  ```r
  # definimos el vector vacío
  ocurre_A <- c()
  
  # de a 1 lo rellenamos
  for(i in 1:Nrep){
    extr <- sample(urna, size=8, replace=FALSE)

    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    ocurrencia <- n_rojas > n_azules

    # lo guardamos en el i-ésimo lugar del vector
    ocurre_A[i] <- ocurrencia
  }
  ```

  {{< /tab >}}
  {{< tab >}}

  ```r
  # A replicate le pasamos cuántas repeticiones y el código a repetir
  ocurre_A <- replicate(Nrep, {
    extr <- sample(urna, size=8, replace=FALSE)

    n_rojas <- sum(extr == 'R')
    n_azules <- sum(extr == 'A')

    n_rojas > n_azules    
  })
  ```

  {{< /tab >}}
{{< /tabs >}}

Si además hicimos la tarea de encapsular la realización de un experimento en una función, el código **en vez de lo de arriba** se va a ver así:

{{< tabs items="for,replicate" >}}
  {{< tab >}}

  ```r
  # definimos el vector vacío
  ocurre_A <- c()
  
  # de a 1 lo rellenamos
  for(i in 1:Nrep){
    # lo guardamos en el i-ésimo lugar del vector
    ocurre_A[i] <- simular_1()
  }
  ```

  {{< /tab >}}
  {{< tab >}}

  ```r
  # A replicate le pasamos cuántas repeticiones y el código a repetir
  ocurre_A <- replicate(Nrep, {
    simular_1()    
  })
  ```

  {{< /tab >}}
{{< /tabs >}}

### Realizar las estimaciones

Una vez que, de la forma que sea, uno obtuvo los vectores de ocurrencias (o realizaciones, si son VAs), llega la parte más fácil: estimar en base a la muestra. Esto suelen ser 1 o 2 renglones para cada estimación.

Como aprendiste (o vas a aprender) en la guía 9, las probabilidades se estiman usando la frecuencia relativa, por lo que vamos a usar la función `mean()` sobre el vector de ocurrencias del evento que nos interese:

```r
mean(ocurre_A)
```

Y con esto estamos.

### Extra: ploteamos la convergencia de la estimación

Haciendo las cuentas (un tanto engorrosas) uno llega a que el resultado teórico es
$$
P(A) = \frac{\sum_{r=1}^8\sum_{a=0}^{r-1} \binom{20}{r}\binom{50}{a}\binom{30}{8-a-r}}{\binom{100}{8}} \approx 0.0906
$$

Para mostrar que la estimación converge uno debería hacer la media (usando `mean`) de las primeras _k_ simulaciones con _k_ de 1 a Nrep, y hacer un `plot`. Adicionalmente, conviene usar `abline` para trazar una recta horizontal (generalmente de otro color, para que se distinga) sobre el valor teórico. Nuevamente, si uno hace uso de la función `cummean` definida en la página de [_*_estructuras_comunes_](/content/simulacion/estructuras_comunes.md) son 2 renglones.

```r
plot(
    cummean(ocurre_A), 
    type='l', 
    main='Convergencia de la estimación de P(A)', 
    xlab='Nrep', 
    ylab='estimación de P(A)'
)
abline(h=0.0906, col='green')
```

Y el resultado es algo así:

![Imagen convergencia](/images/bases_convergencia_ejemplo1.png)

## Conclusiones

Desarrollamos, utilizando un ejemplo, un esquema de trabajo general que nos va a servir para cualquier ejercicio en el que necesitemos simular para realizar una estimación. También mostramos, sobre el mismo ejemplo, cómo hacer un gráfico de convergencia de la estimación.

La próxima página, [_Múltiples mediciones_](/content/simulacion/multiples_salidas.md) cubre cómo extender lo visto a cuando en un mismo experimento queremos medir más de un evento o variable aleatoria, por ejemplo para estimar la probabilidad de una intersección o una covarianza entre variables.

El resto del material va a tratar sobre cuestiones _útiles_ más que necesarias.
