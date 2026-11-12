# Respuestas conceptuales - Ventas

## 1. ¿Por qué usar `_loaded_at` y no `fecha_venta` para este control?

Porque son dos fechas distintas. `fecha_venta` dice cuándo ocurrió la venta en el negocio; `_loaded_at` dice cuándo
llegó esa fila al sistema. El control de freshness pregunta si la carga es reciente, así que necesita la segunda.
Una venta antigua puede cargarse hoy (una corrección o una carga atrasada), y una carga que se detuvo puede dejar
la tabla sin filas nuevas aunque el negocio siga vendiendo.

En este ejercicio se ve con claridad: las seis ventas tienen `fecha_venta` entre el 2026-01-10 y el 2026-01-12, es decir,
meses antes de la ejecución, y aun así en el escenario `actualizada` freshness pasó y `construir_resumen` corrió
(`_loaded_at` de hace 2 horas). Con `fecha_venta` como campo de control, la fuente habría aparecido como
desactualizada en todos los escenarios y el control no habría distinguido entre cargas buenas y malas. Lo que
cambió entre las ejecuciones fue solo `_loaded_at` (2 h, 18 h, 30 h) y por eso freshness pasó, avisó y falló.

Un límite: este control comprueba la carga más reciente, pero no demuestra que hayan llegado todas las ventas esperadas.

## 2. ¿Por qué las pruebas de integridad no garantizan actualidad?

Porque verifican la forma y la validez de las filas que ya están en la tabla (`unique`, `not_null`, cantidades y
precios válidos, coincidencia con el resultado esperado), y no preguntan cuándo se cargaron. Datos viejos pueden ser
perfectamente únicos, completos y válidos.

La evidencia lo muestra: los escenarios usan los mismos datos de negocio y solo cambian las marcas de carga. En la
ejecución de `advertencia` (carga de hace 18 h), `dbt build` terminó con todas las pruebas en PASS, igual que en
`actualizada`; solo `dbt source freshness` distingue los escenarios. En `desactualizada`, el resumen y sus pruebas
habrían sido igual de "correctos", y por eso fue necesario que freshness bloqueara el build (`construir_resumen` en
`upstream_failed`, sin ningún intento ni marca `INICIO dbt` en esa ejecución) en lugar de depender de las pruebas.
Además, `dbt build` no ejecuta freshness automáticamente, así que un build exitoso no dice nada sobre la actualidad.