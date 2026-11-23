"""
Librería de Algoritmos de Ordenamiento Externo (Procesamiento Basado en Archivos Auxiliares y Corridas).
Reutilización y adaptación de librerías propias desarrolladas en MetOrdena:
- MetOrdena/intercalacion.py -> Intercalación de archivos/listas
- MetOrdena/mezcla_directa.py -> Mezcla Directa (Direct Merge Sort con bloques 1, 2, 4, 8...)
- MetOrdena/mezcla_equilibrada.py -> Mezcla Equilibrada / Natural (Natural Merge Sort por corridas)

Incluye además modo de persistencia en archivos auxiliares F1.txt y F2.txt en disco para
demostrar el procesamiento externo real de grandes volúmenes de transacciones financieras.

RESTRICCIÓN ESTRICTA:
Prohibido el uso de .sort(), sorted() o cualquier biblioteca automática de ordenamiento.
"""

import os
import time
from librerias.ordenamientos_internos import verificar_orden


# =====================================================================
# 1. INTERCALACIÓN (MERGE DE ARCHIVOS / CORRIDAS) - Origen: MetOrdena/intercalacion.py
# =====================================================================
def intercalar_listas(lista_a, lista_b, ascendente=True, metricas=None):
    """Intercala dos listas previamente ordenadas en una sola lista ordenada."""
    resultado = []
    i = 0
    j = 0
    na = len(lista_a)
    nb = len(lista_b)

    while i < na and j < nb:
        if metricas is not None:
            metricas["comparaciones"] += 1
            metricas["movimientos"] += 1
        condicion = (lista_a[i] <= lista_b[j]) if ascendente else (lista_a[i] >= lista_b[j])
        if condicion:
            resultado.append(lista_a[i])
            i += 1
        else:
            resultado.append(lista_b[j])
            j += 1

    while i < na:
        resultado.append(lista_a[i])
        i += 1
        if metricas is not None:
            metricas["movimientos"] += 1

    while j < nb:
        resultado.append(lista_b[j])
        j += 1
        if metricas is not None:
            metricas["movimientos"] += 1

    return resultado


def ordenamiento_intercalacion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una colección dividiéndola recursivamente en corridas e intercalándolas
    mediante la rutina propia `intercalar_listas` de MetOrdena/intercalacion.py.
    Complejidad: O(n log n) garantizado.
    """
    t0 = time.perf_counter()
    metricas = {"comparaciones": 0, "movimientos": 0, "pasadas": 0}

    def _dividir_e_intercalar(sublista):
        if len(sublista) <= 1:
            return sublista
        mitad = len(sublista) // 2
        izq = _dividir_e_intercalar(sublista[:mitad])
        der = _dividir_e_intercalar(sublista[mitad:])
        metricas["pasadas"] += 1
        return intercalar_listas(izq, der, ascendente, metricas)

    datos = _dividir_e_intercalar(lista[:])
    t1 = time.perf_counter()

    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Intercalación (External Merge)",
            "tipo": "Externo",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": metricas["pasadas"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 2. MEZCLA DIRECTA (DIRECT MERGE SORT) - Origen: MetOrdena/mezcla_directa.py
# =====================================================================
def _particionar_directa(datos, tam_bloque):
    """Divide la lista en dos archivos/listas auxiliares F1 y F2 alternando bloques de tamaño fijo."""
    f1 = []
    f2 = []
    usar_f1 = True

    for i in range(0, len(datos), tam_bloque):
        bloque = datos[i : i + tam_bloque]
        if usar_f1:
            f1.append(bloque)
        else:
            f2.append(bloque)
        usar_f1 = not usar_f1

    return f1, f2


def _guardar_auxiliares_disco(f1, f2, dir_temp, etiqueta):
    """Persiste los bloques de los archivos auxiliares F1 y F2 en disco para auditoría de ordenamiento externo."""
    os.makedirs(dir_temp, exist_ok=True)
    ruta_f1 = os.path.join(dir_temp, f"F1_{etiqueta}.txt")
    ruta_f2 = os.path.join(dir_temp, f"F2_{etiqueta}.txt")
    with open(ruta_f1, "w", encoding="utf-8") as arch1:
        for idx, b in enumerate(f1):
            arch1.write(f"Tramo_{idx+1}: " + ",".join(str(x) for x in b[:25]) + ("..." if len(b) > 25 else "") + "\n")
    with open(ruta_f2, "w", encoding="utf-8") as arch2:
        for idx, b in enumerate(f2):
            arch2.write(f"Tramo_{idx+1}: " + ",".join(str(x) for x in b[:25]) + ("..." if len(b) > 25 else "") + "\n")
    return ruta_f1, ruta_f2


def mezcla_directa(lista, ascendente=True, retornar_metricas=False, dir_auxiliar=None):
    """
    Ordena una lista mediante el algoritmo de Mezcla Directa (bloques de longitud 1, 2, 4, 8, 16...).
    Reutiliza la arquitectura de archivos auxiliares F1 y F2 de MetOrdena/mezcla_directa.py.
    Complejidad: O(n log n) en exactamente ceil(log2(n)) pasadas externas.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    tam_bloque = 1
    pasada = 0
    metricas = {"comparaciones": 0, "movimientos": 0}
    archivos_aux = []

    while tam_bloque < n:
        pasada += 1
        f1, f2 = _particionar_directa(datos, tam_bloque)

        if dir_auxiliar and pasada in (1, 2):
            r1, r2 = _guardar_auxiliares_disco(f1, f2, dir_auxiliar, f"directa_pasada_{pasada}")
            archivos_aux.extend([r1, r2])

        datos = []
        max_bloques = len(f1) if len(f1) >= len(f2) else len(f2)
        for k in range(max_bloques):
            b1 = f1[k] if k < len(f1) else []
            b2 = f2[k] if k < len(f2) else []
            datos.extend(intercalar_listas(b1, b2, ascendente, metricas))

        tam_bloque *= 2

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Mezcla Directa (Direct Merge Sort)",
            "tipo": "Externo (Auxiliares F1 y F2)",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": pasada,
            "archivos_auxiliares": archivos_aux,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 3. MEZCLA EQUILIBRADA / NATURAL - Origen: MetOrdena/mezcla_equilibrada.py
# =====================================================================
def obtener_tramos_naturales(datos, ascendente=True, metricas=None):
    """Detecta subsecuencias contiguas (corridas) que ya están ordenadas naturalmente."""
    if not datos:
        return []

    tramos = []
    actual = [datos[0]]
    for x in datos[1:]:
        if metricas is not None:
            metricas["comparaciones"] += 1
        condicion = (x >= actual[-1]) if ascendente else (x <= actual[-1])
        if condicion:
            actual.append(x)
        else:
            tramos.append(actual)
            actual = [x]
    tramos.append(actual)
    return tramos


def mezcla_equilibrada(lista, ascendente=True, retornar_metricas=False, dir_auxiliar=None):
    """
    Ordena una lista usando el método de Mezcla Equilibrada (Natural Merge Sort).
    Aprovecha tramos (corridas) ya ordenados naturalmente en los datos y los distribuye
    entre dos archivos auxiliares F1 y F2 hasta lograr un único tramo ordenado.
    Complejidad: O(n log n) en caso general, O(n) si ya está ordenado.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    iteracion = 0
    metricas = {"comparaciones": 0, "movimientos": 0}
    tramos_iniciales = 0
    archivos_aux = []

    while True:
        tramos = obtener_tramos_naturales(datos, ascendente, metricas)
        if iteracion == 0:
            tramos_iniciales = len(tramos)
        if len(tramos) <= 1:
            break

        iteracion += 1
        f1 = tramos[0::2]
        f2 = tramos[1::2]

        if dir_auxiliar and iteracion in (1, 2):
            r1, r2 = _guardar_auxiliares_disco(f1, f2, dir_auxiliar, f"equilibrada_iter_{iteracion}")
            archivos_aux.extend([r1, r2])

        datos = []
        max_tramos = len(f1) if len(f1) >= len(f2) else len(f2)
        for k in range(max_tramos):
            t1_tramo = f1[k] if k < len(f1) else []
            t2_tramo = f2[k] if k < len(f2) else []
            datos.extend(intercalar_listas(t1_tramo, t2_tramo, ascendente, metricas))

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Mezcla Equilibrada (Natural Merge)",
            "tipo": "Externo (Corridas Naturales F1/F2)",
            "complejidad": "O(n log n) / O(n) adaptativo",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": iteracion,
            "tramos_iniciales": tramos_iniciales,
            "archivos_auxiliares": archivos_aux,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


CATALOGO_EXTERNOS = {
    "intercalacion": ("Intercalación (External Merge)", ordenamiento_intercalacion),
    "mezcla_directa": ("Mezcla Directa (Direct Merge Sort)", mezcla_directa),
    "mezcla_equilibrada": ("Mezcla Equilibrada (Natural Merge)", mezcla_equilibrada),
}
