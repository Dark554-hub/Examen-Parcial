"""
Librería de Algoritmos de Búsqueda:
- Requerimiento 3 y 5C del Examen Parcial:
  1. Búsqueda Secuencial (Lineal) -> O(n), funciona en listas ordenadas y desordenadas.
  2. Búsqueda Binaria (Iterativa y Recursiva) -> O(log n), requiere lista ordenada (soporta ascendente y descendente).
  3. Búsqueda por Tabla Hash (Con encadenamiento separado para colisiones) -> O(1) promedio, ideal para búsquedas frecuentes.
"""

import time


# =====================================================================
# 1. BÚSQUEDA SECUENCIAL (LINEAR SEARCH)
# =====================================================================
def busqueda_secuencial(lista, objetivo):
    """
    Recorre secuencialmente la lista desde el índice 0 hasta n-1 buscando todas las
    apariciones del valor objetivo.
    Complejidad: O(n). No requiere que los datos estén ordenados.
    """
    t0 = time.perf_counter()
    posiciones = []
    comparaciones = 0

    for i in range(len(lista)):
        comparaciones += 1
        if lista[i] == objetivo:
            posiciones.append(i)

    t1 = time.perf_counter()
    encontrado = len(posiciones) > 0
    return {
        "metodo": "Búsqueda Secuencial (Lineal)",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones[0] if encontrado else -1,
        "todas_posiciones": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(n)",
    }


# =====================================================================
# 2. BÚSQUEDA BINARIA (BINARY SEARCH - ASCENDENTE Y DESCENDENTE)
# =====================================================================
def busqueda_binaria(lista_ordenada, objetivo, ascendente=True):
    """
    Realiza una búsqueda dicotómica (binaria) dividiendo el intervalo a la mitad en cada paso.
    Detecta además todas las ocurrencias contiguas del valor si existen duplicados.
    Complejidad: O(log n). Requiere que la lista esté previamente ordenada.
    """
    t0 = time.perf_counter()
    n = len(lista_ordenada)
    izq = 0
    der = n - 1
    comparaciones = 0
    indice_encontrado = -1
    traza_pasos = []

    while izq <= der:
        medio = (izq + der) // 2
        val_medio = lista_ordenada[medio]
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

    posiciones = []
    if indice_encontrado != -1:
        # Expandir hacia la izquierda y derecha para capturar duplicados contiguos
        k = indice_encontrado
        while k >= 0 and lista_ordenada[k] == objetivo:
            k -= 1
        inicio = k + 1
        k = indice_encontrado
        while k < n and lista_ordenada[k] == objetivo:
            k += 1
        fin = k - 1
        posiciones = list(range(inicio, fin + 1))

    t1 = time.perf_counter()
    encontrado = indice_encontrado != -1
    return {
        "metodo": "Búsqueda Binaria (Dicotómica)",
        "objetivo": objetivo,
        "encontrado": encontrado,
        "indice_primero": posiciones[0] if encontrado else -1,
        "todas_posiciones": posiciones,
        "total_apariciones": len(posiciones),
        "comparaciones": comparaciones,
        "traza_pasos": traza_pasos,
        "tiempo_seg": t1 - t0,
        "tiempo_ms": (t1 - t0) * 1000.0,
        "complejidad": "O(log n)",
    }


# =====================================================================
# 3. BÚSQUEDA POR TABLA HASH (HASH TABLE SEARCH - ENCADENAMIENTO)
# =====================================================================
class TablaHashTransacciones:
    """
    Estructura de Tabla Hash personalizada con función hash modular y resolución de
    colisiones por encadenamiento separado (Separate Chaining).
    Permite indexar miles de registros financieros y realizar búsquedas en O(1) promedio.
    """

    def __init__(self, capacidad=2003):
        # Usamos un número primo para minimizar colisiones en distribución modular
        self.capacidad = capacidad
        self.cubetas = [[] for _ in range(capacidad)]
        self.total_elementos = 0
        self.colisiones = 0
        self.tiempo_construccion_ms = 0.0

    def funcion_hash(self, clave):
        """Calcula el índice de cubeta para cualquier número entero (positivo o negativo)."""
        return (clave if clave >= 0 else -clave * 31) % self.capacidad

    def construir_desde_lista(self, lista):
        """Indexa todos los elementos de una lista guardando sus posiciones originales."""
        t0 = time.perf_counter()
        self.cubetas = [[] for _ in range(self.capacidad)]
        self.total_elementos = 0
        self.colisiones = 0

        for idx, valor in enumerate(lista):
            h = self.funcion_hash(valor)
            cubeta = self.cubetas[h]
            if len(cubeta) > 0:
                # Verificar si la clave ya existe en la cubeta
                encontrado_en_cubeta = False
                for entrada in cubeta:
                    if entrada[0] == valor:
                        entrada[1].append(idx)
                        encontrado_en_cubeta = True
                        break
                if not encontrado_en_cubeta:
                    self.colisiones += 1
                    cubeta.append((valor, [idx]))
            else:
                cubeta.append((valor, [idx]))
            self.total_elementos += 1

        t1 = time.perf_counter()
        self.tiempo_construccion_ms = (t1 - t0) * 1000.0
        return self

    def buscar(self, objetivo):
        """Busca un valor en la tabla hash en tiempo O(1) promedio."""
        t0 = time.perf_counter()
        h = self.funcion_hash(objetivo)
        cubeta = self.cubetas[h]
        comparaciones = 0
        posiciones = []

        for clave, indices in cubeta:
            comparaciones += 1
            if clave == objetivo:
                posiciones = indices[:]
                break

        t1 = time.perf_counter()
        encontrado = len(posiciones) > 0
        return {
            "metodo": "Búsqueda por Tabla Hash (O(1))",
            "objetivo": objetivo,
            "encontrado": encontrado,
            "indice_primero": posiciones[0] if encontrado else -1,
            "todas_posiciones": posiciones,
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


def busqueda_hash(lista, objetivo, tabla_preconstruida=None):
    """Función envoltorio para realizar búsqueda por Hash sobre una lista de registros."""
    if tabla_preconstruida is None:
        # Escalar tamaño primo según volumen de datos
        cap = 2003 if len(lista) <= 2000 else 10007
        tabla_preconstruida = TablaHashTransacciones(capacidad=cap).construir_desde_lista(lista)
    return tabla_preconstruida.buscar(objetivo)
