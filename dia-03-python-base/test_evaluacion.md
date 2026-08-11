# Test de Preguntas Desafiantes - Día 3: Python Base

Evaluación práctica sobre Estructuras de Datos, Mutabilidad, Rendimiento y Manejo I/O en Python.

---

### Pregunta 1: Mutabilidad y Modificación Imprevista
Analiza el siguiente fragmento de código Python:

```python
registro_a = (101, "Carlos", [100.0, 200.0])
registro_a[2].append(300.0)
print(registro_a)
```

¿Qué sucede al ejecutar este código?

- A) Lanza un `TypeError` porque las tuplas son inmutables y no permiten modificar ninguno de sus elementos.
- B) Imprime `(101, 'Carlos', [100.0, 200.0, 300.0])` con éxito.
- C) Lanza un `AttributeError` indicando que `tuple` no tiene el método `.append()`.
- D) Se crea una tupla idéntica pero nueva en una dirección de memoria diferente.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Una tupla es inmutable en cuanto a la **referencia** de sus elementos (la tupla contiene siempre la misma referencia a la lista en el índice 2). Sin embargo, el objeto guardado en el índice 2 es una `list`, la cual **sí es mutable**. Llamar a `.append()` modifica la lista mutable in situ sin alterar la referencia que posee la tupla.
</details>

---

### Pregunta 2: Complejidad de Búsqueda y Optimización
Tienes una lista `bloqueados_list` con 1,000,000 de CUITs de personas con restricciones bancarias. Cada segundo debes verificar si los CUITs de 50,000 transacciones entrantes están en la lista de bloqueados.

¿Qué cambio estructural mejoraría drásticamente el tiempo de ejecución?

- A) Ordenar la lista con `bloqueados_list.sort()` antes de cada iteración.
- B) Convertir `bloqueados_list` a un `set` mediante `bloqueados_set = set(bloqueados_list)` y realizar la búsqueda con `cuit in bloqueados_set`.
- C) Convertir `bloqueados_list` a una tupla `bloqueados_tuple = tuple(bloqueados_list)`.
- D) Usar un bloque `try...except KeyError` recorriendo la lista con un bucle `for`.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** Buscar en una lista `x in lista` tiene complejidad $O(N)$. Para 50,000 verificaciones sobre 1,000,000 de elementos se realizan en el peor caso $50,000 \times 1,000,000 = 50,000,000,000$ comparaciones. En un `set` (basado en Hash Table), la búsqueda `x in conjunto` se realiza en tiempo constante $O(1)$, reduciendo drásticamente el tiempo total de ejecución a solo 50,000 búsquedas Hash.
</details>

---

### Pregunta 3: Acceso Seguro a Diccionarios
¿Cuál es la diferencia entre `diccionario['clave']` y `diccionario.get('clave', 0)` cuando la clave `'clave'` no existe dentro del diccionario?

- A) `diccionario['clave']` devuelve `None`, mientras que `diccionario.get('clave', 0)` devuelve `0`.
- B) `diccionario['clave']` lanza un error `KeyError`, mientras que `diccionario.get('clave', 0)` captura la ausencia y devuelve `0` de forma segura.
- C) `diccionario.get('clave', 0)` inserta la clave con valor `0` en el diccionario permanentemente.
- D) Ambos métodos devuelven exactamente lo mismo sin lanzar excepciones.

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** El acceso directo por corchetes `d[k]` genera un fallo catastrófico (`KeyError`) si la clave no existe. El método `.get(k, default)` busca la clave de forma defensiva y retorna el parámetro por defecto (o `None` si se omite) sin interrumpir la ejecución ni insertar datos falsos.
</details>

---

### Pregunta 4: Manejo de Contexto I/O
¿Por qué es altamente recomendado usar la sintaxis `with open(...) as f:` al trabajar con archivos planos en Python?

- A) Porque acelera la lectura del archivo comprimiendo los datos en RAM.
- B) Porque garantiza que el archivo se cierre automáticamente al salir del bloque, incluso si ocurre una excepción no controlada.
- C) Porque convierte automáticamente el contenido del archivo a un objeto Pandas DataFrame.
- D) Porque permite modificar el archivo en modo de solo lectura (`'r'`).

<details>
<summary><b> Ver Respuesta y Explicación</b></summary>

**Respuesta Correcta: B**

**Explicación:** `with` implementa el protocolo de Context Manager (`__enter__` y `__exit__`). Al concluir el bloque (o al capturar un error dentro de él), llama automáticamente a `f.close()`, evitando fugas de descriptores de archivo (file handle leaks) e inconsistencias en disco.
</details>
