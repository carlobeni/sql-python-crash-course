# Día 3: Python Base - Python Básico & Estructuras de Datos

Bienvenido al Día 3 del Plan Intensivo de Preparación Acelerada para Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Comprender la arquitectura del entorno Python y uso de Jupyter Notebooks.
2. Dominar exhaustivamente las estructuras de datos fundamentales: **Cadenas (Strings)**, **Listas**, **Tuplas**, **Conjuntos (Sets)** y **Diccionarios**.
3. Comprender los conceptos de **Mutabilidad vs Inmutabilidad** y **Complejidad Algorítmica ($O(1)$ vs $O(N)$)** en accesos y búsquedas.
4. Aplicar lectura y escritura eficientes de archivos planos en Python mediante gestión contextual (`with`).

---

## Teoría Explicada

### 1. Estructuras de Datos Fundamentales en Python

#### A. Cadenas de Texto (Strings - Inmutables)
* Las cadenas en Python son secuencias inmutables de caracteres Unicode.
* **Métodos clave:** `.strip()`, `.upper()`, `.lower()`, `.split()`, `.join()`, `.replace()`, `.startswith()`, `.endswith()`.
* **Slicing:** `texto[inicio:fin:paso]`

```python
cadena = "  30712223338;Tech Solutions S.A.;Corporate  "
datos = cadena.strip().split(";")
# datos = ['30712223338', 'Tech Solutions S.A.', 'Corporate']
cuit_limpio = datos[0].replace("-", "")
```

#### B. Listas (`list` - Mutables y Ordenadas)
* Colección ordenada de elementos heterogéneos.
* **Búsqueda:** $O(N)$ en el peor de los casos (`x in lista`).
* **Métodos clave:** `.append(x)`, `.extend(iterable)`, `.insert(i, x)`, `.pop(i)`, `.remove(x)`, `.sort()`.

#### C. Tuplas (`tuple` - Inmutables y Ordenadas)
* Colección ordenada inmutable. Ideal para registros heterogéneos de estructura fija o como claves de diccionarios.
* **Desempaquetado de tuplas (Tuple Unpacking):** `cliente_id, nombre, saldo = (101, "Carlos", 50000.0)`

#### D. Conjuntos (`set` - Mutables y No Ordenados de Elementos Únicos)
* Colección no ordenada de elementos únicos e inmutables (hashable).
* **Búsqueda:** $O(1)$ en promedio (`x in mi_set`), ideal para deduplicación y filtros de pertenencia de alta velocidad.
* **Operaciones de conjuntos:** Unión (`|`), Intersección (`&`), Diferencia (`-`), Diferencia Simétrica (`^`).

```python
clientes_caja_ahorro = {1001, 1002, 1003, 1005}
clientes_tarjeta_credito = {1002, 1003, 1006}

# Clientes que tienen AMBOS productos (Intersección)
clientes_cross_sell = clientes_caja_ahorro & clientes_tarjeta_credito  # {1002, 1003}

# Clientes con caja de ahorro PERO SIN tarjeta (Diferencia)
solo_ahorro = clientes_caja_ahorro - clientes_tarjeta_credito  # {1001, 1005}
```

#### E. Diccionarios (`dict` - Mutables de Clave-Valor)
* Estructura asociativa de pares `clave: valor`. Búsqueda por clave en $O(1)$.
* **Métodos clave:** `.get(clave, default)`, `.items()`, `.keys()`, `.values()`, `.setdefault()`.

```python
cliente = {
    "cuit": "20358889991",
    "nombre": "María González",
    "score_crediticio": 780
}

# Acceso seguro con default (evita KeyError)
limite = cliente.get("limite_preaprobado", 0.0)
```

---

### 2. Operaciones con Archivos (I/O) en Python

El manejo de archivos debe realizarse mediante administradores de contexto (`with`), asegurando la liberación automática del descriptor de archivo (file handle) incluso ante excepciones.

#### Patrones de Lectura y Escritura
```python
# Lectura línea por línea (Eficiente en Memoria para archivos grandes)
transacciones_validas = []

with open("transacciones.txt", mode="r", encoding="utf-8") as file:
    for linea in file:
        linea_limpia = linea.strip()
        if linea_limpia and not linea_limpia.startswith("#"):
            campos = linea_limpia.split(",")
            transacciones_validas.append(campos)

# Escritura de resultados
with open("reporte_salida.csv", mode="w", encoding="utf-8") as file_out:
    file_out.write("cliente_id,monto\n")
    for item in transacciones_validas:
        file_out.write(f"{item[0]},{item[1]}\n")
```

---

### Comparativa de Rendimiento y Uso de Estructuras

| Estructura | Ordenada | Mutable | Duplicados | Búsqueda `in` | Casos de Uso Recomendados |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`list`** | Sí | Sí | Sí | $O(N)$ | Secuencias de elementos donde el orden importa. |
| **`tuple`** | Sí | No | Sí | $O(N)$ | Registros inmutables, claves compuestas en diccionarios. |
| **`set`** | No | Sí | No | **$O(1)$** | Filtrado de duplicados, validaciones de membresía rápida. |
| **`dict`** | Sí (Python 3.7+) | Sí | Claves únicas | **$O(1)$** (por clave) | Tablas de búsqueda, mapas de propiedades, JSON. |
