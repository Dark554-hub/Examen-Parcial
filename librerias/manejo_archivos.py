"""
Librería de Manejo de Archivos y Generación de Datasets Financieros usando `MyLinkedList.py`.
Cumple con los requerimientos 1, 2, 5A, 5D y 5E del Examen Parcial:
- Carga todos los números enteros directamente en una instancia de tu librería propia `MyLinkedList`.
- Lectura de archivos de 1000 y 5000 números enteros en formatos TXT y XLSX.
- Uso permitido de pandas (solo lectura/escritura), openpyxl, time, os.
- Visualización de primeros 20 elementos, últimos 20 elementos y total de registros desde `MyLinkedList`.
- Exportación de resultados en TXT y XLSX recorriendo los nodos de `MyLinkedList`.
"""

import os
import random
import time
import pandas as pd
from MyLinkedList import MyLinkedList


def generar_datasets_financieros(directorio_datos="datos", semilla=42):
    """
    Genera los datasets oficiales requeridos por el examen utilizando `MyLinkedList`:
    - 1,000 números enteros (TXT y XLSX)
    - 5,000 números enteros (TXT y XLSX)
    """
    os.makedirs(directorio_datos, exist_ok=True)
    rng = random.Random(semilla)

    # Dataset 1: 1,000 transacciones financieras enteras en MyLinkedList
    datos_1000 = MyLinkedList()
    for i in range(1000):
        if i in (125, 840):
            datos_1000.append(77777)
        elif i == 500:
            datos_1000.append(123456)
        else:
            datos_1000.append(rng.randint(-15000, 250000))

    # Dataset 2: 5,000 transacciones financieras enteras en MyLinkedList
    datos_5000 = MyLinkedList()
    for i in range(5000):
        if i in (42, 2500):
            datos_5000.append(99999)
        elif i == 4910:
            datos_5000.append(314159)
        else:
            datos_5000.append(rng.randint(-25000, 500000))

    archivos_creados = {}

    # Guardar 1000 en TXT recorriendo los nodos de MyLinkedList
    ruta_txt_1000 = os.path.join(directorio_datos, "transacciones_1000.txt")
    with open(ruta_txt_1000, "w", encoding="utf-8") as f:
        cur = datos_1000.head
        while cur is not None:
            f.write(f"{cur.data}\n")
            cur = cur.next
    archivos_creados["txt_1000"] = ruta_txt_1000

    # Guardar 1000 en XLSX usando pandas + openpyxl
    ruta_xlsx_1000 = os.path.join(directorio_datos, "transacciones_1000.xlsx")
    df_1000 = pd.DataFrame({
        "ID_Transaccion": [f"TRX-{i+1:04d}" for i in range(len(datos_1000))],
        "Monto_Entero": datos_1000.to_list(),
    })
    df_1000.to_excel(ruta_xlsx_1000, index=False, engine="openpyxl")
    archivos_creados["xlsx_1000"] = ruta_xlsx_1000

    # Guardar 5000 en TXT recorriendo los nodos de MyLinkedList
    ruta_txt_5000 = os.path.join(directorio_datos, "transacciones_5000.txt")
    with open(ruta_txt_5000, "w", encoding="utf-8") as f:
        cur = datos_5000.head
        while cur is not None:
            f.write(f"{cur.data}\n")
            cur = cur.next
    archivos_creados["txt_5000"] = ruta_txt_5000

    # Guardar 5000 en XLSX usando pandas + openpyxl
    ruta_xlsx_5000 = os.path.join(directorio_datos, "transacciones_5000.xlsx")
    df_5000 = pd.DataFrame({
        "ID_Transaccion": [f"TRX-{i+1:05d}" for i in range(len(datos_5000))],
        "Monto_Entero": datos_5000.to_list(),
    })
    df_5000.to_excel(ruta_xlsx_5000, index=False, engine="openpyxl")
    archivos_creados["xlsx_5000"] = ruta_xlsx_5000

    return archivos_creados


def cargar_archivo_datos(ruta_archivo):
    """
    Lee un archivo TXT o XLSX e inserta cada número entero directamente mediante `.append()`
    en una instancia de tu librería propia `MyLinkedList`.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")

    t0 = time.perf_counter()
    ext = os.path.splitext(ruta_archivo)[1].lower()
    numeros_ll = MyLinkedList()

    if ext == ".txt":
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                limpia = linea.strip()
                if not limpia or limpia.startswith("#"):
                    continue
                partes = limpia.replace(",", " ").split()
                for p in partes:
                    try:
                        numeros_ll.append(int(float(p)))
                    except ValueError:
                        continue
    elif ext == ".xlsx":
        df = pd.read_excel(ruta_archivo, engine="openpyxl")
        col_objetivo = None
        if "Monto_Entero" in df.columns:
            col_objetivo = "Monto_Entero"
        else:
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    col_objetivo = col
        if col_objetivo is None and len(df.columns) > 0:
            col_objetivo = df.columns[0]
        if col_objetivo is not None:
            for x in df[col_objetivo].dropna():
                numeros_ll.append(int(x))
    else:
        raise ValueError(f"Formato no permitido: '{ext}'. Solo se permiten archivos .TXT y .XLSX.")

    t1 = time.perf_counter()
    return {
        "ruta": ruta_archivo,
        "nombre_archivo": os.path.basename(ruta_archivo),
        "formato": ext.upper().replace(".", ""),
        "estructura": "MyLinkedList",
        "datos": numeros_ll,
        "total_registros": len(numeros_ll),
        "tiempo_lectura_ms": (t1 - t0) * 1000.0,
    }


def obtener_resumen_resultados(lista_enlazada):
    """
    Requerimiento 5D: Recorre en un solo paso O(n) los nodos `Node` de `MyLinkedList` para obtener:
    - Primeros 20 elementos (como `MyLinkedList` y lista para visualización)
    - Últimos 20 elementos (como `MyLinkedList` y lista para visualización)
    - Total de registros (`len(MyLinkedList)`)
    - Mínimo, máximo y promedio.
    """
    ll = lista_enlazada if isinstance(lista_enlazada, MyLinkedList) else MyLinkedList(lista_enlazada)
    n = len(ll)
    if n == 0 or ll.head is None:
        return {
            "estructura": "MyLinkedList",
            "total_registros": 0,
            "primeros_20": [],
            "ultimos_20": [],
            "primeros_20_ll": MyLinkedList(),
            "ultimos_20_ll": MyLinkedList(),
            "minimo": 0,
            "maximo": 0,
            "promedio": 0.0,
        }

    primeros_20_ll = MyLinkedList()
    ultimos_20_ll = MyLinkedList()
    inicio_ultimos = max(0, n - 20)

    minimo = ll.head.data
    maximo = ll.head.data
    suma = 0

    cur = ll.head
    idx = 0
    while cur is not None:
        val = cur.data
        if idx < 20:
            primeros_20_ll.append(val)
        if idx >= inicio_ultimos:
            ultimos_20_ll.append(val)
        if val < minimo:
            minimo = val
        if val > maximo:
            maximo = val
        suma += val
        cur = cur.next
        idx += 1

    return {
        "estructura": "MyLinkedList",
        "total_registros": n,
        "primeros_20": primeros_20_ll,
        "ultimos_20": ultimos_20_ll,
        "primeros_20_ll": primeros_20_ll,
        "ultimos_20_ll": ultimos_20_ll,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": suma / n,
    }


def exportar_resultados(
    datos_ordenados,
    algoritmo_utilizado,
    tiempo_ejecucion_seg,
    orden="Ascendente",
    comparaciones=0,
    intercambios=0,
    archivo_origen="N/A",
    directorio_salida="resultados",
    formato="AMBOS",
):
    """
    Requerimiento 5E: Exportar resultados desde `MyLinkedList` guardando:
    - Archivo ordenado
    - Tiempo de ejecución
    - Algoritmo utilizado
    - Estructura utilizada (`MyLinkedList`)
    """
    os.makedirs(directorio_salida, exist_ok=True)
    ll = datos_ordenados if isinstance(datos_ordenados, MyLinkedList) else MyLinkedList(datos_ordenados)
    res_20 = obtener_resumen_resultados(ll)

    marca_tiempo = time.strftime("%Y%m%d_%H%M%S")
    nombre_limpio = (
        algoritmo_utilizado.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
    )
    n = len(ll)
    rutas_generadas = {}

    if formato.upper() in ("TXT", "AMBOS"):
        ruta_txt = os.path.join(directorio_salida, f"ordenado_{n}_{nombre_limpio}_{marca_tiempo}.txt")
        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write("# =================================================================\n")
            f.write("# REPORTE DE EXPORTACIÓN - SISTEMA DE PROCESAMIENTO MASIVO DE DATOS\n")
            f.write("# =================================================================\n")
            f.write(f"# Archivo de origen   : {archivo_origen}\n")
            f.write(f"# Librería / TDA base : MyLinkedList (MyLinkedList.py)\n")
            f.write(f"# Algoritmo utilizado : {algoritmo_utilizado}\n")
            f.write(f"# Orden aplicado      : {orden}\n")
            f.write(f"# Tiempo de ejecución : {tiempo_ejecucion_seg:.6f} segundos ({tiempo_ejecucion_seg*1000:.4f} ms)\n")
            f.write(f"# Total de registros  : {n}\n")
            f.write(f"# Comparaciones       : {comparaciones}\n")
            f.write(f"# Intercambios/Movs   : {intercambios}\n")
            f.write(f"# Primeros 20         : {res_20['primeros_20']}\n")
            f.write(f"# Últimos 20          : {res_20['ultimos_20']}\n")
            f.write("# =================================================================\n")
            cur = ll.head
            while cur is not None:
                f.write(f"{cur.data}\n")
                cur = cur.next
        rutas_generadas["TXT"] = ruta_txt

    if formato.upper() in ("XLSX", "AMBOS"):
        ruta_xlsx = os.path.join(directorio_salida, f"ordenado_{n}_{nombre_limpio}_{marca_tiempo}.xlsx")
        df_datos = pd.DataFrame({
            "Posicion_Nodo_MyLinkedList": list(range(1, n + 1)),
            "Monto_Entero": ll.to_list(),
        })
        df_meta = pd.DataFrame({
            "Parametro": [
                "Archivo de Origen",
                "Librería Propia Utilizada",
                "Algoritmo Utilizado",
                "Orden Aplicado",
                "Tiempo de Ejecución (segundos)",
                "Tiempo de Ejecución (milisegundos)",
                "Total de Nodos en MyLinkedList",
                "Comparaciones Realizadas",
                "Intercambios / Movimientos",
                "Primeros 20 Elementos",
                "Últimos 20 Elementos",
            ],
            "Valor": [
                str(archivo_origen),
                "MyLinkedList.py (Node & MyLinkedList)",
                str(algoritmo_utilizado),
                str(orden),
                f"{tiempo_ejecucion_seg:.6f} s",
                f"{tiempo_ejecucion_seg * 1000:.4f} ms",
                str(n),
                str(comparaciones),
                str(intercambios),
                str(res_20["primeros_20"]),
                str(res_20["ultimos_20"]),
            ],
        })
        with pd.ExcelWriter(ruta_xlsx, engine="openpyxl") as writer:
            df_meta.to_excel(writer, sheet_name="Resumen_Ejecucion", index=False)
            df_datos.to_excel(writer, sheet_name="Datos_Ordenados", index=False)
        rutas_generadas["XLSX"] = ruta_xlsx

    return rutas_generadas
