"""
Librería de Diagnóstico y Corrección de Código Defectuoso (Requerimiento 4 del Examen Parcial).
Incluye los 5 casos de errores lógicos solicitados en el examen:
1. Errores de Índices (IndexError / Off-by-one en recorrido de ordenamiento)
2. Errores de Recursividad (Falta de caso base / partición infinita en Quicksort)
3. Errores de Intercambio Incorrecto (Sobrescritura sin variable temporal / pérdida de datos)
4. Errores de Manejo de Archivos (Falta de cierre, conversión de tipos y líneas vacías)
5. Errores de Búsquedas Incorrectas (Actualización errónea de límites en Búsqueda Binaria)

Cada caso expone:
- El fragmento de código defectuoso original
- La identificación exacta de la falla técnica
- El código corregido funcional
- La explicación técnica breve y una prueba comparativa en vivo.
"""

import os
import tempfile


# =====================================================================
# CASO 1: ERROR DE ÍNDICES (OFF-BY-ONE & DESBORDAMIENTO EN BURBUJA)
# =====================================================================
CODIGO_DEFECTUOSO_1 = """def burbuja_defectuoso(lista):
    n = len(lista)
    # ERROR 1: range(n) llega hasta i = n-1
    # ERROR 2: range(1, n) hace que lista[j + 1] desborde en j = n - 1 (IndexError)
    # además de omitir el índice 0 (el primer elemento nunca se ordena).
    for i in range(n):
        for j in range(1, n):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista"""

CODIGO_CORREGIDO_1 = """def burbuja_corregido(lista):
    datos = lista[:]
    n = len(datos)
    # CORRECCIÓN: iniciar en j = 0 y limitar hasta n - 1 - i
    # Así j + 1 nunca excede n - 1 y se incluye el índice 0.
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if datos[j] > datos[j + 1]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
    return datos"""


def probar_caso_1_indices(muestra=None):
    if muestra is None:
        muestra = [45, 12, 89, 7, 33]

    # Simular fallo del código defectuoso capturando la excepción real
    error_capturado = None
    try:
        datos_err = muestra[:]
        n = len(datos_err)
        for _ in range(n):
            for j in range(1, n):
                if datos_err[j] > datos_err[j + 1]:
                    datos_err[j], datos_err[j + 1] = datos_err[j + 1], datos_err[j]
    except Exception as exc:
        error_capturado = f"{type(exc).__name__}: {exc} (al evaluar lista[j + 1] cuando j = {len(muestra)-1})"

    # Ejecutar versión corregida
    datos_ok = muestra[:]
    n = len(datos_ok)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if datos_ok[j] > datos_ok[j + 1]:
                datos_ok[j], datos_ok[j + 1] = datos_ok[j + 1], datos_ok[j]

    return {
        "id": 1,
        "categoria": "Errores de Índices (Off-by-One / Desbordamiento)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_1,
        "codigo_corregido": CODIGO_CORREGIDO_1,
        "identificacion_error": (
            "El ciclo interno usa `range(1, n)` y evalúa `lista[j + 1]`. "
            "Esto provoca dos errores críticos: 1) ignora el elemento en la posición `0`, y "
            "2) cuando `j = n - 1`, intenta acceder a `lista[n]`, lanzando `IndexError: list index out of range`."
        ),
        "explicacion_solucion": (
            "Se corrigió el rango del ciclo interno a `range(0, n - 1 - i)`. "
            "De esta forma se evalúa desde el primer índice (`0`) y el límite superior `n - 1 - i` garantiza "
            "que `j + 1` llegue como máximo a `n - 1`, evitando el desbordamiento y optimizando las pasadas."
        ),
        "entrada_prueba": muestra,
        "resultado_defectuoso": error_capturado,
        "resultado_corregido": datos_ok,
    }


# =====================================================================
# CASO 2: ERROR DE RECURSIVIDAD (RECURSIÓN INFINITA EN QUICKSORT)
# =====================================================================
CODIGO_DEFECTUOSO_2 = """def quicksort_defectuoso(lista):
    # ERROR 1: Condición base insuficiente (solo verifica lista vacía, no longitud 1)
    if len(lista) == 0:
        return lista
    pivote = lista[0]
    # ERROR 2: Incluye el propio pivote en 'menores_iguales' con '<=' sin separarlo
    # Cuando todos los elementos son iguales o de longitud 1, 'menores' tiene el mismo
    # tamaño que 'lista', causando RecursionError (recursión infinita).
    menores = [x for x in lista if x <= pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort_defectuoso(menores) + quicksort_defectuoso(mayores)"""

CODIGO_CORREGIDO_2 = """def quicksort_corregido(lista):
    # CORRECCIÓN 1: Caso base detiene la recursión cuando len(lista) <= 1
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    # CORRECCIÓN 2: Partición tripartita (<, ==, >) garantiza que las llamadas
    # recursivas siempre reciban sublistas estrictamente más pequeñas.
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort_corregido(menores) + iguales + quicksort_corregido(mayores)"""


def probar_caso_2_recursividad(muestra=None):
    if muestra is None:
        muestra = [50, 20, 50, 10, 30]

    # Simular con contador de profundidad para no colgar el intérprete y evidenciar el RecursionError
    def _qs_defectuoso_seguro(lst, prof=0):
        if prof > 40:
            raise RecursionError("maximum recursion depth exceeded (partición no reduce el tamaño de la lista)")
        if len(lst) == 0:
            return lst
        pivote = lst[0]
        menores = [x for x in lst if x <= pivote]
        mayores = [x for x in lst if x > pivote]
        return _qs_defectuoso_seguro(menores, prof + 1) + _qs_defectuoso_seguro(mayores, prof + 1)

    error_capturado = None
    try:
        _qs_defectuoso_seguro(muestra)
    except Exception as exc:
        error_capturado = f"{type(exc).__name__}: {exc}"

    def _qs_corregido(lst):
        if len(lst) <= 1:
            return lst
        pivote = lst[len(lst) // 2]
        menores = [x for x in lst if x < pivote]
        iguales = [x for x in lst if x == pivote]
        mayores = [x for x in lst if x > pivote]
        return _qs_corregido(menores) + iguales + _qs_corregido(mayores)

    return {
        "id": 2,
        "categoria": "Errores de Recursividad (Caso Base y Progreso Recursivo)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_2,
        "codigo_corregido": CODIGO_CORREGIDO_2,
        "identificacion_error": (
            "El caso base `len(lista) == 0` no detiene listas de 1 elemento, y la comprensión "
            "`[x for x in lista if x <= pivote]` vuelve a incluir al propio pivote en la sublista izquierda. "
            "Cuando el pivote es el mayor elemento o la lista tiene 1 elemento, la sublista no se reduce y "
            "produce `RecursionError` (desbordamiento de pila)."
        ),
        "explicacion_solucion": (
            "Se estableció el caso base en `if len(lista) <= 1: return lista` y se separó la partición en "
            "tres listas (`menores < pivote`, `iguales == pivote`, `mayores > pivote`). Al excluir `iguales` "
            "de las llamadas recursivas, cada nivel reduce estrictamente el tamaño del problema."
        ),
        "entrada_prueba": muestra,
        "resultado_defectuoso": error_capturado,
        "resultado_corregido": _qs_corregido(muestra),
    }


# =====================================================================
# CASO 3: ERROR DE INTERCAMBIO INCORRECTO (PÉRDIDA DE VALOR EN SELECCIÓN)
# =====================================================================
CODIGO_DEFECTUOSO_3 = """def seleccion_defectuoso(lista):
    datos = lista[:]
    n = len(datos)
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if datos[j] < datos[idx_min]:
                idx_min = j
        # ERROR: Intercambio destructivo sin variable auxiliar ni desempaquetado
        # Al asignar datos[i] = datos[idx_min], el valor original de datos[i] se pierde
        # y luego datos[idx_min] recibe el mismo valor duplicado.
        datos[i] = datos[idx_min]
        datos[idx_min] = datos[i]
    return datos"""

CODIGO_CORREGIDO_3 = """def seleccion_corregido(lista):
    datos = lista[:]
    n = len(datos)
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if datos[j] < datos[idx_min]:
                idx_min = j
        # CORRECCIÓN: Usar variable temporal (o asignación simultánea de tuplas)
        if idx_min != i:
            temp = datos[i]
            datos[i] = datos[idx_min]
            datos[idx_min] = temp
    return datos"""


def probar_caso_3_intercambio(muestra=None):
    if muestra is None:
        muestra = [90, 25, 60, 10, 40]

    # Ejecutar versión defectuosa (corrompe y duplica los valores menores)
    datos_err = muestra[:]
    n = len(datos_err)
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if datos_err[j] < datos_err[idx_min]:
                idx_min = j
        datos_err[i] = datos_err[idx_min]
        datos_err[idx_min] = datos_err[i]

    # Ejecutar versión corregida
    datos_ok = muestra[:]
    for i in range(n - 1):
        idx_min = i
        for j in range(i + 1, n):
            if datos_ok[j] < datos_ok[idx_min]:
                idx_min = j
        if idx_min != i:
            temp = datos_ok[i]
            datos_ok[i] = datos_ok[idx_min]
            datos_ok[idx_min] = temp

    return {
        "id": 3,
        "categoria": "Errores de Intercambio Incorrecto (Sobrescritura de Memoria)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_3,
        "codigo_corregido": CODIGO_CORREGIDO_3,
        "identificacion_error": (
            "Al hacer `datos[i] = datos[idx_min]` seguido de `datos[idx_min] = datos[i]`, la primera instrucción "
            "sobrescribe el valor original de `datos[i]` antes de respaldarlo. Como resultado, el valor original "
            "desaparece del arreglo y el valor mínimo se clona en ambas posiciones."
        ),
        "explicacion_solucion": (
            "Se respaldó el valor `temp = datos[i]` antes de sobrescribir `datos[i]`, o bien se emplea "
            "desempaquetado de tuplas `datos[i], datos[idx_min] = datos[idx_min], datos[i]`, preservando la "
            "integridad de todos los registros financieros."
        ),
        "entrada_prueba": muestra,
        "resultado_defectuoso": f"Datos corruptos (duplicados y pérdida de valores): {datos_err}",
        "resultado_corregido": datos_ok,
    }


# =====================================================================
# CASO 4: ERROR DE MANEJO DE ARCHIVOS (TIPOS STRING Y FALTA DE CIERRE/STRIP)
# =====================================================================
CODIGO_DEFECTUOSO_4 = """def leer_transacciones_defectuoso(ruta):
    # ERROR 1: No usa gestor de contexto 'with', dejando el descriptor de archivo abierto
    archivo = open(ruta, "r")
    # ERROR 2: Lee las líneas como cadenas (str) con '\\n' sin convertir a int()
    # Al ordenar cadenas, "1000" queda antes que "25" (orden lexicográfico ASCII, no numérico)
    # y tampoco filtra líneas vacías.
    datos = archivo.readlines()
    return datos"""

CODIGO_CORREGIDO_4 = """def leer_transacciones_corregido(ruta):
    datos = []
    # CORRECCIÓN 1: Bloque 'with' garantiza el cierre automático del archivo
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            limpia = linea.strip()
            # CORRECCIÓN 2: Ignorar líneas vacías y convertir explícitamente a int
            if limpia:
                datos.append(int(limpia))
    return datos"""


def probar_caso_4_archivos():
    lineas_archivo = ["1000\n", "25\n", "\n", "9\n", "300\n"]
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as tmp:
        tmp.writelines(lineas_archivo)
        ruta_tmp = tmp.name

    try:
        # Defectuoso: lee strings y al compararlos lexicográficamente produce orden erróneo
        f = open(ruta_tmp, "r", encoding="utf-8")
        crudos = [x.strip() for x in f.readlines() if x.strip()]
        f.close()
        # Ordenamiento burbuja sobre strings (simula el efecto de no convertir a int)
        lex = crudos[:]
        for i in range(len(lex) - 1):
            for j in range(len(lex) - 1 - i):
                if lex[j] > lex[j + 1]:
                    lex[j], lex[j + 1] = lex[j + 1], lex[j]

        # Corregido: convierte a int y cierra con with
        datos_ok = []
        with open(ruta_tmp, "r", encoding="utf-8") as arch:
            for linea in arch:
                limpia = linea.strip()
                if limpia:
                    datos_ok.append(int(limpia))
        for i in range(len(datos_ok) - 1):
            for j in range(len(datos_ok) - 1 - i):
                if datos_ok[j] > datos_ok[j + 1]:
                    datos_ok[j], datos_ok[j + 1] = datos_ok[j + 1], datos_ok[j]
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)

    return {
        "id": 4,
        "categoria": "Errores de Manejo de Archivos (Conversión de Tipos y Recursos)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_4,
        "codigo_corregido": CODIGO_CORREGIDO_4,
        "identificacion_error": (
            "1) Abre el archivo sin bloque `with` ni `.close()`, provocando fugas de descriptores de archivo. "
            "2) No elimina saltos de línea (`.strip()`) ni filtra líneas en blanco. "
            "3) Mantiene los datos como cadenas (`str`), causando que el ordenamiento sea lexicográfico ASCII "
            "(`'1000' < '25' < '300' < '9'`) en lugar de numérico."
        ),
        "explicacion_solucion": (
            "Se implementó el administrador de contexto `with open(..., encoding='utf-8')`, se limpió cada "
            "línea con `.strip()`, se descartaron líneas vacías y se convirtió cada registro a `int()`."
        ),
        "entrada_prueba": ["1000", "25", "", "9", "300"],
        "resultado_defectuoso": f"Orden lexicográfico incorrecto sobre strings: {lex}",
        "resultado_corregido": datos_ok,
    }


# =====================================================================
# CASO 5: ERROR DE BÚSQUEDA INCORRECTA (CICLO INFINITO Y LÍMITES EN BINARIA)
# =====================================================================
CODIGO_DEFECTUOSO_5 = """def busqueda_binaria_defectuosa(lista, objetivo):
    izq = 0
    der = len(lista) - 1
    # ERROR 1: Usa '<' en vez de '<=', por lo que falla cuando izq == der (último elemento)
    while izq < der:
        medio = (izq + der) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            # ERROR 2: Asigna izq = medio (sin +1) e invierte o estanca los punteros.
            # Cuando izq + 1 == der, medio == izq, causando un ciclo infinito.
            izq = medio
        else:
            der = medio
    return -1"""

CODIGO_CORREGIDO_5 = """def busqueda_binaria_corregida(lista, objetivo):
    izq = 0
    der = len(lista) - 1
    # CORRECCIÓN 1: Condición 'izq <= der' evalúa incluso cuando queda 1 solo elemento
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            # CORRECCIÓN 2: Descartar 'medio' usando medio + 1 y medio - 1
            izq = medio + 1
        else:
            der = medio - 1
    return -1"""


def probar_caso_5_busquedas():
    muestra = [10, 25, 40, 55, 70, 85, 100]
    objetivo = 100

    # Simular búsqueda defectuosa con límite de iteraciones para evidenciar el ciclo infinito
    izq = 0
    der = len(muestra) - 1
    pasos = 0
    fallo_detectado = None
    while izq < der:
        pasos += 1
        if pasos > 25:
            fallo_detectado = (
                f"Ciclo infinito detectado tras {pasos} iteraciones "
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

    # Ejecutar búsqueda corregida
    izq = 0
    der = len(muestra) - 1
    idx_ok = -1
    while izq <= der:
        medio = (izq + der) // 2
        if muestra[medio] == objetivo:
            idx_ok = medio
            break
        elif muestra[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1

    return {
        "id": 5,
        "categoria": "Errores en Búsquedas (Ciclo Infinito y Exclusión de Extremos en Binaria)",
        "codigo_defectuoso": CODIGO_DEFECTUOSO_5,
        "codigo_corregido": CODIGO_CORREGIDO_5,
        "identificacion_error": (
            "1) La condición `while izq < der` omite la verificación cuando `izq == der`. "
            "2) Al actualizar `izq = medio` en lugar de `izq = medio + 1`, la división entera `(izq + der) // 2` "
            "cuando `der == izq + 1` siempre devuelve `izq`, dejando los punteros estancados en un ciclo infinito "
            "al buscar el último elemento (`100`) o un valor inexistente."
        ),
        "explicacion_solucion": (
            "Se cambió la condición del ciclo a `while izq <= der:` y se actualizaron los límites excluyendo "
            "la posición media ya evaluada (`izq = medio + 1` y `der = medio - 1`), garantizando convergencia "
            "en O(log n)."
        ),
        "entrada_prueba": f"Lista={muestra}, Objetivo={objetivo}",
        "resultado_defectuoso": fallo_detectado,
        "resultado_corregido": f"Valor {objetivo} encontrado exitosamente en el índice {idx_ok}",
    }


def ejecutar_todos_los_casos_defectuosos():
    """Ejecuta y devuelve el reporte completo de los 5 casos de código defectuoso."""
    return [
        probar_caso_1_indices(),
        probar_caso_2_recursividad(),
        probar_caso_3_intercambio(),
        probar_caso_4_archivos(),
        probar_caso_5_busquedas(),
    ]
