"""
Librería de Algoritmos de Ordenamiento Interno (En Memoria RAM).
Reutilización y adaptación de librerías propias desarrolladas en ADA1 y ADA2:
- ADA1: Burbuja, Inserción, Selección
- ADA2: ShellSort, Quicksort, Heapsort, Radix Sort

RESTRICCIÓN ESTRICTA:
Prohibido el uso de .sort(), sorted() o cualquier biblioteca automática de ordenamiento.
Todos los algoritmos soportan ordenamiento Ascendente y Descendente y devuelven
métricas detalladas de rendimiento (comparaciones, intercambios/movimientos, tiempo).
"""

import time


def verificar_orden(lista, ascendente=True):
    """Verifica manualmente en O(n) si una lista está correctamente ordenada."""
    n = len(lista)
    if n <= 1:
        return True
    if ascendente:
        for i in range(n - 1):
            if lista[i] > lista[i + 1]:
                return False
    else:
        for i in range(n - 1):
            if lista[i] < lista[i + 1]:
                return False
    return True


def invertir_lista_manual(lista):
    """Invierte una lista manualmente in-place sin funciones nativas de ordenamiento."""
    n = len(lista)
    mitad = n // 2
    for i in range(mitad):
        lista[i], lista[n - 1 - i] = lista[n - 1 - i], lista[i]
    return lista


# =====================================================================
# 1. ORDENAMIENTO BURBUJA (BUBBLE SORT) - Origen: ADA1/burbuja.py
# =====================================================================
def ordenamiento_burbuja(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista de números enteros mediante el método de Burbuja con bandera de optimización.
    Complejidad: Mejor caso O(n), Caso promedio y peor caso O(n^2). Memoria: O(1) auxiliar.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            comparaciones += 1
            condicion = (datos[j] > datos[j + 1]) if ascendente else (datos[j] < datos[j + 1])
            if condicion:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                hubo_intercambio = True
                intercambios += 1
        if not hubo_intercambio:
            break

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Burbuja (Bubble Sort)",
            "tipo": "Interno",
            "complejidad": "O(n²)",
            "comparaciones": comparaciones,
            "intercambios": intercambios,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 2. ORDENAMIENTO POR INSERCIÓN (INSERTION SORT) - Origen: ADA1/insercion.py
# =====================================================================
def ordenamiento_insercion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista de números enteros mediante Inserción Directa.
    Ideal para datos pequeños o parcialmente ordenados.
    Complejidad: Mejor caso O(n), Caso promedio y peor caso O(n^2). Memoria: O(1) auxiliar.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    comparaciones = 0
    desplazamientos = 0

    for i in range(1, n):
        actual = datos[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            condicion = (datos[j] > actual) if ascendente else (datos[j] < actual)
            if condicion:
                datos[j + 1] = datos[j]
                j -= 1
                desplazamientos += 1
            else:
                break
        datos[j + 1] = actual

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Inserción (Insertion Sort)",
            "tipo": "Interno",
            "complejidad": "O(n²) / O(n) adaptativo",
            "comparaciones": comparaciones,
            "intercambios": desplazamientos,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 3. ORDENAMIENTO POR SELECCIÓN (SELECTION SORT) - Origen: ADA1/seleccion.py
# =====================================================================
def ordenamiento_seleccion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista seleccionando iterativamente el elemento extremo (mínimo o máximo).
    Complejidad: O(n^2) en todos los casos. Memoria: O(1) auxiliar.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):
        idx_extremo = i
        for j in range(i + 1, n):
            comparaciones += 1
            condicion = (datos[j] < datos[idx_extremo]) if ascendente else (datos[j] > datos[idx_extremo])
            if condicion:
                idx_extremo = j
        if idx_extremo != i:
            datos[i], datos[idx_extremo] = datos[idx_extremo], datos[i]
            intercambios += 1

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Selección (Selection Sort)",
            "tipo": "Interno",
            "complejidad": "O(n²)",
            "comparaciones": comparaciones,
            "intercambios": intercambios,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 4. ORDENAMIENTO SHELLSORT - Origen: ADA2/shellsort.py
# =====================================================================
def shell_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista utilizando incrementos decrecientes (ShellSort).
    Complejidad: O(n log^2 n) dependiendo de la brecha. Memoria: O(1) auxiliar.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    salto = n // 2
    comparaciones = 0
    desplazamientos = 0

    while salto > 0:
        for i in range(salto, n):
            temp = datos[i]
            j = i
            while j >= salto:
                comparaciones += 1
                condicion = (datos[j - salto] > temp) if ascendente else (datos[j - salto] < temp)
                if condicion:
                    datos[j] = datos[j - salto]
                    j -= salto
                    desplazamientos += 1
                else:
                    break
            datos[j] = temp
        salto //= 2

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "ShellSort",
            "tipo": "Interno",
            "complejidad": "O(n^1.25 ~ n log² n)",
            "comparaciones": comparaciones,
            "intercambios": desplazamientos,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 5. ORDENAMIENTO QUICKSORT - Origen: ADA2/quicksort.py
# =====================================================================
def quicksort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista mediante Divide y Vencerás (Quicksort con partición tripartita).
    Complejidad: Promedio O(n log n), Peor caso O(n^2).
    """
    t0 = time.perf_counter()
    metricas = {"comparaciones": 0, "movimientos": 0}

    def _qs(sublista):
        if len(sublista) <= 1:
            return sublista

        pivote = sublista[len(sublista) // 2]
        menores = []
        iguales = []
        mayores = []

        for x in sublista:
            metricas["comparaciones"] += 1
            metricas["movimientos"] += 1
            if x < pivote:
                menores.append(x)
            elif x > pivote:
                mayores.append(x)
            else:
                iguales.append(x)

        if ascendente:
            return _qs(menores) + iguales + _qs(mayores)
        else:
            return _qs(mayores) + iguales + _qs(menores)

    datos = _qs(lista[:])
    t1 = time.perf_counter()

    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Quicksort",
            "tipo": "Interno",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 6. ORDENAMIENTO HEAPSORT - Origen: ADA2/heapsort.py
# =====================================================================
def _heapify(lista, n, i, ascendente, metricas):
    extremo = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n:
        metricas["comparaciones"] += 1
        # Para orden ascendente usamos Max-Heap; para descendente usamos Min-Heap
        cond_izq = (lista[izq] > lista[extremo]) if ascendente else (lista[izq] < lista[extremo])
        if cond_izq:
            extremo = izq

    if der < n:
        metricas["comparaciones"] += 1
        cond_der = (lista[der] > lista[extremo]) if ascendente else (lista[der] < lista[extremo])
        if cond_der:
            extremo = der

    if extremo != i:
        lista[i], lista[extremo] = lista[extremo], lista[i]
        metricas["intercambios"] += 1
        _heapify(lista, n, extremo, ascendente, metricas)


def heapsort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una lista utilizando un montículo binario (Max-Heap / Min-Heap).
    Complejidad garantizada: O(n log n) en todos los casos. Memoria: O(1) auxiliar.
    """
    t0 = time.perf_counter()
    datos = lista[:]
    n = len(datos)
    metricas = {"comparaciones": 0, "intercambios": 0}

    for i in range(n // 2 - 1, -1, -1):
        _heapify(datos, n, i, ascendente, metricas)

    for i in range(n - 1, 0, -1):
        datos[0], datos[i] = datos[i], datos[0]
        metricas["intercambios"] += 1
        _heapify(datos, i, 0, ascendente, metricas)

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Heapsort",
            "tipo": "Interno",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["intercambios"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


# =====================================================================
# 7. ORDENAMIENTO RADIX SORT (LSD) - Origen: ADA2/radix.py
# =====================================================================
def _maximo_manual(lista):
    """Obtiene el valor máximo manualmente sin funciones mágicas."""
    m = lista[0]
    for x in lista[1:]:
        if x > m:
            m = x
    return m


def _counting_por_digito(lista, exp, metricas):
    n = len(lista)
    salida = [0] * n
    conteo = [0] * 10

    for num in lista:
        indice = (num // exp) % 10
        conteo[indice] += 1
        metricas["movimientos"] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    for i in range(n - 1, -1, -1):
        indice = (lista[i] // exp) % 10
        salida[conteo[indice] - 1] = lista[i]
        conteo[indice] -= 1
        metricas["movimientos"] += 1

    for i in range(n):
        lista[i] = salida[i]


def radix_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena números enteros (positivos y negativos) dígito por dígito (Radix Sort LSD).
    Complejidad: O(d * (n + b)), no comparativo.
    """
    t0 = time.perf_counter()
    if not lista:
        datos = []
        metricas = {"comparaciones": 0, "movimientos": 0}
    else:
        metricas = {"comparaciones": 0, "movimientos": 0}
        negativos = [-x for x in lista if x < 0]
        positivos = [x for x in lista if x >= 0]

        if positivos:
            max_pos = _maximo_manual(positivos)
            exp = 1
            while max_pos // exp > 0:
                _counting_por_digito(positivos, exp, metricas)
                exp *= 10

        if negativos:
            max_neg = _maximo_manual(negativos)
            exp = 1
            while max_neg // exp > 0:
                _counting_por_digito(negativos, exp, metricas)
                exp *= 10
            invertir_lista_manual(negativos)
            negativos = [-x for x in negativos]

        datos = negativos + positivos
        if not ascendente:
            invertir_lista_manual(datos)

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos,
            "algoritmo": "Radix Sort (LSD)",
            "tipo": "Interno (No Comparativo)",
            "complejidad": "O(d · n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos, ascendente),
        }
    return datos


CATALOGO_INTERNOS = {
    "burbuja": ("Burbuja (Bubble Sort)", ordenamiento_burbuja),
    "insercion": ("Inserción (Insertion Sort)", ordenamiento_insercion),
    "seleccion": ("Selección (Selection Sort)", ordenamiento_seleccion),
    "shellsort": ("ShellSort", shell_sort),
    "quicksort": ("Quicksort", quicksort),
    "heapsort": ("Heapsort", heapsort),
    "radix": ("Radix Sort (LSD)", radix_sort),
}
