"""
Librería de Diagnóstico y Corrección de Código Defectuoso (Requerimiento 4 del Examen Parcial).
Integrada con la librería propia `MyLinkedList.py` (`estructura/MyLinkedList.py`).

Incluye los 5 casos de errores lógicos solicitados en el examen operando con `MyLinkedList`:
1. Errores de Índices (IndexError / Off-by-one en recorrido de ordenamiento sobre MyLinkedList)
2. Errores de Recursividad (Falta de caso base / partición infinita en Quicksort con MyLinkedList)
3. Errores de Intercambio Incorrecto (Sobrescritura sin variable temporal en nodos de MyLinkedList)
4. Errores de Manejo de Archivos (Falta de cierre, conversión de tipos y carga en MyLinkedList)
5. Errores de Búsquedas Incorrectas (Actualización errónea de límites en Búsqueda Binaria)
"""

import os
import tempfile
from MyLinkedList import MyLinkedList


# =====================================================================
# CASO 1: ERROR DE ÍNDICES (OFF-BY-ONE & DESBORDAMIENTO EN MYLINKEDLIST)
# =====================================================================
CODIGO_DEFECTUOSO_1 = """def burbuja_defectuoso(lista_ll):
    n = len(lista_ll)
    # ERROR 1: range(n) llega hasta i = n-1
    # ERROR 2: range(1, n) hace que lista_ll[j + 1] desborde en j = n - 1 (IndexError)
    # en MyLinkedList._normalize(), además de omitir el índice 0.
    for i in range(n):
        for j in range(1, n):
            if lista_ll[j] > lista_ll[j + 1]:
                lista_ll[j], lista_ll[j + 1] = lista_ll[j + 1], lista_ll[j]
    return lista_ll"""

CODIGO_CORREGIDO_1 = """def burbuja_corregido(lista_ll):
    datos_ll = MyLinkedList(lista_ll)
    n = len(datos_ll)
    # CORRECCIÓN: recorrer desde el nodo head hasta n - 1 - i sin desbordar punteros
    for i in range(n - 1):
        cur = datos_ll.head
        for _ in range(0, n - 1 - i):
            if cur.data > cur.next.data:
                cur.data, cur.next.data = cur.next.data, cur.data
            cur = cur.next
    return datos_ll"""


def probar_caso_1_indices(muestra=None):
    if muestra is None:
        muestra = MyLinkedList([45, 12, 89, 7, 33])
    else:
        muestra = MyLinkedList(muestra)

    error_capturado = None
    try:
        datos_err = MyLinkedList(muestra)
        n = len(datos_err)
        for _ in range(n):
            for j in range(1, n):
                if datos_err[j] > datos_err[j + 1]:
                    datos_err[j], datos_err[j + 1] = datos_err[j + 1], datos_err[j]
    except Exception as exc:
        error_capturado = f"{type(exc).__name__}: {exc} (en MyLinkedList[j + 1] cuando j = {len(muestra)-1})"

    datos_ok = MyLinkedList(muestra)
    n = len(datos_ok)
    for i in range(n - 1):
        cur = datos_ok.head
        for _ in range(0, n - 1 - i):
            if cur.data > cur.next.data:
                cur.data, cur.next.data = cur.next.data, cur.data
            cur = cur.next

    return {
        "id": 1,
        "categoria": "Errores de Índices en MyLinkedList (Off-by-One / Desbordamiento)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_1,
        "codigo_corregido": CODIGO_CORREGIDO_1,
        "identificacion_error": (
            "El ciclo interno usa `range(1, n)` y evalúa `lista_ll[j + 1]`. "
            "Esto provoca dos errores críticos en `MyLinkedList`: 1) ignora el nodo `head` en la posición `0`, y "
            "2) cuando `j = n - 1`, intenta acceder a `lista_ll[n]`, disparando `IndexError: índice fuera de rango` "
            "en `MyLinkedList._normalize()`."
        ),
        "explicacion_solucion": (
            "Se corrigió el recorrido iniciando en `cur = datos_ll.head` (índice `0`) con límite `range(0, n - 1 - i)`, "
            "garantizando que `cur.next` siempre exista y evitando el desbordamiento de índice."
        ),
        "entrada_prueba": repr(muestra),
        "resultado_defectuoso": error_capturado,
        "resultado_corregido": datos_ok.to_list(),
        "resultado_linked_list": repr(datos_ok),
    }


# =====================================================================
# CASO 2: ERROR DE RECURSIVIDAD (RECURSIÓN INFINITA EN QUICKSORT CON MYLINKEDLIST)
# =====================================================================
CODIGO_DEFECTUOSO_2 = """def quicksort_defectuoso(lista_ll):
    # ERROR 1: Condición base insuficiente (solo verifica lista vacía, no longitud 1)
    if len(lista_ll) == 0:
        return lista_ll
    pivote = lista_ll.head.data
    # ERROR 2: Incluye el propio pivote en 'menores' con '<=' sin separarlo
    # Cuando todos los elementos son iguales o de longitud 1, 'menores' tiene el mismo
    # tamaño que 'lista_ll', causando RecursionError (recursión infinita).
    menores = MyLinkedList([x for x in lista_ll if x <= pivote])
    mayores = MyLinkedList([x for x in lista_ll if x > pivote])
    return quicksort_defectuoso(menores) + quicksort_defectuoso(mayores)"""

CODIGO_CORREGIDO_2 = """def quicksort_corregido(lista_ll):
    # CORRECCIÓN 1: Caso base detiene la recursión cuando len(lista_ll) <= 1
    if len(lista_ll) <= 1:
        return lista_ll
    pivote = lista_ll.head.data
    # CORRECCIÓN 2: Partición en 3 MyLinkedList (<, ==, >) garantiza que las llamadas
    # recursivas siempre reciban sublistas enlazadas estrictamente más pequeñas.
    menores = MyLinkedList()
    iguales = MyLinkedList()
    mayores = MyLinkedList()
    for x in lista_ll:
        if x < pivote: menores.append(x)
        elif x > pivote: mayores.append(x)
        else: iguales.append(x)
    return quicksort_corregido(menores) + iguales + quicksort_corregido(mayores)"""


def probar_caso_2_recursividad(muestra=None):
    if muestra is None:
        muestra = MyLinkedList([50, 20, 50, 10, 30])
    else:
        muestra = MyLinkedList(muestra)

    def _qs_defectuoso_seguro(ll, prof=0):
        if prof > 40:
            raise RecursionError("maximum recursion depth exceeded (MyLinkedList no reduce su tamaño en la partición)")
        if len(ll) == 0:
            return ll
        pivote = ll.head.data
        menores = MyLinkedList([x for x in ll if x <= pivote])
        mayores = MyLinkedList([x for x in ll if x > pivote])
        return _qs_defectuoso_seguro(menores, prof + 1) + _qs_defectuoso_seguro(mayores, prof + 1)

    error_capturado = None
    try:
        _qs_defectuoso_seguro(muestra)
    except Exception as exc:
        error_capturado = f"{type(exc).__name__}: {exc}"

    def _qs_corregido(ll):
        if len(ll) <= 1:
            return ll
        pivote = ll.head.data
        menores = MyLinkedList()
        iguales = MyLinkedList()
        mayores = MyLinkedList()
        for x in ll:
            if x < pivote:
                menores.append(x)
            elif x > pivote:
                mayores.append(x)
            else:
                iguales.append(x)
        return _qs_corregido(menores) + iguales + _qs_corregido(mayores)

    res_ok = _qs_corregido(muestra)
    return {
        "id": 2,
        "categoria": "Errores de Recursividad en MyLinkedList (Caso Base y Progreso Recursivo)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_2,
        "codigo_corregido": CODIGO_CORREGIDO_2,
        "identificacion_error": (
            "El caso base `len(lista_ll) == 0` no detiene listas enlazadas de 1 nodo, y la partición "
            "`x <= pivote` vuelve a insertar al propio `pivote` en la `MyLinkedList` izquierda. "
            "Cuando el pivote es el mayor elemento o hay 1 solo nodo, la `MyLinkedList` no se reduce y "
            "produce `RecursionError`."
        ),
        "explicacion_solucion": (
            "Se estableció el caso base en `if len(lista_ll) <= 1: return lista_ll` y se separó la partición en "
            "tres instancias de `MyLinkedList` (`menores`, `iguales`, `mayores`). Al excluir `iguales` "
            "de las llamadas recursivas, cada nivel reduce estrictamente el número de nodos."
        ),
        "entrada_prueba": repr(muestra),
        "resultado_defectuoso": error_capturado,
        "resultado_corregido": res_ok.to_list(),
        "resultado_linked_list": repr(res_ok),
    }


# =====================================================================
# CASO 3: ERROR DE INTERCAMBIO INCORRECTO EN NODOS DE MYLINKEDLIST
# =====================================================================
CODIGO_DEFECTUOSO_3 = """def seleccion_defectuoso(lista_ll):
    datos_ll = MyLinkedList(lista_ll)
    nodo_i = datos_ll.head
    while nodo_i is not None:
        nodo_min = nodo_i
        nodo_j = nodo_i.next
        while nodo_j is not None:
            if nodo_j.data < nodo_min.data:
                nodo_min = nodo_j
            nodo_j = nodo_j.next
        # ERROR: Intercambio destructivo en Node.data sin variable auxiliar
        # Al asignar nodo_i.data = nodo_min.data, el dato original de nodo_i se pierde.
        nodo_i.data = nodo_min.data
        nodo_min.data = nodo_i.data
        nodo_i = nodo_i.next
    return datos_ll"""

CODIGO_CORREGIDO_3 = """def seleccion_corregido(lista_ll):
    datos_ll = MyLinkedList(lista_ll)
    nodo_i = datos_ll.head
    while nodo_i is not None:
        nodo_min = nodo_i
        nodo_j = nodo_i.next
        while nodo_j is not None:
            if nodo_j.data < nodo_min.data:
                nodo_min = nodo_j
            nodo_j = nodo_j.next
        # CORRECCIÓN: Usar variable temporal 'temp' para intercambiar Node.data
        if nodo_min is not nodo_i:
            temp = nodo_i.data
            nodo_i.data = nodo_min.data
            nodo_min.data = temp
        nodo_i = nodo_i.next
    return datos_ll"""


def probar_caso_3_intercambio(muestra=None):
    if muestra is None:
        muestra = MyLinkedList([90, 25, 60, 10, 40])
    else:
        muestra = MyLinkedList(muestra)

    datos_err = MyLinkedList(muestra)
    nodo_i = datos_err.head
    while nodo_i is not None:
        nodo_min = nodo_i
        nodo_j = nodo_i.next
        while nodo_j is not None:
            if nodo_j.data < nodo_min.data:
                nodo_min = nodo_j
            nodo_j = nodo_j.next
        nodo_i.data = nodo_min.data
        nodo_min.data = nodo_i.data
        nodo_i = nodo_i.next

    datos_ok = MyLinkedList(muestra)
    nodo_i = datos_ok.head
    while nodo_i is not None:
        nodo_min = nodo_i
        nodo_j = nodo_i.next
        while nodo_j is not None:
            if nodo_j.data < nodo_min.data:
                nodo_min = nodo_j
            nodo_j = nodo_j.next
        if nodo_min is not nodo_i:
            temp = nodo_i.data
            nodo_i.data = nodo_min.data
            nodo_min.data = temp
        nodo_i = nodo_i.next

    return {
        "id": 3,
        "categoria": "Errores de Intercambio Incorrecto en Nodos de MyLinkedList",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_3,
        "codigo_corregido": CODIGO_CORREGIDO_3,
        "identificacion_error": (
            "Al hacer `nodo_i.data = nodo_min.data` seguido de `nodo_min.data = nodo_i.data`, la primera instrucción "
            "sobrescribe el atributo `data` del nodo `nodo_i` en `MyLinkedList` antes de respaldarlo. Como resultado, "
            "el valor original se pierde y el mínimo se duplica en todos los nodos."
        ),
        "explicacion_solucion": (
            "Se respaldó `temp = nodo_i.data` antes de sobrescribir `nodo_i.data` (o mediante asignación simultánea "
            "`nodo_i.data, nodo_min.data = nodo_min.data, nodo_i.data`), preservando la integridad de `MyLinkedList`."
        ),
        "entrada_prueba": repr(muestra),
        "resultado_defectuoso": f"Datos corruptos en MyLinkedList: {datos_err.to_list()}",
        "resultado_corregido": datos_ok.to_list(),
        "resultado_linked_list": repr(datos_ok),
    }


# =====================================================================
# CASO 4: ERROR DE MANEJO DE ARCHIVOS AL CARGAR EN MYLINKEDLIST
# =====================================================================
CODIGO_DEFECTUOSO_4 = """def leer_transacciones_defectuoso(ruta):
    # ERROR 1: No usa gestor de contexto 'with', dejando el archivo abierto
    archivo = open(ruta, "r")
    # ERROR 2: Inserta las líneas crudas (str) en MyLinkedList sin convertir a int()
    # Al ordenar cadenas, "1000" queda antes que "25" (orden lexicográfico ASCII)
    datos_ll = MyLinkedList(archivo.readlines())
    return datos_ll"""

CODIGO_CORREGIDO_4 = """def leer_transacciones_corregido(ruta):
    datos_ll = MyLinkedList()
    # CORRECCIÓN 1: Bloque 'with' garantiza el cierre automático del archivo
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            limpia = linea.strip()
            # CORRECCIÓN 2: Ignorar líneas vacías e insertar int en MyLinkedList
            if limpia:
                datos_ll.append(int(limpia))
    return datos_ll"""


def probar_caso_4_archivos():
    lineas_archivo = ["1000\n", "25\n", "\n", "9\n", "300\n"]
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as tmp:
        tmp.writelines(lineas_archivo)
        ruta_tmp = tmp.name

    try:
        f = open(ruta_tmp, "r", encoding="utf-8")
        lex_ll = MyLinkedList([x.strip() for x in f.readlines() if x.strip()])
        f.close()
        # Ordenar MyLinkedList de strings con burbuja de punteros
        n = len(lex_ll)
        for i in range(n - 1):
            cur = lex_ll.head
            for _ in range(n - 1 - i):
                if cur.data > cur.next.data:
                    cur.data, cur.next.data = cur.next.data, cur.data
                cur = cur.next

        datos_ok = MyLinkedList()
        with open(ruta_tmp, "r", encoding="utf-8") as arch:
            for linea in arch:
                limpia = linea.strip()
                if limpia:
                    datos_ok.append(int(limpia))
        n_ok = len(datos_ok)
        for i in range(n_ok - 1):
            cur = datos_ok.head
            for _ in range(n_ok - 1 - i):
                if cur.data > cur.next.data:
                    cur.data, cur.next.data = cur.next.data, cur.data
                cur = cur.next
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)

    return {
        "id": 4,
        "categoria": "Errores de Manejo de Archivos al Poblar MyLinkedList",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_4,
        "codigo_corregido": CODIGO_CORREGIDO_4,
        "identificacion_error": (
            "1) Abre el archivo sin bloque `with` ni `.close()`. "
            "2) No elimina saltos de línea (`.strip()`) ni filtra líneas vacías. "
            "3) Inserta cadenas (`str`) en los nodos de `MyLinkedList`, causando ordenamiento lexicográfico ASCII "
            "(`'1000' < '25' < '300' < '9'`) en lugar de numérico."
        ),
        "explicacion_solucion": (
            "Se implementó `with open(..., encoding='utf-8')`, se limpió cada línea con `.strip()`, se descartaron "
            "líneas vacías y se insertó cada valor con `datos_ll.append(int(limpia))` en `MyLinkedList`."
        ),
        "entrada_prueba": "['1000', '25', '', '9', '300']",
        "resultado_defectuoso": f"Orden lexicográfico incorrecto en MyLinkedList: {lex_ll.to_list()}",
        "resultado_corregido": datos_ok.to_list(),
        "resultado_linked_list": repr(datos_ok),
    }


# =====================================================================
# CASO 5: ERROR DE BÚSQUEDA INCORRECTA SOBRE MYLINKEDLIST
# =====================================================================
CODIGO_DEFECTUOSO_5 = """def busqueda_binaria_defectuosa(lista_ll, objetivo):
    izq = 0
    der = len(lista_ll) - 1
    # ERROR 1: Usa '<' en vez de '<=', por lo que falla cuando izq == der (último nodo)
    while izq < der:
        medio = (izq + der) // 2
        if lista_ll[medio] == objetivo:
            return medio
        elif lista_ll[medio] < objetivo:
            # ERROR 2: Asigna izq = medio (sin +1). Cuando izq + 1 == der,
            # medio == izq, causando un ciclo infinito.
            izq = medio
        else:
            der = medio
    return -1"""

CODIGO_CORREGIDO_5 = """def busqueda_binaria_corregida(lista_ll, objetivo):
    izq = 0
    der = len(lista_ll) - 1
    # CORRECCIÓN 1: Condición 'izq <= der' evalúa incluso cuando queda 1 solo nodo
    while izq <= der:
        medio = (izq + der) // 2
        val_medio = lista_ll[medio]
        if val_medio == objetivo:
            return medio
        elif val_medio < objetivo:
            # CORRECCIÓN 2: Descartar 'medio' usando medio + 1 y medio - 1
            izq = medio + 1
        else:
            der = medio - 1
    return -1"""


def probar_caso_5_busquedas():
    muestra = MyLinkedList([10, 25, 40, 55, 70, 85, 100])
    objetivo = 100

    izq = 0
    der = len(muestra) - 1
    pasos = 0
    fallo_detectado = None
    while izq < der:
        pasos += 1
        if pasos > 25:
            fallo_detectado = (
                f"Ciclo infinito detectado tras {pasos} iteraciones sobre MyLinkedList "
                f"(izq={izq}, der={der}, medio={(izq+der)//2} no avanza hacia {objetivo})"
            )
            break
        medio = (izq + der) // 2
        if muestra[medio] == objetivo:
            break
        elif muestra[medio] < objetivo:
            izq = medio
        else:
            der = medio

    izq = 0
    der = len(muestra) - 1
    idx_ok = -1
    while izq <= der:
        medio = (izq + der) // 2
        val_medio = muestra[medio]
        if val_medio == objetivo:
            idx_ok = medio
            break
        elif val_medio < objetivo:
            izq = medio + 1
        else:
            der = medio - 1

    return {
        "id": 5,
        "categoria": "Errores en Búsquedas sobre MyLinkedList (Ciclo Infinito en Binaria)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_5,
        "codigo_corregido": CODIGO_CORREGIDO_5,
        "identificacion_error": (
            "1) La condición `while izq < der` omite la verificación cuando `izq == der`. "
            "2) Al actualizar `izq = medio` en lugar de `izq = medio + 1`, cuando `der == izq + 1` la división "
            "`(izq + der) // 2` siempre devuelve `izq`, estancando la búsqueda sobre `MyLinkedList` en un ciclo infinito."
        ),
        "explicacion_solucion": (
            "Se cambió la condición del ciclo a `while izq <= der:` y se actualizaron los límites excluyendo "
            "la posición media ya evaluada (`izq = medio + 1` y `der = medio - 1`), logrando convergencia en O(log n)."
        ),
        "entrada_prueba": f"{repr(muestra)}, Objetivo={objetivo}",
        "resultado_defectuoso": fallo_detectado,
        "resultado_corregido": f"Valor {objetivo} encontrado exitosamente en el nodo índice {idx_ok}",
    }


def ejecutar_todos_los_casos_defectuosos():
    """Ejecuta y devuelve el reporte completo de los 5 casos de código defectuoso con MyLinkedList."""
    return [
        probar_caso_1_indices(),
        probar_caso_2_recursividad(),
        probar_caso_3_intercambio(),
        probar_caso_4_archivos(),
        probar_caso_5_busquedas(),
    ]
