"""
Librería de Algoritmos de Ordenamiento Externo (Procesamiento Basado en Archivos Auxiliares y Corridas).
Reutilización obligatoria de la librería propia `MyLinkedList.py` (`estructura/MyLinkedList.py`)
y de las librerías propias desarrolladas en `MetOrdena`:
- `MyLinkedList` -> Estructura enlazada para los archivos/flujos auxiliares `F1`, `F2` y corridas naturales.
- `MetOrdena/intercalacion.py` -> Intercalación de listas enlazadas con punteros `Node`
- `MetOrdena/mezcla_directa.py` -> Mezcla Directa (Direct Merge Sort con bloques 1, 2, 4, 8...)
- `MetOrdena/mezcla_equilibrada.py` -> Mezcla Equilibrada / Natural (Natural Merge Sort por corridas)

RESTRICCIÓN ESTRICTA:
Prohibido el uso de .sort(), sorted() o cualquier biblioteca automática de ordenamiento.
"""

import os
import time
from MyLinkedList import MyLinkedList
from librerias.ordenamientos_internos import asegurar_linked_list, verificar_orden


# =====================================================================
# 1. INTERCALACIÓN (MERGE DE MYLINKEDLIST) - Origen: MetOrdena/intercalacion.py
# =====================================================================
def intercalar_listas(lista_a, lista_b, ascendente=True, metricas=None):
    """
    Intercala dos instancias de `MyLinkedList` previamente ordenadas en una sola `MyLinkedList`
    recorriendo directamente sus punteros `Node` (`cur_a` y `cur_b`) en O(n + m).
    """
    ll_a = lista_a if isinstance(lista_a, MyLinkedList) else MyLinkedList(lista_a)
    ll_b = lista_b if isinstance(lista_b, MyLinkedList) else MyLinkedList(lista_b)

    resultado = MyLinkedList()
    cur_a = ll_a.head
    cur_b = ll_b.head

    while cur_a is not None and cur_b is not None:
        if metricas is not None:
            metricas["comparaciones"] += 1
            metricas["movimientos"] += 1
        condicion = (cur_a.data <= cur_b.data) if ascendente else (cur_a.data >= cur_b.data)
        if condicion:
            resultado.append(cur_a.data)
            cur_a = cur_a.next
        else:
            resultado.append(cur_b.data)
            cur_b = cur_b.next

    while cur_a is not None:
        resultado.append(cur_a.data)
        cur_a = cur_a.next
        if metricas is not None:
            metricas["movimientos"] += 1

    while cur_b is not None:
        resultado.append(cur_b.data)
        cur_b = cur_b.next
        if metricas is not None:
            metricas["movimientos"] += 1

    return resultado


def _dividir_linked_list_mitad(ll):
    """Divide una MyLinkedList en dos mitades (izquierda y derecha) recorriendo sus nodos."""
    mitad = len(ll) // 2
    izq = MyLinkedList()
    der = MyLinkedList()
    cur = ll.head
    idx = 0
    while cur is not None:
        if idx < mitad:
            izq.append(cur.data)
        else:
            der.append(cur.data)
        cur = cur.next
        idx += 1
    return izq, der


def ordenamiento_intercalacion(lista, ascendente=True, retornar_metricas=False):
    """
    Ordena una `MyLinkedList` dividiéndola recursivamente en corridas enlazadas e intercalándolas
    mediante `intercalar_listas` de `MetOrdena/intercalacion.py`.
    Complejidad: O(n log n) garantizado.
    """
    t0 = time.perf_counter()
    entrada_ll = asegurar_linked_list(lista)
    metricas = {"comparaciones": 0, "movimientos": 0, "pasadas": 0}

    def _dividir_e_intercalar(sub_ll):
        if len(sub_ll) <= 1:
            return sub_ll
        izq, der = _dividir_linked_list_mitad(sub_ll)
        izq_ord = _dividir_e_intercalar(izq)
        der_ord = _dividir_e_intercalar(der)
        metricas["pasadas"] += 1
        return intercalar_listas(izq_ord, der_ord, ascendente, metricas)

    datos_ll = _dividir_e_intercalar(entrada_ll)
    t1 = time.perf_counter()

    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Intercalación (External Merge)",
            "tipo": "Externo (MyLinkedList)",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": metricas["pasadas"],
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


# =====================================================================
# 2. MEZCLA DIRECTA (DIRECT MERGE SORT CON MYLINKEDLIST) - Origen: MetOrdena/mezcla_directa.py
# =====================================================================
def _particionar_directa_ll(datos_ll, tam_bloque):
    """
    Divide una `MyLinkedList` en dos listas enlazadas auxiliares `F1` y `F2` (cada una es una
    `MyLinkedList` de bloques `MyLinkedList` de longitud fija `tam_bloque`).
    """
    f1 = MyLinkedList()
    f2 = MyLinkedList()
    usar_f1 = True

    cur = datos_ll.head
    while cur is not None:
        bloque = MyLinkedList()
        k = 0
        while cur is not None and k < tam_bloque:
            bloque.append(cur.data)
            cur = cur.next
            k += 1
        if usar_f1:
            f1.append(bloque)
        else:
            f2.append(bloque)
        usar_f1 = not usar_f1

    return f1, f2


def _guardar_auxiliares_disco(f1_ll, f2_ll, dir_temp, etiqueta):
    """Persiste los tramos de las MyLinkedList auxiliares F1 y F2 en disco para auditoría."""
    os.makedirs(dir_temp, exist_ok=True)
    ruta_f1 = os.path.join(dir_temp, f"F1_{etiqueta}.txt")
    ruta_f2 = os.path.join(dir_temp, f"F2_{etiqueta}.txt")
    with open(ruta_f1, "w", encoding="utf-8") as arch1:
        idx = 1
        cur = f1_ll.head
        while cur is not None:
            tramo = cur.data
            muestra = []
            c_t = tramo.head
            while c_t is not None and len(muestra) < 25:
                muestra.append(str(c_t.data))
                c_t = c_t.next
            arch1.write(f"MyLinkedList_Tramo_{idx}: " + ",".join(muestra) + ("..." if len(tramo) > 25 else "") + "\n")
            cur = cur.next
            idx += 1
    with open(ruta_f2, "w", encoding="utf-8") as arch2:
        idx = 1
        cur = f2_ll.head
        while cur is not None:
            tramo = cur.data
            muestra = []
            c_t = tramo.head
            while c_t is not None and len(muestra) < 25:
                muestra.append(str(c_t.data))
                c_t = c_t.next
            arch2.write(f"MyLinkedList_Tramo_{idx}: " + ",".join(muestra) + ("..." if len(tramo) > 25 else "") + "\n")
            cur = cur.next
            idx += 1
    return ruta_f1, ruta_f2


def mezcla_directa(lista, ascendente=True, retornar_metricas=False, dir_auxiliar=None):
    """
    Ordena una `MyLinkedList` mediante Mezcla Directa (bloques de longitud 1, 2, 4, 8, 16...).
    Los archivos auxiliares `F1` y `F2` son instancias de `MyLinkedList`.
    Complejidad: O(n log n) en exactamente ceil(log2(n)) pasadas externas.
    """
    t0 = time.perf_counter()
    datos_ll = asegurar_linked_list(lista)
    n = len(datos_ll)
    tam_bloque = 1
    pasada = 0
    metricas = {"comparaciones": 0, "movimientos": 0}
    archivos_aux = MyLinkedList()

    while tam_bloque < n:
        pasada += 1
        f1, f2 = _particionar_directa_ll(datos_ll, tam_bloque)

        if dir_auxiliar and pasada in (1, 2):
            r1, r2 = _guardar_auxiliares_disco(f1, f2, dir_auxiliar, f"directa_pasada_{pasada}")
            archivos_aux.append(r1)
            archivos_aux.append(r2)

        datos_ll = MyLinkedList()
        cur_f1 = f1.head
        cur_f2 = f2.head
        while cur_f1 is not None or cur_f2 is not None:
            b1 = cur_f1.data if cur_f1 is not None else MyLinkedList()
            b2 = cur_f2.data if cur_f2 is not None else MyLinkedList()
            fusionado = intercalar_listas(b1, b2, ascendente, metricas)
            datos_ll.extend(fusionado)
            if cur_f1 is not None:
                cur_f1 = cur_f1.next
            if cur_f2 is not None:
                cur_f2 = cur_f2.next

        tam_bloque *= 2

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Mezcla Directa (Direct Merge Sort)",
            "tipo": "Externo (MyLinkedList F1 y F2)",
            "complejidad": "O(n log n)",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": pasada,
            "archivos_auxiliares": archivos_aux,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


# =====================================================================
# 3. MEZCLA EQUILIBRADA / NATURAL (CON MYLINKEDLIST) - Origen: MetOrdena/mezcla_equilibrada.py
# =====================================================================
def obtener_tramos_naturales(datos_ll, ascendente=True, metricas=None):
    """
    Recorre los nodos de `MyLinkedList` detectando subsecuencias contiguas (corridas)
    que ya están ordenadas naturalmente, retornando una `MyLinkedList` de tramos `MyLinkedList`.
    """
    ll = datos_ll if isinstance(datos_ll, MyLinkedList) else MyLinkedList(datos_ll)
    tramos = MyLinkedList()
    if ll.is_empty():
        return tramos

    cur = ll.head
    actual = MyLinkedList([cur.data])
    ultimo_val = cur.data
    cur = cur.next

    while cur is not None:
        x = cur.data
        if metricas is not None:
            metricas["comparaciones"] += 1
        condicion = (x >= ultimo_val) if ascendente else (x <= ultimo_val)
        if condicion:
            actual.append(x)
        else:
            tramos.append(actual)
            actual = MyLinkedList([x])
        ultimo_val = x
        cur = cur.next

    tramos.append(actual)
    return tramos


def mezcla_equilibrada(lista, ascendente=True, retornar_metricas=False, dir_auxiliar=None):
    """
    Ordena una `MyLinkedList` usando Mezcla Equilibrada (Natural Merge Sort).
    Aprovecha corridas naturales y las reparte alternadamente entre dos `MyLinkedList`
    auxiliares `F1` y `F2`.
    """
    t0 = time.perf_counter()
    datos_ll = asegurar_linked_list(lista)
    iteracion = 0
    metricas = {"comparaciones": 0, "movimientos": 0}
    tramos_iniciales = 0
    archivos_aux = MyLinkedList()

    while True:
        tramos = obtener_tramos_naturales(datos_ll, ascendente, metricas)
        if iteracion == 0:
            tramos_iniciales = len(tramos)
        if len(tramos) <= 1:
            break

        iteracion += 1
        f1 = MyLinkedList()
        f2 = MyLinkedList()
        usar_f1 = True
        cur_t = tramos.head
        while cur_t is not None:
            if usar_f1:
                f1.append(cur_t.data)
            else:
                f2.append(cur_t.data)
            usar_f1 = not usar_f1
            cur_t = cur_t.next

        if dir_auxiliar and iteracion in (1, 2):
            r1, r2 = _guardar_auxiliares_disco(f1, f2, dir_auxiliar, f"equilibrada_iter_{iteracion}")
            archivos_aux.append(r1)
            archivos_aux.append(r2)

        datos_ll = MyLinkedList()
        cur_f1 = f1.head
        cur_f2 = f2.head
        while cur_f1 is not None or cur_f2 is not None:
            t1_tramo = cur_f1.data if cur_f1 is not None else MyLinkedList()
            t2_tramo = cur_f2.data if cur_f2 is not None else MyLinkedList()
            datos_ll.extend(intercalar_listas(t1_tramo, t2_tramo, ascendente, metricas))
            if cur_f1 is not None:
                cur_f1 = cur_f1.next
            if cur_f2 is not None:
                cur_f2 = cur_f2.next

    t1 = time.perf_counter()
    if retornar_metricas:
        return {
            "datos": datos_ll,
            "estructura": "MyLinkedList",
            "algoritmo": "Mezcla Equilibrada (Natural Merge)",
            "tipo": "Externo (MyLinkedList Corridas F1/F2)",
            "complejidad": "O(n log n) / O(n) adaptativo",
            "comparaciones": metricas["comparaciones"],
            "intercambios": metricas["movimientos"],
            "pasadas_externas": iteracion,
            "tramos_iniciales": tramos_iniciales,
            "archivos_auxiliares": archivos_aux,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "orden": "Ascendente" if ascendente else "Descendente",
            "verificado": verificar_orden(datos_ll, ascendente),
        }
    return datos_ll


CATALOGO_EXTERNOS = {
    "intercalacion": ("Intercalación (External Merge)", ordenamiento_intercalacion),
    "mezcla_directa": ("Mezcla Directa (Direct Merge Sort)", mezcla_directa),
    "mezcla_equilibrada": ("Mezcla Equilibrada (Natural Merge)", mezcla_equilibrada),
}
