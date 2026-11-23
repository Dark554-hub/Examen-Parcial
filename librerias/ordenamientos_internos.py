"""
Librería de Algoritmos de Ordenamiento Interno (En Memoria RAM).
Reutilización exclusiva y obligatoria de tu librería propia `MyLinkedList.py` (`Node` y `MyLinkedList`)
proveniente de `c:\\Users\\Emili\\OneDrive\\Desktop\\estructura\\MyLinkedList.py`.

RESTRICCIÓN ESTRICTA:
- SOLO se utiliza la librería propia `MyLinkedList.py` (`Node` y `MyLinkedList`) como estructura de datos.
- Cero uso de listas nativas de Python (`list` / `[]`) en la lógica de ordenamiento.
- Cero uso de `.sort()`, `sorted()` o cualquier biblioteca automática de ordenamiento.
"""

import time
from MyLinkedList import Node, MyLinkedList


def asegurar_linked_list(coleccion):
    """Clona o construye una instancia nueva de MyLinkedList recorriendo únicamente nodos."""
    nueva = MyLinkedList()
    if coleccion is not None:
        if isinstance(coleccion, MyLinkedList):
            cur = coleccion.head
            while cur is not None:
                nueva.append(cur.data)
                cur = cur.next
        else:
            nueva.extend(coleccion)
    return nueva


def verificar_orden(lista_enlazada, ascendente=True):
    """
    Verifica manualmente en O(n) recorriendo exclusivamente los punteros `Node.next` de `MyLinkedList`
    si la lista enlazada está correctamente ordenada.
    """
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else asegurar_linked_list(lista_enlazada)
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
    """Invierte una MyLinkedList utilizando su propio método `.reverse()` de punteros Node.next en O(n)."""
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else asegurar_linked_list(lista_enlazada)
    ll.reverse()
    return ll


# =====================================================================
# 1. ORDENAMIENTO BURBUJA (100% PUNTEROS DE MYLINKEDLIST) - Origen: ADA1/burbuja.py
# =====================================================================
def ordenamiento_burbuja(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` recorriendo exclusivamente sus punteros `cur = datos_ll.head`
    y `sig = cur.next`, intercambiando `cur.data` y `sig.data`.
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
# 2. ORDENAMIENTO POR INSERCIÓN (100% REENLACE DE NODOS NODE EN MYLINKEDLIST)
# =====================================================================
def ordenamiento_insercion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` mediante Inserción Directa re-enlazando directamente
    instancias `Node` de `MyLinkedList` en una cadena ordenada (0% uso de listas de Python).
    Mantiene un puntero de búsqueda rápida al último nodo insertado para lograr O(n) en datos ordenados.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    comparaciones = 0
    desplazamientos = 0

    ordenada_ll = MyLinkedList()
    cur = entrada_ll.head

    while cur is not None:
        val = cur.data
        if ordenada_ll.head is None:
            ordenada_ll.append(val)
        else:
            comparaciones += 1
            # Caso 1: Insertar al final en O(1) usando ordenada_ll.tail
            va_al_final = (val >= ordenada_ll.tail.data) if ascendente else (val <= ordenada_ll.tail.data)
            if va_al_final:
                ordenada_ll.append(val)
            else:
                comparaciones += 1
                # Caso 2: Insertar al inicio en O(1) usando ordenada_ll.head
                va_al_inicio = (val <= ordenada_ll.head.data) if ascendente else (val >= ordenada_ll.head.data)
                if va_al_inicio:
                    ordenada_ll.prepend(val)
                    desplazamientos += 1
                else:
                    # Caso 3: Recorrer los punteros Node.next de ordenada_ll para insertar en su sitio
                    prev = ordenada_ll.head
                    while prev.next is not None:
                        comparaciones += 1
                        cond = (prev.next.data < val) if ascendente else (prev.next.data > val)
                        if cond:
                            prev = prev.next
                            desplazamientos += 1
                        else:
                            break
                    nuevo_nodo = Node(val, prev.next)
                    prev.next = nuevo_nodo
                    ordenada_ll._size += 1
                    desplazamientos += 1
        cur = cur.next

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": ordenada_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Inserción (Insertion Sort)",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n²) / O(n) adaptativo",
            "comparaciones": comparaciones,
            "intercambios": desplazamientos,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(ordenada_ll, ascendente),
        }
    return ordenada_ll


# =====================================================================
# 3. ORDENAMIENTO POR SELECCIÓN (100% PUNTEROS DE MYLINKEDLIST) - Origen: ADA1/seleccion.py
# =====================================================================
def ordenamiento_seleccion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` recorriendo sus punteros `Node` (`nodo_i` y `nodo_j = nodo_i.next`)
    para seleccionar el nodo extremo en cada pasada e intercambiar `nodo_i.data` con `nodo_extremo.data`.
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
# 4. ORDENAMIENTO SHELLSORT (100% SUBLISTAS ENLAZADAS MYLINKEDLIST) - Origen: ADA2/shellsort.py
# =====================================================================
def _insercion_sobre_linked_list(sub_ll, ascendente, metricas):
    """Aplica inserción por punteros Node sobre una sub-MyLinkedList de brecha (gap)."""
    if len(sub_ll) <= 1:
        return sub_ll
    ord_ll = MyLinkedList()
    cur = sub_ll.head
    while cur is not None:
        val = cur.data
        if ord_ll.head is None:
            ord_ll.append(val)
        else:
            metricas["comparaciones"] += 1
            if (val >= ord_ll.tail.data) if ascendente else (val <= ord_ll.tail.data):
                ord_ll.append(val)
            else:
                metricas["comparaciones"] += 1
                if (val <= ord_ll.head.data) if ascendente else (val >= ord_ll.head.data):
                    ord_ll.prepend(val)
                    metricas["desplazamientos"] += 1
                else:
                    prev = ord_ll.head
                    while prev.next is not None:
                        metricas["comparaciones"] += 1
                        if (prev.next.data < val) if ascendente else (prev.next.data > val):
                            prev = prev.next
                            metricas["desplazamientos"] += 1
                        else:
                            break
                    prev.next = Node(val, prev.next)
                    ord_ll._size += 1
                    metricas["desplazamientos"] += 1
        cur = cur.next
    return ord_ll


def shell_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` por incrementos decrecientes (`salto = n // 2`, `salto //= 2`)
    repartiendo en cada brecha los nodos en `salto` sub-listas `MyLinkedList` (almacenadas en una
    `MyLinkedList` de `MyLinkedList`), ordenando cada sub-lista por inserción de punteros `Node`
    y reintercalándolas en la `MyLinkedList` principal. 0% uso de listas de Python.
    """
    t0 = time.perf_counter()
    datos_ll = asegurar_linked_list(lista)
    n = len(datos_ll)
    salto = n // 2
    metricas = {"comparaciones": 0, "desplazamientos": 0}

    while salto > 0:
        if salto == 1:
            datos_ll = _insercion_sobre_linked_list(datos_ll, ascendente, metricas)
        else:
            # Crear una MyLinkedList que contiene `salto` sub-listas MyLinkedList
            columnas_ll = MyLinkedList()
            for _ in range(salto):
                columnas_ll.append(MyLinkedList())

            # Distribuir nodos de datos_ll circularmente entre las `salto` sub-MyLinkedList
            cur_dato = datos_ll.head
            cur_col = columnas_ll.head
            while cur_dato is not None:
                cur_col.data.append(cur_dato.data)
                cur_dato = cur_dato.next
                cur_col = cur_col.next if cur_col.next is not None else columnas_ll.head

            # Ordenar cada sub-MyLinkedList con inserción de nodos Node
            cur_col = columnas_ll.head
            while cur_col is not None:
                cur_col.data = _insercion_sobre_linked_list(cur_col.data, ascendente, metricas)
                cur_col = cur_col.next

            # Reconstruir datos_ll extrayendo en redondo el nodo head de cada sub-MyLinkedList
            datos_ll.clear()
            quedan_elementos = True
            while quedan_elementos:
                quedan_elementos = False
                cur_col = columnas_ll.head
                while cur_col is not None:
                    sub = cur_col.data
                    if sub.head is not None:
                        datos_ll.append(sub.pop(0))
                        if sub.head is not None:
                            quedan_elementos = True
                    cur_col = cur_col.next

        salto //= 2

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "ShellSort",
            "tipo": "Interno (MyLinkedList)",
            "complejidad": "O(n^1.25 ~ n log² n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["desplazamientos"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


# =====================================================================
# 5. ORDENAMIENTO QUICKSORT (100% PARTICIÓN DE MYLINKEDLIST) - Origen: ADA2/quicksort.py
# =====================================================================
def quicksort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` mediante Divide y Vencerás creando únicamente sublistas enlazadas
    `MyLinkedList` para `menores`, `iguales` y `mayores` en cada partición.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    metricas = {"comparaciones": 0, "movimientos": 0}

    def _qs_linked(sub_ll):
        if len(sub_ll) <= 1:
            return sub_ll

        pivote = sub_ll.head.data
        if sub_ll.head.next is not None and sub_ll.tail is not None:
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
# 6. ORDENAMIENTO HEAPSORT (100% ÁRBOL DE NODOS MYLINKEDLIST) - Origen: ADA2/heapsort.py
# =====================================================================
def _sift_down_nodo_heap(nodo_heap, ascendente, metricas):
    """
    Hunde un valor en un montículo binario cuyos enlaces hijo_izq e hijo_der están
    almacenados en una instancia de `MyLinkedList` `[valor, sub_izq, sub_der]`.
    """
    actual = nodo_heap
    while actual is not None:
        val_actual = actual.head.data
        nodo_izq_ptr = actual.head.next
        nodo_der_ptr = nodo_izq_ptr.next
        hijo_izq = nodo_izq_ptr.data
        hijo_der = nodo_der_ptr.data

        mejor_hijo = None
        val_mejor = val_actual

        if hijo_izq is not None:
            metricas["comparaciones"] += 1
            val_i = hijo_izq.head.data
            if (val_i < val_mejor) if ascendente else (val_i > val_mejor):
                val_mejor = val_i
                mejor_hijo = hijo_izq

        if hijo_der is not None:
            metricas["comparaciones"] += 1
            val_d = hijo_der.head.data
            if (val_d < val_mejor) if ascendente else (val_d > val_mejor):
                val_mejor = val_d
                mejor_hijo = hijo_der

        if mejor_hijo is not None:
            actual.head.data, mejor_hijo.head.data = mejor_hijo.head.data, actual.head.data
            metricas["intercambios"] += 1
            actual = mejor_hijo
        else:
            break


def heapsort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` construyendo un árbol montículo binario (Heap) donde cada nodo
    del árbol y la cola de nivel (BFS) son instancias exclusivas de `MyLinkedList`.
    0% uso de listas nativas de Python. Complejidad: O(n log n).
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    n = len(entrada_ll)
    metricas = {"comparaciones": 0, "intercambios": 0}

    if n <= 1:
        salida_ll = entrada_ll
    else:
        # Construir árbol binario completo usando exclusivamente MyLinkedList
        # Cada nodo del heap es una MyLinkedList de 3 posiciones: [valor, hijo_izq, hijo_der]
        cur = entrada_ll.head
        raiz = MyLinkedList()
        raiz.append(cur.data)
        raiz.append(None)
        raiz.append(None)
        cur = cur.next

        cola_padres = MyLinkedList()
        cola_padres.append(raiz)
        pila_internos = MyLinkedList()

        while cur is not None:
            padre = cola_padres.head.data
            pila_internos.prepend(padre)

            # Hijo izquierdo
            h_izq = MyLinkedList()
            h_izq.append(cur.data)
            h_izq.append(None)
            h_izq.append(None)
            padre.head.next.data = h_izq
            cola_padres.append(h_izq)
            cur = cur.next

            # Hijo derecho (si aún hay elementos)
            if cur is not None:
                h_der = MyLinkedList()
                h_der.append(cur.data)
                h_der.append(None)
                h_der.append(None)
                padre.head.next.next.data = h_der
                cola_padres.append(h_der)
                cur = cur.next

            cola_padres.pop(0)

        # Fase 1: Heapify bottom-up sobre los nodos internos en pila_internos (MyLinkedList)
        cur_p = pila_internos.head
        while cur_p is not None:
            _sift_down_nodo_heap(cur_p.data, ascendente, metricas)
            cur_p = cur_p.next

        # Fase 2: Extracción sucesiva de la raíz hacia la MyLinkedList de salida
        CENTINELA = 10**18 if ascendente else -(10**18)
        salida_ll = MyLinkedList()
        for _ in range(n):
            salida_ll.append(raiz.head.data)
            raiz.head.data = CENTINELA
            metricas["intercambios"] += 1
            _sift_down_nodo_heap(raiz, ascendente, metricas)

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
# 7. ORDENAMIENTO RADIX SORT (100% MYLINKEDLIST DE MYLINKEDLIST) - Origen: ADA2/radix.py
# =====================================================================
def _maximo_manual_ll(ll):
    """Obtiene el valor máximo recorriendo los punteros Node de MyLinkedList."""
    cur = ll.head
    m = cur.data
    cur = cur.next
    while cur is not None:
        if cur.data > m:
            m = cur.data
        cur = cur.next
    return m


def _obtener_cubeta_en_ll(cubetas_ll, digito):
    """Avanza `digito` nodos (de 0 a 9) dentro de la MyLinkedList de cubetas."""
    cur = cubetas_ll.head
    for _ in range(digito):
        cur = cur.next
    return cur.data


def _radix_cubetas_linked(ll, exp, metricas):
    """
    Distribuye los nodos de `MyLinkedList` en 10 cubetas donde TANTO el contenedor de cubetas
    como cada cubeta individual son instancias de `MyLinkedList` (0% uso de `list` de Python).
    """
    cubetas_ll = MyLinkedList()
    for _ in range(10):
        cubetas_ll.append(MyLinkedList())

    cur = ll.head
    while cur is not None:
        digito = (cur.data // exp) % 10
        cubeta = _obtener_cubeta_en_ll(cubetas_ll, digito)
        cubeta.append(cur.data)
        metricas["movimientos"] += 1
        cur = cur.next

    ll.clear()
    nodo_cubeta = cubetas_ll.head
    while nodo_cubeta is not None:
        cubeta_actual = nodo_cubeta.data
        cur_c = cubeta_actual.head
        while cur_c is not None:
            ll.append(cur_c.data)
            metricas["movimientos"] += 1
            cur_c = cur_c.next
        nodo_cubeta = nodo_cubeta.next


def radix_sort(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` de enteros (positivos y negativos) dígito por dígito (Radix Sort LSD)
    usando una `MyLinkedList` de 10 cubetas `MyLinkedList` e invirtiendo con `.reverse()`.
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
