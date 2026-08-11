# Test de Preguntas Desafiantes - Día 4: Python Funcional

Evaluación práctica sobre Programación Funcional, Lambdas, List Comprehensions y Módulo Math.

---

### Pregunta 1: Posición de `if`/`else` en List Comprehensions
Considera las siguientes dos líneas de código Python:

```python
# Opción 1:
res_1 = [x * 2 for x in range(10) if x % 2 == 0 else 0]

# Opción 2:
res_2 = [x * 2 if x % 2 == 0 else 0 for x in range(10)]
```

¿Qué sucede al ejecutar cada una?

- A) Ambas líneas ejecutan correctamente y producen el mismo resultado.
- B) La Opción 1 produce un `SyntaxError`; la Opción 2 ejecuta correctamente retornando `[0, 0, 4, 0, 8, 0, 12, 0, 16, 0]`.
- C) La Opción 2 produce un `SyntaxError`; la Opción 1 ejecuta correctamente.
- D) Ambas líneas producen `SyntaxError`.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** En una List Comprehension, la expresión ternaria `[valor_si_true if condicion else valor_si_false for x in iterable]` debe ir ubicada **antes** del `for`. Si se ubica al final (después del `for`), no se permite la cláusula `else`, solo un `if` de filtrado.
</details>

---

### Pregunta 2: Evaluación Perezosa (Lazy Evaluation) con `map()`
¿Cuál es la salida del siguiente fragmento de código en Python 3?

```python
numeros = [1, 2, 3]
resultado = map(lambda x: x * 10, numeros)
print(type(resultado), len(resultado))
```

- A) `<class 'list'> 3`
- B) `<class 'map'> 3`
- C) Lanza un `TypeError` porque los objetos tipo `map` no soportan la función `len()`.
- D) `<class 'generator'> 3`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** En Python 3, `map()` no devuelve una lista en memoria; devuelve un objeto iterador de clase `map` que evalúa los elementos a demanda (lazy evaluation). Los objetos iteradores no tienen definida una longitud por adelantado, por lo que intentar ejecutar `len(resultado)` lanza un `TypeError: object of type 'map' has no len()`. Para obtener la lista y su tamaño hay que envolverlo con `list(map(...))`.
</details>

---

### Pregunta 3: Enlace Tardío (Late Binding) en Lambdas dentro de Bucles
Analiza el comportamiento del siguiente código:

```python
funciones = [lambda x: x + i for i in range(3)]
resultados = [f(10) for f in funciones]
print(resultados)
```

- A) `[10, 11, 12]`
- B) `[12, 12, 12]`
- C) `[0, 1, 2]`
- D) `[10, 10, 10]`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Esta es una trampa muy común de **Late Binding** en cierres (closures) de Python. La variable `i` no se evalúa al definir la lambda, sino al momento de ejecutarla `f(10)`. Cuando se ejecutan las funciones, el bucle `for i in range(3)` ya finalizó y la variable `i` conserva su último valor (`2`). Por lo tanto, las 3 funciones ejecutan `10 + 2 = 12`. Para evitar esto, se debe pasar `i` como parámetro predeterminado: `lambda x, i=i: x + i`.
</details>

---

### Pregunta 4: Validación de NaNs con `math.isnan()`
¿Cuál es la forma correcta de evaluar si una variable `valor` de tipo float contiene `NaN` (Not a Number)?

- A) `valor == float('nan')`
- B) `valor is float('nan')`
- C) `import math; math.isnan(valor)`
- D) `valor == None`

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: C**

**Explicación:** En el estándar IEEE 754 de punto flotante, `NaN` tiene la propiedad única de **no ser igual a nada, ni siquiera a sí mismo** (`float('nan') == float('nan')` evalúa a `False`). La única forma fiable en Python base de comprobar si un valor es `NaN` es utilizar `math.isnan(valor)` (o `np.isnan()` en NumPy).
</details>
