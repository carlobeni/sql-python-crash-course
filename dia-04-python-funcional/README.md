# Día 4: Python Funcional - Programación Funcional & Módulo Math

Bienvenido al Día 4 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Definir funciones personalizadas avanzadas con parámetros posicionales, nombrados, `*args` y `**kwargs`.
2. Dominar las expresiones anónimas `lambda`.
3. Transformar colecciones utilizando las funciones de alto orden `map()` y `filter()`.
4. Dominar la sintaxis y patrones de List Comprehensions (con condicionales `if`/`else` de una sola línea).
5. Utilizar las funciones matemáticas avanzadas de la librería estándar `math`.

---

## Teoría Explicada

### 1. Definición de Funciones Avanzadas

* **Firma de función:** `def nombre_func(param1, param2=defecto, *args, **kwargs):`
* `*args`: Empaqueta argumentos posicionales arbitrarios en una **tupla**.
* `**kwargs`: Empaqueta argumentos nombrados adicionales en un **diccionario**.

```python
def calcular_comision(monto, tasa_base=0.02, **opciones):
    comision = monto * tasa_base
    if opciones.get("es_vip", False):
        comision *= 0.5  # 50% de descuento para clientes VIP
    return comision

print(calcular_comision(100000, es_vip=True))  # Retorna 1000.0
```

---

### 2. Funciones Anónimas (`lambda`)

Una función `lambda` es una función pequeña de una sola expresión que no requiere una definición formal `def`.
* **Sintaxis:** `lambda parametro1, parametro2: expresion_retornada`

```python
# Función tradicional
def calcular_iva(monto):
    return monto * 1.21

# Equivalente con lambda
calcular_iva_lambda = lambda monto: monto * 1.21

print(calcular_iva_lambda(100))  # 121.0
```

---

### 3. Transformación Funcional de Colecciones: `map()` y `filter()`

* **`map(funcion, iterable)`**: Aplica la función especificada a cada uno de los elementos de la colección. Retorna un iterador / generador (evaluación perezosa / lazy evaluation).
* **`filter(funcion_predicado, iterable)`**: Conserva únicamente los elementos donde `funcion_predicado` retorna `True`.

```python
saldos = [150000.0, 45000.0, 1200000.0, 0.0, -15000.0]

# Convertir saldos en ARS a USD (tipo de cambio 1200) usando map y lambda
saldos_usd = list(map(lambda s: round(s / 1200, 2), saldos))

# Filtrar solo saldos estrictamente positivos usando filter
saldos_positivos = list(filter(lambda s: s > 0, saldos))
```

---

### Regla de Oro Itaú #3: Sintaxis Ágil en Una Sola Línea

> En la evaluación de Python se mide la capacidad de escribir transformaciones limpias y expresivas en una sola línea utilizando List Comprehensions y `map()` / `lambda`.

#### Sintaxis de List Comprehensions:
Existen dos variantes fundamentales en List Comprehensions que se deben diferenciar con precisión:

1. **Solo Filtrado (Cláusula `if` al final):**
   `[expresion for x in iterable if condicion]`

2. **Transformación Condicional (Ternario `if-else` al inicio):**
   `[expresion_si_true if condicion else expresion_si_false for x in iterable]`

```python
numeros = [-10, 5, 0, 12, -3, 20]

# Caso 1: Filtrar solo números positivos elevados al cuadrado
cuadrados_positivos = [x**2 for x in numeros if x > 0]
# Resultado: [25, 144, 400]

# Caso 2: Etiquetar como 'POSITIVO' o 'NO_POSITIVO' para todos los elementos
etiquetas = ["POSITIVO" if x > 0 else "NO_POSITIVO" for x in numeros]
# Resultado: ['NO_POSITIVO', 'POSITIVO', 'NO_POSITIVO', 'POSITIVO', 'NO_POSITIVO', 'POSITIVO']

# Combinación con map y lambda (equivalente en una línea)
transformados = list(map(lambda x: x**2 if x > 0 else 0, numeros))
```

---

### 4. Módulo `math` de la Librería Estándar

El módulo `math` incluye funciones optimizadas para operaciones matemáticas:

* `math.isnan(x)`: Comprueba si un valor es `NaN` (Not a Number). Crucial para Data Prep.
* `math.ceil(x)`: Redondea hacia arriba al entero más cercano.
* `math.floor(x)`: Redondea hacia abajo al entero más cercano.
* `math.isclose(a, b, rel_tol=1e-9)`: Evalúa si dos números flotantes son prácticamente iguales (evita errores de precisión IEEE 754).
* `math.sqrt(x)`: Raíz cuadrada.

```python
import math

monto_cuota = 15420.35
print(math.ceil(monto_cuota))   # 15421
print(math.floor(monto_cuota))  # 15420

val = float('nan')
print(math.isnan(val))          # True
```
