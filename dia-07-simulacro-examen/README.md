# Día 7: Repaso & Test - Simulacro de Examen & Repaso Intensivo

Bienvenido al Día 7 del Plan Intensivo de Preparación Acelerada para la Evaluación Técnica (Itaú).

---

## Objetivos del Día
1. Repasar de forma integral la teoría y sintaxis clave de **SQL/T-SQL**, **Python Base**, **Programación Funcional**, **Pandas/NumPy** y **Data Preparation**.
2. Revisar la Checklist de las 4 Reglas de Oro indispensables para superar la evaluación con $\ge 70\%$ de aprobación.
3. Ejecutar el Simulacro de Examen Integrado Cronometrado de 20 preguntas desafiantes (50% SQL / 50% Python & Data Prep).
4. Resolver el Ejercicio Práctico Integrador de extremo a extremo que combina SQL, Pandas y Data Preparation.

---

## Checklist de las 4 Reglas de Oro para la Evaluación (≥ 70% Aprobación)

Antes de iniciar la prueba oficial o el simulacro, repasa mentalmente estas 4 reglas fundamentales:

| Área | Regla de Oro | Trampa Típica a Evitar |
| :--- | :--- | :--- |
| **SQL - Nulos** | Usa `IS NULL`, `IS NOT NULL` o `COALESCE()`. | Comparar `col = NULL` o `col <> NULL` siempre devuelve `UNKNOWN` (falso). |
| **SQL - Joins** | Para mantener un `LEFT JOIN`, los filtros sobre la tabla derecha deben ir **dentro del `ON`**. | Poner un filtro de la tabla derecha en la cláusula `WHERE` convierte el `LEFT JOIN` en un `INNER JOIN`. |
| **Python - Sintaxis Ágil** | Domina expresiones de una sola línea: `[x**2 for x in lista if x > 0]` y `list(map(lambda x: ..., datos))`. | Diferenciar la posición de `if/else`: `[A if cond else B for x in list]` vs `[A for x in list if cond]`. |
| **Pandas & Data Prep** | Usa siempre métodos orientados a DataFrames (`fillna`, `dropna`, `apply`, `groupby`, `merge`). | Evitar el uso de bucles `for` (`for row in df.iterrows()`) para recorrer DataFrames. |

---

## Recomendaciones de Manejo del Tiempo en el Examen
* **Tiempo Total Estimado:** 60 a 90 minutos.
* **Sección 1 (SQL Core & Avanzado):** 30 minutos. Revisar detalladamente los `JOIN`s y los alias en `GROUP BY` / `HAVING`.
* **Sección 2 (Python Base & Funcional):** 20 minutos. Atención al orden de ejecución y late binding en lambdas.
* **Sección 3 (Pandas & Data Prep):** 30 minutos. Prestar especial atención a la diferencia entre `.loc` e `.iloc` y el uso de `pd.cut` vs `pd.qcut`.

---

## Archivos del Día 7
* **`README.md`**: (Este archivo) Guía de repaso y reglas clave.
* **`test_evaluacion.md`**: Simulacro de Examen Integrado de 20 Preguntas Desafiantes.
* **`ejercicio_integrador.py`**: Solución y script del desafío técnico práctico integrador.
