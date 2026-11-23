"""
Librería de Algoritmos de Ordenamiento Interno (En Memoria RAM).
Reutilización obligatoria de la librería propia `MyLinkedList.py` (desarrollada en `estructura/MyLinkedList.py`)
y de los algoritmos propios de `ADA1` y `ADA2`:
- Estructura de datos obligatoria: `MyLinkedList` y `Node` (de `MyLinkedList.py`)
- ADA1: Burbuja, Inserción, Selección
- ADA2: ShellSort, Quicksort, Heapsort, Radix Sort

RESTRICCIÓN ESTRICTA:
Prohibido el uso de .sort(), sorted() o cualquier biblioteca automática de ordenamiento.
Toda la entrada y salida de datos utiliza `MyLinkedList`.
"""

import time
from MyLinkedList import MyLinkedList


def asegurar_linked_list(coleccion):
    """Garantiza que cualquier colección de entrada sea una instancia de MyLinkedList."""
    if isinstance(coleccion, MyLinkedList):
        return coleccion.copy()
    return MyLinkedList(coleccion)


def verificar_orden(lista_enlazada, ascendente=True):
    """
    Verifica manualmente en O(n) recorriendo los punteros `Node.next` de `MyLinkedList`
    si la lista enlazada está correctamente ordenada.
    """
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else MyLinkedList(lista_enlazada)
    if len(ll) <= 1 or ll.head is None:
        return True

    actual = ll.head
    while actual.next is not None:
        if ascendente:
            if actual.data > actual.next.data:
                return False
        else:
            if actual.data < actual.next.data:
                return False
        actual = actual.next
    return True


def invertir_lista_manual(lista_enlazada):
    """Invierte una MyLinkedList utilizando su método propio `.reverse()` de punteros O(n)."""
    if isinstance(lista_enlazada, MyLinkedList):
        lista_enlazada.reverse()
        return lista_enlazada
    ll = MyLinkedList(lista_enlazada)
    ll.reverse()
    return ll


# =====================================================================
# 1. ORDENAMIENTO BURBUJA (BUBBLE SORT SOBRE MYLINKEDLIST) - Origen: ADA1/burbuja.py
# =====================================================================
def ordenamiento_burbuja(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` recorriendo directamente sus nodos enlazados (`cur = ll.head` y `cur.next`)
    e intercambiando `cur.data` con `cur.next.data`.
    Complejidad: Mejor caso O(n), Caso promedio y peor caso O(n^2).
    """
    t0 = time.perf_counter()
    datos_ll = asegurar_linked_list(lista)
    n = len(datos_ll)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):
        hubo_intercambio = False
        cur = datos_ll.head
        for _ in range(n - 1 - i):
            comparaciones += 1
            sig = cur.next
            condicion = (cur.data > sig.data) if ascendente else (cur.data < sig.data)
            if condicion:
                cur.data, sig.data = sig.data, cur.data
                hubo_intercambio = True
                intercambios += 1
            cur = sig
        if not hubo_intercambio:
            break

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Burbuja (Bubble Sort)",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n²)",
            "comparaciones": comparaciones,
            "intercambios": intercambios,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


# =====================================================================
# 2. ORDENAMIENTO POR INSERCIÓN (INSERTION SORT CON MYLINKEDLIST) - Origen: ADA1/insercion.py
# =====================================================================
def ordenamiento_insercion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena los elementos de una `MyLinkedList` mediante Inserción Directa y reconstruye
    los nodos en una `MyLinkedList` ordenada.
    Complejidad: Mejor caso O(n), Caso promedio y peor caso O(n^2).
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    # Extraemos mediante el protocolo __iter__ de MyLinkedList
    datos = [x for x in entrada_ll]
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

    salida_ll = MyLinkedList(datos)
    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": salida_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Inserción (Insertion Sort)",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n²) / O(n) adaptativo",
            "comparaciones": comparaciones,
            "intercambios": desplazamientos,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(salida_ll, ascendente),
        }
    return salida_ll


# =====================================================================
# 3. ORDENAMIENTO POR SELECCIÓN (SELECTION SORT SOBRE MYLINKEDLIST) - Origen: ADA1/seleccion.py
# =====================================================================
def ordenamiento_seleccion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` recorriendo sus punteros `Node` para seleccionar el nodo extremo
    (mínimo o máximo) en cada pasada e intercambiando `nodo_i.data` con `nodo_extremo.data`.
    Complejidad: O(n^2) en todos los casos.
    """
    t0 = time.perf_counter()
    datos_ll = asegurar_linked_list(lista)
    comparaciones = 0
    intercambios = 0

    nodo_i = datos_ll.head
    while nodo_i is not None and nodo_i.next is not None:
        nodo_extremo = nodo_i
        nodo_j = nodo_i.next
        while nodo_j is not None:
            comparaciones += 1
            condicion = (nodo_j.data < nodo_extremo.data) if ascendente else (nodo_j.data > nodo_extremo.data)
            if condicion:
                nodo_extremo = nodo_j
            nodo_j = nodo_j.next

        if nodo_extremo is not nodo_i:
            nodo_i.data, nodo_extremo.data = nodo_extremo.data, nodo_i.data
            intercambios += 1
        nodo_i = nodo_i.next

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Selección (Selection Sort)",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n²)",
            "comparaciones": comparaciones,
            "intercambios": intercambios,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


# =====================================================================
# 4. ORDENAMIENTO SHELLSORT (CON MYLINKEDLIST) - Origen: ADA2/shellsort.py
# =====================================================================
def shell_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` utilizando incrementos decrecientes (ShellSort) y devuelve
    el resultado encapsulado en `MyLinkedList`.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    datos = [x for x in entrada_ll]
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

    salida_ll = MyLinkedList(datos)
    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": salida_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "ShellSort",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n^1.25 ~ n log² n)",
            "comparaciones": comparaciones,
            "intercambios": desplazamientos,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(salida_ll, ascendente),
        }
    return salida_ll


# =====================================================================
# 5. ORDENAMIENTO QUICKSORT (PARTICIÓN DE MYLINKEDLIST) - Origen: ADA2/quicksort.py
# =====================================================================
def quicksort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` mediante Divide y Vencerás creando sublistas enlazadas
    `MyLinkedList` para `menores`, `iguales` y `mayores` en cada partición.
    Complejidad: Promedio O(n log n).
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    metricas = {"comparaciones": 0, "movimientos": 0}

    def _qs_linked(sub_ll):
        if len(sub_ll) <= 1:
            return sub_ll

        # Pivote tomado de la cabeza o centro de la MyLinkedList
        pivote = sub_ll.head.data
        if sub_ll.head.next is not None and sub_ll.tail is not None:
            # Media simple entre head y tail para evitar peor caso en listas ordenadas
            a = sub_ll.head.data
            b = sub_ll.head.next.data
            c = sub_ll.tail.data
            if (a <= b <= c) or (c <= b <= a):
                pivote = b
            elif (b <= a <= c) or (c <= a <= b):
                pivote = a
            else:
                pivote = c

        menores = MyLinkedList()
        iguales = MyLinkedList()
        mayores = MyLinkedList()

        cur = sub_ll.head
        while cur is not None:
            x = cur.data
            metricas["comparaciones"] += 1
            metricas["movimientos"] += 1
            if x < pivote:
                menores.append(x)
            elif x > pivote:
                mayores.append(x)
            else:
                iguales.append(x)
            cur = cur.next

        izq_ord = _qs_linked(menores) if ascendente else _qs_linked(mayores)
        der_ord = _qs_linked(mayores) if ascendente else _qs_linked(menores)

        resultado = MyLinkedList()
        resultado.extend(izq_ord)
        resultado.extend(iguales)
        resultado.extend(der_ord)
        return resultado

    salida_ll = _qs_linked(entrada_ll)
    t1 = time.perf_counter()

    if retornar_metricas:
        return {
            "datos": salida_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Quicksort",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(salida_ll, ascendente),
        }
    return salida_ll


# =====================================================================
# 6. ORDENAMIENTO HEAPSORT (CON MYLINKEDLIST) - Origen: ADA2/heapsort.py
# =====================================================================
def _heapify(lista, n, i, ascendente, metricas):
    extremo = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n:
        metricas["comparaciones"] += 1
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
    Ordena una `MyLinkedList` mediante montículo binario (Max-Heap / Min-Heap) y retorna
    la secuencia ordenada como instancia de `MyLinkedList`.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    datos = [x for x in entrada_ll]
    n = len(datos)
    metricas = {"comparaciones": 0, "intercambios": 0}

    for i in range(n // 2 - 1, -1, -1):
        _heapify(datos, n, i, ascendente, metricas)

    for i in range(n - 1, 0, -1):
        datos[0], datos[i] = datos[i], datos[0]
        metricas["intercambios"] += 1
        _heapify(datos, i, 0, ascendente, metricas)

    salida_ll = MyLinkedList(datos)
    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": salida_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Heapsort",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["intercambios"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(salida_ll, ascendente),
        }
    return salida_ll


# =====================================================================
# 7. ORDENAMIENTO RADIX SORT (CUBETAS MYLINKEDLIST) - Origen: ADA2/radix.py
# =====================================================================
def _maximo_manual_ll(ll):
    """Obtiene el valor máximo recorriendo los nodos de MyLinkedList."""
    cur = ll.head
    m = cur.data
    cur = cur.next
    while cur is not None:
        if cur.data > m:
            m = cur.data
        cur = cur.next
    return m


def _radix_cubetas_linked(ll, exp, metricas):
    """Distribuye los nodos de MyLinkedList en 10 cubetas que también son instancias de MyLinkedList."""
    cubetas = [MyLinkedList() for _ in range(10)]
    cur = ll.head
    while cur is not None:
        digito = (cur.data // exp) % 10
        cubetas[digito].append(cur.data)
        metricas["movimientos"] += 1
        cur = cur.next

    ll.clear()
    for cubeta in cubetas:
        cur_c = cubeta.head
        while cur_c is not None:
            ll.append(cur_c.data)
            metricas["movimientos"] += 1
            cur_c = cur_c.next


def radix_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` de enteros (positivos y negativos) dígito por dígito (Radix Sort LSD)
    usando 10 cubetas enlazadas `MyLinkedList` e invirtiendo con `.reverse()` de `MyLinkedList`.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    metricas = {"comparaciones": 0, "movimientos": 0}

    if entrada_ll.is_empty():
        salida_ll = MyLinkedList()
    else:
        negativos = MyLinkedList()
        positivos = MyLinkedList()
        cur = entrada_ll.head
        while cur is not None:
            if cur.data < 0:
                negativos.append(-cur.data)
            else:
                positivos.append(cur.data)
            cur = cur.next

        if not positivos.is_empty():
            max_pos = _maximo_manual_ll(positivos)
            exp = 1
            while max_pos // exp > 0:
                _radix_cubetas_linked(positivos, exp, metricas)
                exp *= 10

        if not negativos.is_empty():
            max_neg = _maximo_manual_ll(negativos)
            exp = 1
            while max_neg // exp > 0:
                _radix_cubetas_linked(negativos, exp, metricas)
                exp *= 10
            # Usamos el método propio .reverse() de MyLinkedList
            negativos.reverse()

        salida_ll = MyLinkedList()
        cur_neg = negativos.head
        while cur_neg is not None:
            salida_ll.append(-cur_neg.data)
            cur_neg = cur_neg.next
        salida_ll.extend(positivos)

        if not ascendente:
            salida_ll.reverse()

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": salida_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Radix Sort (LSD)",
            "tipo": "Interno (MyLinkedList Cubetas)",
            "complejidad": "O(d · n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(salida_ll, ascendente),
        }
    return salida_ll


CATALOGO_INTERNOS = {
    "burbuja": ("Burbuja (Bubble Sort)", ordenamiento_burbuja),
    "insercion": ("Inserción (Insertion Sort)", ordenamiento_insercion),
    "seleccion": ("Selección (Selection Sort)", ordenamiento_seleccion),
    "shellsort": ("ShellSort", shell_sort),
    "quicksort": ("Quicksort", quicksort),
    "heapsort": ("Heapsort", heapsort),
    "radix": ("Radix Sort (LSD)", radix_sort),
}
