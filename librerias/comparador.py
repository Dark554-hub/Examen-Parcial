"""
Librería de Comparación de Escenarios y Benchmarks Empíricos (Requerimiento 6 del Examen Parcial).
Proporciona:
1. La tabla oficial de recomendaciones técnicas para los 5 escenarios del examen:
   - Datos pequeños
   - Datos masivos
   - Archivos externos
   - Datos parcialmente ordenados
   - Búsquedas frecuentes
2. Un motor de benchmark empírico que ejecuta todos los algoritmos internos y externos
   sobre los datasets de 1,000 y 5,000 registros para medir tiempos reales, comparaciones
   e intercambios.
"""

from librerias.ordenamientos_internos import CATALOGO_INTERNOS
from librerias.ordenamientos_externos import CATALOGO_EXTERNOS
from librerias.busquedas import busqueda_secuencial, busqueda_binaria, TablaHashTransacciones


TABLA_COMPARACION_ESCENARIOS = [
    {
        "escenario": "Datos pequeños (n < 100)",
        "algoritmo_recomendado": "Inserción (Insertion Sort)",
        "complejidad": "O(n²) promedio / O(n) mejor caso",
        "justificacion": (
            "Presenta sobrecarga mínima de memoria O(1) sin llamadas recursivas, alta localidad de caché "
            "y supera a algoritmos complejos en arreglos cortos."
        ),
    },
    {
        "escenario": "Datos masivos en memoria (n >= 5,000)",
        "algoritmo_recomendado": "Quicksort / Radix Sort (LSD) / Heapsort",
        "complejidad": "O(n log n) / O(d · n)",
        "justificacion": (
            "Quicksort divide el problema logarítmicamente con excelente velocidad práctica; "
            "Radix Sort procesa enteros en tiempo lineal O(d·n) sin comparaciones; "
            "Heapsort garantiza O(n log n) en el peor caso con memoria O(1)."
        ),
    },
    {
        "escenario": "Archivos externos (Volumen mayor a RAM / Disco)",
        "algoritmo_recomendado": "Mezcla Equilibrada (Natural Merge) / Mezcla Directa",
        "complejidad": "O(n log n) en pasadas secuenciales sobre archivos F1 y F2",
        "justificacion": (
            "Diseñados para acceso secuencial en almacenamiento secundario mediante particiones "
            "y fusiones de corridas en archivos auxiliares (F1, F2) sin cargar todo en RAM."
        ),
    },
    {
        "escenario": "Datos parcialmente ordenados",
        "algoritmo_recomendado": "Inserción (Interno) / Mezcla Equilibrada (Externo)",
        "complejidad": "O(n) adaptativo cuando existen pocas inversiones o pocos tramos",
        "justificacion": (
            "Inserción solo desplaza los elementos fuera de orden en O(n + k); "
            "Mezcla Equilibrada detecta las corridas naturales existentes reduciendo drásticamente las pasadas."
        ),
    },
    {
        "escenario": "Búsquedas frecuentes",
        "algoritmo_recomendado": "Tabla Hash (O(1)) / Búsqueda Binaria sobre datos ordenados (O(log n))",
        "complejidad": "O(1) promedio en Hash / O(log n) en Búsqueda Binaria",
        "justificacion": (
            "Para consultas exactas repetitivas, indexar en una Tabla Hash resuelve cada búsqueda en O(1); "
            "si también se requieren consultas por rango u orden, ordenar una vez con Quicksort/Radix y "
            "aplicar Búsqueda Binaria toma solo ~13 comparaciones en 5,000 registros."
        ),
    },
]


def ejecutar_benchmark_ordenamientos(lista_datos, ascendente=True, incluir_cuadraticos=True):
    """
    Ejecuta todos los algoritmos de ordenamiento internos y externos sobre la misma lista
    de entrada y devuelve una lista de diccionarios con las métricas comparativas.
    """
    resultados = []

    for clave, (_, funcion) in CATALOGO_INTERNOS.items():
        if not incluir_cuadraticos and clave in ("burbuja", "seleccion", "insercion") and len(lista_datos) > 10000:
            continue
        res = funcion(lista_datos, ascendente=ascendente, retornar_metricas=True)
        resultados.append({
            "clave": clave,
            "algoritmo": res["algoritmo"],
            "categoria": res["tipo"],
            "complejidad": res["complejidad"],
            "tiempo_ms": round(res["tiempo_ms"], 4),
            "tiempo_seg": round(res["tiempo_seg"], 6),
            "comparaciones": res["comparaciones"],
            "intercambios": res["intercambios"],
            "verificado": res["verificado"],
        })

    for clave, (_, funcion) in CATALOGO_EXTERNOS.items():
        res = funcion(lista_datos, ascendente=ascendente, retornar_metricas=True)
        resultados.append({
            "clave": clave,
            "algoritmo": res["algoritmo"],
            "categoria": res["tipo"],
            "complejidad": res["complejidad"],
            "tiempo_ms": round(res["tiempo_ms"], 4),
            "tiempo_seg": round(res["tiempo_seg"], 6),
            "comparaciones": res["comparaciones"],
            "intercambios": res["intercambios"],
            "verificado": res["verificado"],
        })

    return resultados


def ejecutar_benchmark_busquedas(lista_ordenada, objetivo, ascendente=True):
    """Compara empíricamente Búsqueda Secuencial, Búsqueda Binaria y Búsqueda Hash."""
    cap = 2003 if len(lista_ordenada) <= 2000 else 10007
    tabla = TablaHashTransacciones(capacidad=cap).construir_desde_lista(lista_ordenada)

    res_sec = busqueda_secuencial(lista_ordenada, objetivo)
    res_bin = busqueda_binaria(lista_ordenada, objetivo, ascendente=ascendente)
    res_hash = tabla.buscar(objetivo)

    return [res_sec, res_bin, res_hash]
