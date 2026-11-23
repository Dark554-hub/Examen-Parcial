"""
Librería de Algoritmos de Búsqueda utilizando EXCLUSIVAMENTE tu librería propia `MyLinkedList.py`:
- Requerimiento 3 y 5C del Examen Parcial:
  1. Búsqueda Secuencial (Lineal) -> O(n), recorre los punteros `Node` (`cur = ll.head`) de `MyLinkedList`.
  2. Búsqueda Binaria (Dicotómica) -> Indexa directamente sobre `MyLinkedList[medio]` usando `MyLinkedList.__getitem__`.
  3. Búsqueda por Tabla Hash -> El contenedor principal de cubetas (`self.cubetas`), cada cubeta individual
     y cada lista de índices de colisión son instancias de `MyLinkedList` (0% uso de listas nativas de Python).
"""

import time
from MyLinkedList import MyLinkedList
from librerias.ordenamientos_internos import asegurar_linked_list


# =====================================================================
# 1. BÚSQUEDA SECUENCIAL SOBRE MYLINKEDLIST (LINEAR SEARCH)
# =====================================================================
def busqueda_secuencial(lista_enlazada, objetivo):
    """
    Recorre secuencialmente los nodos (`cur = ll.head`, `cur = cur.next`) de una `MyLinkedList`
    desde el índice 0 hasta n-1 buscando todas las apariciones del valor objetivo.
    """
    t0 = time.perf_counter()
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else asegurar_linked_list(lista_enlazada)
    posiciones = MyLinkedList()
    comparaciones = 0

    cur = ll.head
    idx = 0
    while cur is not None:
        comparaciones += 1
        if cur.data == objetivo:
            posiciones.append(idx)
        cur = cur.next
        idx += 1

    t1 = time.perf_counter()
    encontrado = not posiciones.is_empty()
    return {
        "metodo": "Búsqueda Secuencial (MyLinkedList)",
        "estructura": "MyLinkedList",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones.head.data if encontrado else -1,
        "todas_posiciones": posiciones,
        "posiciones_linked_list": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(n)",
    }


# =====================================================================
# 2. BÚSQUEDA BINARIA DIRECTAMENTE SOBRE MYLINKEDLIST (ASCENDENTE Y DESCENDENTE)
# =====================================================================
def busqueda_binaria(lista_ordenada, objetivo, ascendente=True):
    """
    Realiza la búsqueda dicotómica (binaria) evaluando directamente `ll[medio]` mediante
    el protocolo `__getitem__` (`_node_at`) de tu librería `MyLinkedList.py` sin convertir a `list`.
    Guarda las posiciones encontradas y la traza de pasos en instancias de `MyLinkedList`.
    """
    t0 = time.perf_counter()
    ll = lista_ordenada if isinstance(lista_ordenada, MyLinkedList) else asegurar_linked_list(lista_ordenada)
    n = len(ll)
    izq = 0
    der = n - 1
    comparaciones = 0
    indice_encontrado = -1
    traza_pasos = MyLinkedList()

    while izq <= der:
        medio = (izq + der) // 2
        # Uso directo de __getitem__ de MyLinkedList.py
        val_medio = ll[medio]
        comparaciones += 1
        traza_pasos.append({"izq": izq, "der": der, "medio": medio, "valor_medio": val_medio})

        if val_medio == objetivo:
            indice_encontrado = medio
            break

        if ascendente:
            if val_medio < objetivo:
                izq = medio + 1
            else:
                der = medio - 1
        else:
            if val_medio > objetivo:
                izq = medio + 1
            else:
                der = medio - 1

    posiciones = MyLinkedList()
    if indice_encontrado != -1:
        k = indice_encontrado
        while k >= 0 and ll[k] == objetivo:
            k -= 1
        inicio = k + 1
        k = indice_encontrado
        while k < n and ll[k] == objetivo:
            k += 1
        fin = k - 1
        for pos in range(inicio, fin + 1):
            posiciones.append(pos)

    t1 = time.perf_counter()
    encontrado = indice_encontrado != -1
    return {
        "metodo": "Búsqueda Binaria (MyLinkedList)",
        "estructura": "MyLinkedList",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones.head.data if encontrado else -1,
        "todas_posiciones": posiciones,
        "posiciones_linked_list": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "traza_pasos": traza_pasos,
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(log n) comparaciones",
    }


# =====================================================================
# 3. BÚSQUEDA POR TABLA HASH 100% CONSTRUIDA CON MYLINKEDLIST
# =====================================================================
class TablaHashTransacciones:
    """
    Estructura de Tabla Hash personalizada construida 100% con `MyLinkedList`:
    - `self.cubetas` es una `MyLinkedList` donde cada nodo es una cubeta `MyLinkedList`.
    - Cada entrada de colisión dentro de una cubeta guarda `(clave, MyLinkedList_de_indices)`.
    Cero uso de listas nativas de Python (`list`).
    """

    def __init__(self, capacidad=257):
        self.capacidad = capacidad
        self.cubetas = MyLinkedList()
        for _ in range(capacidad):
            self.cubetas.append(MyLinkedList())
        self.total_elementos = 0
        self.colisiones = 0
        self.tiempo_construccion_ms = 0.0

    def funcion_hash(self, clave):
        """Calcula el índice de cubeta para cualquier número entero (positivo o negativo)."""
        return (clave if clave >= 0 else -clave * 31) % self.capacidad

    def construir_desde_lista(self, lista_enlazada):
        """Recorre los nodos de `MyLinkedList` e indexa cada valor en su cubeta `MyLinkedList`."""
        t0 = time.perf_counter()
        ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else asegurar_linked_list(lista_enlazada)
        self.cubetas = MyLinkedList()
        for _ in range(self.capacidad):
            self.cubetas.append(MyLinkedList())
        self.total_elementos = 0
        self.colisiones = 0

        cur = ll.head
        idx = 0
        while cur is not None:
            valor = cur.data
            h = self.funcion_hash(valor)
            # Acceso a la cubeta h mediante __getitem__ de MyLinkedList
            cubeta_ll = self.cubetas[h]

            if not cubeta_ll.is_empty():
                encontrado_en_cubeta = False
                nodo_c = cubeta_ll.head
                while nodo_c is not None:
                    clave_actual, indices_ll = nodo_c.data
                    if clave_actual == valor:
                        indices_ll.append(idx)
                        encontrado_en_cubeta = True
                        break
                    nodo_c = nodo_c.next
                if not encontrado_en_cubeta:
                    self.colisiones += 1
                    nueva_pos_ll = MyLinkedList()
                    nueva_pos_ll.append(idx)
                    cubeta_ll.append((valor, nueva_pos_ll))
            else:
                nueva_pos_ll = MyLinkedList()
                nueva_pos_ll.append(idx)
                cubeta_ll.append((valor, nueva_pos_ll))

            self.total_elementos += 1
            cur = cur.next
            idx += 1

        t1 = time.perf_counter()
        self.tiempo_construccion_ms = (t1 - t0) * 1000.0
        return self

    def buscar(self, objetivo):
        """Busca un valor accediendo a `self.cubetas[h]` (todo en `MyLinkedList`)."""
        t0 = time.perf_counter()
        h = self.funcion_hash(objetivo)
        cubeta_ll = self.cubetas[h]
        comparaciones = 0
        posiciones = MyLinkedList()

        nodo_c = cubeta_ll.head
        while nodo_c is not None:
            comparaciones += 1
            clave, indices_ll = nodo_c.data
            if clave == objetivo:
                posiciones = asegurar_linked_list(indices_ll)
                break
            nodo_c = nodo_c.next

        t1 = time.perf_counter()
        encontrado = not posiciones.is_empty()
        return {
            "metodo": "Búsqueda por Tabla Hash (MyLinkedList Chaining)",
            "estructura": "MyLinkedList",
            "objetivo": objetivo,
            "encontrado": encontrado,
            "indice_primero": posiciones.head.data if encontrado else -1,
            "todas_posiciones": posiciones,
            "posiciones_linked_list": posiciones,
            "total_apariciones": len(posiciones),
            "comparaciones": comparaciones if comparaciones > 0 else 1,
            "cubeta_hash": h,
            "colisiones_tabla": self.colisiones,
            "factor_carga": round(self.total_elementos / self.capacidad, 3),
            "tiempo_construccion_ms": self.tiempo_construccion_ms,
            "tiempo_seg": t1 - t0,
            "tiempo_ms": (t1 - t0) * 1000.0,
            "complejidad": "O(1) promedio",
        }


def busqueda_hash(lista_enlazada, objetivo, tabla_preconstruida=None):
    """Función envoltorio para realizar búsqueda por Hash sobre una `MyLinkedList`."""
    if tabla_preconstruida is None:
        cap = 257 if len(lista_enlazada) <= 2000 else 521
        tabla_preconstruida = TablaHashTransacciones(capacidad=cap).construir_desde_lista(lista_enlazada)
    return tabla_preconstruida.buscar(objetivo)
