"""
SISTEMA DE PROCESAMIENTO Y ORDENAMIENTO MASIVO DE DATOS
Examen Parcial — Algoritmos de Ordenamiento y Búsqueda
Materia: Estructura de Datos
Alumno: Emiliano Cab Martínez

Consola Interactiva Principal (CLI).
Permite ejecutar en vivo todos los requerimientos del Examen Parcial:
A) Cargar archivo (Seleccionar TXT o XLSX de 1,000 o 5,000 números enteros, o ruta personalizada)
B) Ordenar datos (Elegir algoritmo interno o externo y orden Ascendente / Descendente)
C) Buscar un valor (Usando Búsqueda Secuencial, Binaria o Tabla Hash)
D) Mostrar resultados (Primeros 20 elementos, últimos 20 elementos, total de registros)
E) Exportar resultados (Guardar archivo ordenado TXT/XLSX, tiempo de ejecución, algoritmo utilizado)
F) Corrección de código defectuoso (Demostración interactiva de los 5 casos: índices, recursividad, intercambio, archivos, búsquedas)
G) Comparación de escenarios y Benchmark completo de todos los algoritmos
"""

import os
import sys

from librerias import (
    CATALOGO_INTERNOS,
    CATALOGO_EXTERNOS,
    TablaHashTransacciones,
    busqueda_secuencial,
    busqueda_binaria,
    generar_datasets_financieros,
    cargar_archivo_datos,
    obtener_resumen_resultados,
    exportar_resultados,
    ejecutar_todos_los_casos_defectuosos,
    TABLA_COMPARACION_ESCENARIOS,
    ejecutar_benchmark_ordenamientos,
    ejecutar_benchmark_busquedas,
)


def linea_decorativa(char="=", ancho=88):
    print(char * ancho)


def encabezado(titulo):
    print()
    linea_decorativa("=")
    print(f"  {titulo}")
    linea_decorativa("=")


def mostrar_resumen_20(titulo, lista):
    """Muestra primeros 20 elementos, últimos 20 elementos y total de registros (Requerimiento 5D)."""
    res = obtener_resumen_resultados(lista)
    print(f"\n--- {titulo} ---")
    print(f"  Total de registros : {res['total_registros']:,}")
    print(f"  Valor mínimo       : {res['minimo']:,}")
    print(f"  Valor máximo       : {res['maximo']:,}")
    print(f"  Promedio           : {res['promedio']:,.2f}")
    print(f"  Primeros 20 elementos:\n    {res['primeros_20']}")
    print(f"  Últimos 20 elementos:\n    {res['ultimos_20']}")


def menu_cargar_archivo(archivos_base):
    encabezado("A) CARGAR ARCHIVO DE TRANSACCIONES FINANCIERAS (TXT / XLSX)")
    print("  1. Cargar archivo de 1,000 números enteros en formato TXT  (datos/transacciones_1000.txt)")
    print("  2. Cargar archivo de 1,000 números enteros en formato XLSX (datos/transacciones_1000.xlsx)")
    print("  3. Cargar archivo de 5,000 números enteros en formato TXT  (datos/transacciones_5000.txt)")
    print("  4. Cargar archivo de 5,000 números enteros en formato XLSX (datos/transacciones_5000.xlsx)")
    print("  5. Ingresar ruta personalizada de archivo (.txt o .xlsx)")
    print("  6. Regenerar datasets financieros aleatorios")
    opcion = input("\n  Selecciona una opción (1-6): ").strip()

    mapa = {
        "1": archivos_base["txt_1000"],
        "2": archivos_base["xlsx_1000"],
        "3": archivos_base["txt_5000"],
        "4": archivos_base["xlsx_5000"],
    }

    if opcion in mapa:
        info = cargar_archivo_datos(mapa[opcion])
    elif opcion == "5":
        ruta = input("  Ingresa la ruta del archivo (.txt o .xlsx): ").strip().strip('"')
        info = cargar_archivo_datos(ruta)
    elif opcion == "6":
        sem = input("  Ingresa semilla numérica (Enter para 42): ").strip()
        semilla = int(sem) if sem.isdigit() else 42
        nuevos = generar_datasets_financieros("datos", semilla=semilla)
        archivos_base.update(nuevos)
        print("  [+] Datasets de 1,000 y 5,000 registros regenerados exitosamente en TXT y XLSX.")
        info = cargar_archivo_datos(archivos_base["txt_1000"])
    else:
        print("  [!] Opción no válida. Cargando por defecto 1,000 registros TXT.")
        info = cargar_archivo_datos(archivos_base["txt_1000"])

    print(f"\n  [OK] Archivo cargado : {info['nombre_archivo']} (Formato: {info['formato']})")
    print(f"  [OK] Total registros : {info['total_registros']:,} números enteros")
    print(f"  [OK] Tiempo de carga : {info['tiempo_lectura_ms']:.4f} ms")
    mostrar_resumen_20("Vista Previa de Datos Cargados (Sin Ordenar)", info["datos"])
    return info


def menu_ordenar_datos(estado):
    encabezado("B) ORDENAR DATOS (INTERNOS Y EXTERNOS - LIBRERÍAS PROPIAS)")
    print("  --- ORDENAMIENTOS INTERNOS (En Memoria RAM - ADA1 / ADA2) ---")
    print("   1. Burbuja (Bubble Sort)            [O(n²)]")
    print("   2. Inserción (Insertion Sort)       [O(n²) / O(n) adaptativo]")
    print("   3. Selección (Selection Sort)       [O(n²)]")
    print("   4. ShellSort                        [O(n log² n)]")
    print("   5. Quicksort                        [O(n log n)]")
    print("   6. Heapsort                         [O(n log n)]")
    print("   7. Radix Sort (LSD)                 [O(d · n)]")
    print("\n  --- ORDENAMIENTOS EXTERNOS (Archivos Auxiliares / Corridas - MetOrdena) ---")
    print("   8. Intercalación (External Merge)   [O(n log n)]")
    print("   9. Mezcla Directa (Direct Merge)    [O(n log n) - Auxiliares F1 y F2]")
    print("  10. Mezcla Equilibrada (Natural)     [O(n log n) - Corridas Naturales F1 y F2]")

    op_alg = input("\n  Elige el algoritmo (1-10): ").strip()
    mapa_alg = {
        "1": ("interno", "burbuja"),
        "2": ("interno", "insercion"),
        "3": ("interno", "seleccion"),
        "4": ("interno", "shellsort"),
        "5": ("interno", "quicksort"),
        "6": ("interno", "heapsort"),
        "7": ("interno", "radix"),
        "8": ("externo", "intercalacion"),
        "9": ("externo", "mezcla_directa"),
        "10": ("externo", "mezcla_equilibrada"),
    }

    if op_alg not in mapa_alg:
        print("  [!] Opción inválida. Se utilizará Quicksort por defecto.")
        categoria, clave = ("interno", "quicksort")
    else:
        categoria, clave = mapa_alg[op_alg]

    print("\n  Selecciona el orden:")
    print("   1. Ascendente  (Menor a Mayor)")
    print("   2. Descendente (Mayor a Menor)")
    op_ord = input("  Orden (1-2, Enter=1): ").strip()
    ascendente = op_ord != "2"

    datos_origen = estado["datos_originales"]
    if categoria == "interno":
        _, funcion = CATALOGO_INTERNOS[clave]
        res = funcion(datos_origen, ascendente=ascendente, retornar_metricas=True)
    else:
        _, funcion = CATALOGO_EXTERNOS[clave]
        if clave in ("mezcla_directa", "mezcla_equilibrada"):
            res = funcion(
                datos_origen,
                ascendente=ascendente,
                retornar_metricas=True,
                dir_auxiliar=os.path.join("resultados", "auxiliares_externos"),
            )
        else:
            res = funcion(datos_origen, ascendente=ascendente, retornar_metricas=True)

    estado["datos_actuales"] = res["datos"]
    estado["esta_ordenado"] = True
    estado["ascendente"] = ascendente
    estado["ultimo_ordenamiento"] = res
    # Actualizar tabla hash sobre los datos ordenados para búsquedas inmediatas
    cap = 2003 if len(res["datos"]) <= 2000 else 10007
    estado["tabla_hash"] = TablaHashTransacciones(capacidad=cap).construir_desde_lista(res["datos"])

    print("\n  ======================================================================")
    print(f"  [OK] ORDENAMIENTO COMPLETADO EXITOSAMENTE")
    print("  ======================================================================")
    print(f"  Algoritmo ejecutado  : {res['algoritmo']} ({res['tipo']})")
    print(f"  Complejidad teórica  : {res['complejidad']}")
    print(f"  Sentido del orden    : {res['orden']}")
    print(f"  Tiempo de ejecución  : {res['tiempo_seg']:.6f} s ({res['tiempo_ms']:.4f} ms)")
    print(f"  Comparaciones        : {res['comparaciones']:,}")
    print(f"  Intercambios / Movs  : {res['intercambios']:,}")
    if "pasadas_externas" in res:
        print(f"  Pasadas externas     : {res['pasadas_externas']}")
    if res.get("archivos_auxiliares"):
        print(f"  Auxiliares en disco  : {', '.join(res['archivos_auxiliares'])}")
    print(f"  Verificación O(n)    : {'CORRECTO (100% Ordenado)' if res['verificado'] else 'ERROR'}")

    mostrar_resumen_20(f"Resultados Ordenados ({res['algoritmo']} - {res['orden']})", res["datos"])


def menu_buscar_valor(estado):
    encabezado("C) BUSCAR UN VALOR (SECUENCIAL, BINARIA O TABLA HASH)")
    print("  1. Búsqueda Secuencial (Lineal)           [O(n)]")
    print("  2. Búsqueda Binaria (Dicotómica)          [O(log n) - Requiere datos ordenados]")
    print("  3. Búsqueda por Tabla Hash                [O(1) promedio]")
    print("  4. Comparar los 3 métodos simultáneamente [Secuencial vs Binaria vs Hash]")

    op_busq = input("\n  Selecciona el método de búsqueda (1-4): ").strip()

    # Mostrar sugerencias de valores reales presentes en el archivo cargado
    muestra_valores = [
        estado["datos_actuales"][0],
        estado["datos_actuales"][len(estado["datos_actuales"]) // 2],
        estado["datos_actuales"][-1],
    ]
    print(f"  (Sugerencia de valores existentes en el dataset actual: {muestra_valores})")
    val_str = input("  Ingresa el número entero a buscar: ").strip()
    try:
        objetivo = int(val_str)
    except ValueError:
        objetivo = muestra_valores[1]
        print(f"  [!] Entrada no numérica. Buscando valor de muestra: {objetivo}")

    if op_busq in ("2", "4") and not estado["esta_ordenado"]:
        print("  [*] Nota: La Búsqueda Binaria requiere datos ordenados. Ordenando automáticamente con Quicksort...")
        _, fn_qs = CATALOGO_INTERNOS["quicksort"]
        res_ord = fn_qs(estado["datos_originales"], ascendente=True, retornar_metricas=True)
        estado["datos_actuales"] = res_ord["datos"]
        estado["esta_ordenado"] = True
        estado["ascendente"] = True
        estado["ultimo_ordenamiento"] = res_ord
        cap = 2003 if len(res_ord["datos"]) <= 2000 else 10007
        estado["tabla_hash"] = TablaHashTransacciones(capacidad=cap).construir_desde_lista(res_ord["datos"])

    resultados = []
    if op_busq == "1":
        resultados.append(busqueda_secuencial(estado["datos_actuales"], objetivo))
    elif op_busq == "2":
        resultados.append(busqueda_binaria(estado["datos_actuales"], objetivo, ascendente=estado["ascendente"]))
    elif op_busq == "3":
        if estado["tabla_hash"] is None:
            cap = 2003 if len(estado["datos_actuales"]) <= 2000 else 10007
            estado["tabla_hash"] = TablaHashTransacciones(capacidad=cap).construir_desde_lista(estado["datos_actuales"])
        resultados.append(estado["tabla_hash"].buscar(objetivo))
    else:
        resultados = ejecutar_benchmark_busquedas(estado["datos_actuales"], objetivo, ascendente=estado["ascendente"])

    for r in resultados:
        print("\n  ----------------------------------------------------------------------")
        print(f"  Método               : {r['metodo']} ({r['complejidad']})")
        print(f"  Valor buscado        : {r['objetivo']:,}")
        print(f"  Estado               : {'ENCONTRADO' if r['encontrado'] else 'NO ENCONTRADO'}")
        if r["encontrado"]:
            print(f"  Primera posición     : Índice {r['indice_primero']}")
            print(f"  Total apariciones    : {r['total_apariciones']} -> Índices: {r['todas_posiciones'][:15]}")
        print(f"  Comparaciones        : {r['comparaciones']:,}")
        print(f"  Tiempo de búsqueda   : {r['tiempo_seg']:.8f} s ({r['tiempo_ms']:.5f} ms)")
        if "cubeta_hash" in r:
            print(f"  Cubeta Hash asignada : #{r['cubeta_hash']} (Factor de carga: {r['factor_carga']})")


def menu_exportar_resultados(estado):
    encabezado("E) EXPORTAR RESULTADOS (ARCHIVO ORDENADO, TIEMPO Y ALGORITMO)")
    if not estado["esta_ordenado"] or estado["ultimo_ordenamiento"] is None:
        print("  [*] Los datos aún no han sido ordenados en esta sesión. Ordenando con Quicksort antes de exportar...")
        _, fn_qs = CATALOGO_INTERNOS["quicksort"]
        res_ord = fn_qs(estado["datos_originales"], ascendente=True, retornar_metricas=True)
        estado["datos_actuales"] = res_ord["datos"]
        estado["esta_ordenado"] = True
        estado["ascendente"] = True
        estado["ultimo_ordenamiento"] = res_ord

    info_ord = estado["ultimo_ordenamiento"]
    print("  Selecciona el formato de exportación:")
    print("   1. Exportar a TXT")
    print("   2. Exportar a XLSX (Excel con hoja de Metadatos + hoja de Datos Ordenados)")
    print("   3. Exportar a AMBOS formatos (TXT y XLSX)")
    op_fmt = input("  Formato (1-3, Enter=3): ").strip()
    fmt = "TXT" if op_fmt == "1" else ("XLSX" if op_fmt == "2" else "AMBOS")

    rutas = exportar_resultados(
        datos_ordenados=estado["datos_actuales"],
        algoritmo_utilizado=info_ord["algoritmo"],
        tiempo_ejecucion_seg=info_ord["tiempo_seg"],
        orden=info_ord["orden"],
        comparaciones=info_ord["comparaciones"],
        intercambios=info_ord["intercambios"],
        archivo_origen=estado["info_archivo"]["nombre_archivo"],
        directorio_salida="resultados",
        formato=fmt,
    )

    print("\n  [OK] Exportación finalizada con éxito:")
    for tipo_fmt, ruta_arch in rutas.items():
        print(f"    -> [{tipo_fmt}] {ruta_arch}")


def menu_codigo_defectuoso():
    encabezado("4) CORRECCIÓN DE CÓDIGO DEFECTUOSO (5 CASOS DEL EXAMEN)")
    casos = ejecutar_todos_los_casos_defectuosos()
    for c in casos:
        print(f"\n  ======================================================================")
        print(f"  CASO {c['id']}: {c['categoria']}")
        print(f"  ======================================================================")
        print("  [Código Defectuoso Entregado]:")
        for linea in c["codigo_defectuoso"].splitlines():
            print(f"    {linea}")
        print(f"\n  [Identificación del Error]:\n    {c['identificacion_error']}")
        print("\n  [Código Corregido]:")
        for linea in c["codigo_corregido"].splitlines():
            print(f"    {linea}")
        print(f"\n  [Explicación de la Solución]:\n    {c['explicacion_solucion']}")
        print(f"  [Prueba de Entrada]       : {c['entrada_prueba']}")
        print(f"  [Resultado Defectuoso]    : {c['resultado_defectuoso']}")
        print(f"  [Resultado Corregido]     : {c['resultado_corregido']}")


def menu_comparacion_y_benchmark(estado):
    encabezado("6) COMPARACIÓN BÁSICA DE ESCENARIOS Y BENCHMARK EMPÍRICO")
    print("  TABLA OFICIAL DE RECOMENDACIÓN POR ESCENARIO:")
    linea_decorativa("-")
    print(f"  {'ESCENARIO':<36} | {'ALGORITMO RECOMENDADO':<45}")
    linea_decorativa("-")
    for fila in TABLA_COMPARACION_ESCENARIOS:
        print(f"  {fila['escenario']:<36} | {fila['algoritmo_recomendado']:<45}")
        print(f"    -> Complejidad : {fila['complejidad']}")
        print(f"    -> Razón       : {fila['justificacion']}\n")

    print("\n  Ejecutando Benchmark en vivo sobre el dataset cargado "
          f"({len(estado['datos_originales']):,} registros)...")
    resultados = ejecutar_benchmark_ordenamientos(estado["datos_originales"], ascendente=True)
    linea_decorativa("-")
    print(f"  {'ALGORITMO':<34} | {'TIPO':<14} | {'TIEMPO (ms)':>12} | {'COMPARACIONES':>14} | {'MOVIMIENTOS':>13}")
    linea_decorativa("-")
    for r in resultados:
        tipo_corto = "Interno" if "Interno" in r["categoria"] else "Externo"
        print(
            f"  {r['algoritmo']:<34} | {tipo_corto:<14} | {r['tiempo_ms']:>12.4f} | "
            f"{r['comparaciones']:>14,} | {r['intercambios']:>13,}"
        )
    linea_decorativa("-")


def ejecutar_demostracion_automatica():
    """Modo no interactivo (--demo) para verificar y capturar todos los requerimientos."""
    encabezado("EJECUCIÓN AUTOMÁTICA DE DEMOSTRACIÓN COMPLETA — EXAMEN PARCIAL")
    archivos = generar_datasets_financieros("datos", semilla=42)
    print("  [1] Datasets generados en TXT y XLSX (1,000 y 5,000 números enteros):")
    for k, v in archivos.items():
        print(f"      - {k}: {v}")

    for etiqueta, clave_arch in [("DATASET 1,000 REGISTROS (TXT)", "txt_1000"), ("DATASET 5,000 REGISTROS (XLSX)", "xlsx_5000")]:
        info = cargar_archivo_datos(archivos[clave_arch])
        encabezado(f"PROCESANDO {etiqueta}: {info['nombre_archivo']}")
        mostrar_resumen_20(f"Datos Originales ({info['total_registros']} enteros)", info["datos"])

        # Benchmark de todos los ordenamientos internos y externos
        bench = ejecutar_benchmark_ordenamientos(info["datos"], ascendente=True)
        print("\n  Comparativa de Algoritmos Internos y Externos:")
        linea_decorativa("-")
        print(f"  {'ALGORITMO':<34} | {'CATEGORÍA':<14} | {'TIEMPO (ms)':>12} | {'COMPARACIONES':>14} | {'VERIFICADO':>10}")
        linea_decorativa("-")
        for b in bench:
            cat = "Interno" if "Interno" in b["categoria"] else "Externo"
            ok = "OK" if b["verificado"] else "ERROR"
            print(f"  {b['algoritmo']:<34} | {cat:<14} | {b['tiempo_ms']:>12.4f} | {b['comparaciones']:>14,} | {ok:>10}")
        linea_decorativa("-")

        # Mostrar primeros 20 y últimos 20 ordenados con Quicksort
        res_qs = CATALOGO_INTERNOS["quicksort"][1](info["datos"], ascendente=True, retornar_metricas=True)
        mostrar_resumen_20(f"Datos Ordenados con {res_qs['algoritmo']} (Ascendente)", res_qs["datos"])

        # Exportar resultados
        rutas = exportar_resultados(
            datos_ordenados=res_qs["datos"],
            algoritmo_utilizado=res_qs["algoritmo"],
            tiempo_ejecucion_seg=res_qs["tiempo_seg"],
            orden=res_qs["orden"],
            comparaciones=res_qs["comparaciones"],
            intercambios=res_qs["intercambios"],
            archivo_origen=info["nombre_archivo"],
            directorio_salida="resultados",
            formato="AMBOS",
        )
        print(f"\n  [Exportación 5E] Archivos guardados: {rutas}")

        # Demostración de las 3 búsquedas
        objetivo = 77777 if info["total_registros"] == 1000 else 99999
        print(f"\n  [Búsquedas 3 y 5C] Buscando transacción objetivo = {objetivo:,}:")
        for rb in ejecutar_benchmark_busquedas(res_qs["datos"], objetivo, ascendente=True):
            print(
                f"    - {rb['metodo']:<32}: Encontrado={rb['encontrado']} | "
                f"Índice={rb['indice_primero']} | Apariciones={rb['total_apariciones']} | "
                f"Comparaciones={rb['comparaciones']} | Tiempo={rb['tiempo_ms']:.5f} ms"
            )

    menu_codigo_defectuoso()


def main():
    archivos_base = generar_datasets_financieros("datos", semilla=42)
    if "--demo" in sys.argv:
        ejecutar_demostracion_automatica()
        return

    info_inicial = cargar_archivo_datos(archivos_base["txt_1000"])
    estado = {
        "info_archivo": info_inicial,
        "datos_originales": info_inicial["datos"][:],
        "datos_actuales": info_inicial["datos"][:],
        "esta_ordenado": False,
        "ascendente": True,
        "ultimo_ordenamiento": None,
        "tabla_hash": None,
    }

    while True:
        encabezado("SISTEMA DE PROCESAMIENTO Y ORDENAMIENTO MASIVO DE DATOS FINANCIEROS")
        print(
            f"  Archivo activo : {estado['info_archivo']['nombre_archivo']} "
            f"({estado['info_archivo']['formato']} - {len(estado['datos_actuales']):,} registros)"
        )
        estado_str = (
            f"ORDENADO ({estado['ultimo_ordenamiento']['algoritmo']} - {estado['ultimo_ordenamiento']['orden']})"
            if estado["esta_ordenado"]
            else "SIN ORDENAR (Original)"
        )
        print(f"  Estado actual  : {estado_str}")
        linea_decorativa("-")
        print("  A) Cargar archivo             (Seleccionar TXT o XLSX de 1,000 o 5,000 enteros)")
        print("  B) Ordenar datos              (Elegir algoritmo Interno/Externo y orden Asc/Desc)")
        print("  C) Buscar un valor            (Secuencial, Binaria o Tabla Hash)")
        print("  D) Mostrar resultados         (Primeros 20 elementos, últimos 20 y total de registros)")
        print("  E) Exportar resultados        (Guardar archivo ordenado, tiempo y algoritmo utilizado)")
        print("  F) Corrección de código       (Ver y ejecutar los 5 casos de código defectuoso corregidos)")
        print("  G) Comparación y Benchmark    (Tabla de escenarios + Benchmark de los 10 algoritmos)")
        print("  S) Salir del sistema")
        linea_decorativa("-")

        opcion = input("  Selecciona una opción (A-G / S): ").strip().upper()

        if opcion in ("A", "1"):
            nueva_info = menu_cargar_archivo(archivos_base)
            estado["info_archivo"] = nueva_info
            estado["datos_originales"] = nueva_info["datos"][:]
            estado["datos_actuales"] = nueva_info["datos"][:]
            estado["esta_ordenado"] = False
            estado["ultimo_ordenamiento"] = None
            estado["tabla_hash"] = None
        elif opcion in ("B", "2"):
            menu_ordenar_datos(estado)
        elif opcion in ("C", "3"):
            menu_buscar_valor(estado)
        elif opcion in ("D", "4"):
            encabezado("D) MOSTRAR RESULTADOS (PRIMEROS 20, ÚLTIMOS 20 Y TOTAL DE REGISTROS)")
            mostrar_resumen_20("Estado Actual de los Registros en Memoria", estado["datos_actuales"])
        elif opcion in ("E", "5"):
            menu_exportar_resultados(estado)
        elif opcion in ("F", "6"):
            menu_codigo_defectuoso()
        elif opcion in ("G", "7"):
            menu_comparacion_y_benchmark(estado)
        elif opcion in ("S", "0", "SALIR"):
            print("\n  Cerrando el Sistema de Procesamiento y Ordenamiento Masivo de Datos. ¡Éxito en el examen!")
            break
        else:
            print("  [!] Opción no reconocida. Por favor elige A, B, C, D, E, F, G o S.")


if __name__ == "__main__":
    main()
