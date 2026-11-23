"""
Librería de Algoritmos de Búsqueda utilizando obligatoriamente la librería propia `MyLinkedList.py`:
- Requerimiento 3 y 5C del Examen Parcial:
  1. Búsqueda Secuencial (Lineal) -> O(n), recorre los punteros `Node` (`cur = ll.head`) de `MyLinkedList`.
  2. Búsqueda Binaria (Dicotómica) -> O(log n), sobre los elementos de `MyLinkedList` ordenada.
  3. Búsqueda por Tabla Hash -> O(1) promedio, donde cada cubeta (bucket) y cada lista de índices de
     colisión es una instancia de `MyLinkedList` (encadenamiento separado con `MyLinkedList`).
"""

import time
from MyLinkedList import MyLinkedList


# =====================================================================
# 1. BÚSQUEDA SECUENCIAL SOBRE MYLINKEDLIST (LINEAR SEARCH)
# =====================================================================
def busqueda_secuencial(lista_enlazada, objetivo):
    """
    Recorre secuencialmente los nodos (`cur = ll.head`, `cur = cur.next`) de una `MyLinkedList`
    desde el índice 0 hasta n-1 buscando todas las apariciones del valor objetivo.
    Complejidad: O(n). No requiere que los datos estén ordenados.
    """
    t0 = time.perf_counter()
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else MyLinkedList(lista_enlazada)
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
    lista_pos = posiciones.to_list()
    return {
        "metodo": "Búsqueda Secuencial (MyLinkedList)",
        "estructura": "MyLinkedList",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones.head.data if encontrado else -1,
        "todas_posiciones": lista_pos,
        "posiciones_linked_list": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(n)",
    }


# =====================================================================
# 2. BÚSQUEDA BINARIA CON MYLINKEDLIST (ASCENDENTE Y DESCENDENTE)
# =====================================================================
def busqueda_binaria(lista_ordenada, objetivo, ascendente=True):
    """
    Realiza una búsqueda dicotómica (binaria) sobre una `MyLinkedList` ordenada.
    Guarda las posiciones encontradas y la traza de pasos en instancias de `MyLinkedList`.
    Complejidad: O(log n). Requiere que la `MyLinkedList` esté previamente ordenada.
    """
    t0 = time.perf_counter()
    ll = lista_ordenada if isinstance(lista_ordenada, MyLinkedList) else MyLinkedList(lista_ordenada)
    # Vector de acceso indexado extraído de MyLinkedList para saltos dicotómicos O(log n)
    vista = ll.to_list()
    n = len(vista)
    izq = 0
    der = n - 1
    comparaciones = 0
    indice_encontrado = -1
    traza_pasos = MyLinkedList()

    while izq <= der:
        medio = (izq + der) // 2
        val_medio = vista[medio]
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
        while k >= 0 and vista[k] == objetivo:
            k -= 1
        inicio = k + 1
        k = indice_encontrado
        while k < n and vista[k] == objetivo:
            k += 1
        fin = k - 1
        for pos in range(inicio, fin + 1):
            posiciones.append(pos)

    t1 = time.perf_counter()
    encontrado = indice_encontrado != -1
    lista_pos = posiciones.to_list()
    return {
        "metodo": "Búsqueda Binaria (MyLinkedList)",
        "estructura": "MyLinkedList",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones.head.data if encontrado else -1,
        "todas_posiciones": lista_pos,
        "posiciones_linked_list": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "traza_pasos": traza_pasos.to_list(),
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(log n)",
    }


# =====================================================================
# 3. BÚSQUEDA POR TABLA HASH CON ENCADENAMIENTO EN MYLINKEDLIST
# =====================================================================
class TablaHashTransacciones:
    """
    Estructura de Tabla Hash personalizada donde cada cubeta (bucket) es una instancia
    de tu librería propia `MyLinkedList` (Encadenamiento Separado con `MyLinkedList`).
    Cada nodo de la cubeta almacena `(clave, MyLinkedList_de_indices)`.
    """

    def __init__(self, capacidad=2003):
        self.capacidad = capacidad
        # Cada cubeta es una MyLinkedList propia para resolver colisiones por encadenamiento
        self.cubetas = [MyLinkedList() for _ in range(capacidad)]
        self.total_elementos = 0
        self.colisiones = 0
        self.tiempo_construccion_ms = 0.0

    def funcion_hash(self, clave):
        """Calcula el índice de cubeta para cualquier número entero (positivo o negativo)."""
        return (clave if clave >= 0 else -clave * 31) % self.capacidad

    def construir_desde_lista(self, lista_enlazada):
        """Recorre los nodos de `MyLinkedList` e indexa cada valor en su cubeta `MyLinkedList`."""
        t0 = time.perf_counter()
        ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else MyLinkedList(lista_enlazada)
        self.cubetas = [MyLinkedList() for _ in range(self.capacidad)]
        self.total_elementos = 0
        self.colisiones = 0

        cur = ll.head
        idx = 0
        while cur is not None:
            valor = cur.data
            h = self.funcion_hash(valor)
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
                    cubeta_ll.append((valor, MyLinkedList([idx])))
            else:
                cubeta_ll.append((valor, MyLinkedList([idx])))

            self.total_elementos += 1
            cur = cur.next
            idx += 1

        t1 = time.perf_counter()
        self.tiempo_construccion_ms = (t1 - t0) * 1000.0
        return self

    def buscar(self, objetivo):
        """Busca un valor recorriendo la `MyLinkedList` de la cubeta hash correspondiente en O(1) promedio."""
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
                posiciones = indices_ll.copy()
                break
            nodo_c = nodo_c.next

        t1 = time.perf_counter()
        encontrado = not posiciones.is_empty()
        lista_pos = posiciones.to_list()
        return {
            "metodo": "Búsqueda por Tabla Hash (MyLinkedList Chaining)",
            "estructura": "MyLinkedList",
            "objetivo": objetivo,
            "encontrado": encontrado,
            "indice_primero": posiciones.head.data if encontrado else -1,
            "todas_posiciones": lista_pos,
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
        cap = 2003 if len(lista_enlazada) <= 2000 else 10007
        tabla_preconstruida = TablaHashTransacciones(capacidad=cap).construir_desde_lista(lista_enlazada)
    return tabla_preconstruida.buscar(objetivo)
