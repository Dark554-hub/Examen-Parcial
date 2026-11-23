"""
Librería de Manejo de Archivos y Generación de Datasets Financieros.
Cumple con los requerimientos 1, 5A, 5D y 5E del Examen Parcial:
- Lectura de archivos de 1000 y 5000 números enteros en formatos TXT y XLSX.
- Uso permitido de pandas (solo lectura/escritura), openpyxl, time, os.
- Visualización de primeros 20 elementos, últimos 20 elementos y total de registros.
- Exportación de resultados en TXT y XLSX incluyendo archivo ordenado, tiempo de ejecución
  y algoritmo utilizado.
"""

import os
import random
import time
import pandas as pd


def generar_datasets_financieros(directorio_datos="datos", semilla=42):
    """
    Genera los datasets oficiales requeridos por el examen:
    - 1,000 números enteros (TXT y XLSX)
    - 5,000 números enteros (TXT y XLSX)
    - Además un dataset parcialmente ordenado de 1,000 registros para pruebas comparativas.
    Simula montos de transacciones financieras en pesos (entre -25,000 y 500,000).
    """
    os.makedirs(directorio_datos, exist_ok=True)
    rng = random.Random(semilla)

    # Dataset 1: 1,000 transacciones financieras enteras
    datos_1000 = [rng.randint(-15000, 250000) for _ in range(1000)]
    # Inyectar valores conocidos para facilitar demostraciones de búsqueda en vivo
    datos_1000[125] = 77777
    datos_1000[840] = 77777
    datos_1000[500] = 123456

    # Dataset 2: 5,000 transacciones financieras enteras
    datos_5000 = [rng.randint(-25000, 500000) for _ in range(5000)]
    datos_5000[42] = 99999
    datos_5000[2500] = 99999
    datos_5000[4910] = 314159

    archivos_creados = {}

    # Guardar 1000 en TXT
    ruta_txt_1000 = os.path.join(directorio_datos, "transacciones_1000.txt")
    with open(ruta_txt_1000, "w", encoding="utf-8") as f:
        for val in datos_1000:
            f.write(f"{val}\n")
    archivos_creados["txt_1000"] = ruta_txt_1000

    # Guardar 1000 en XLSX usando pandas + openpyxl
    ruta_xlsx_1000 = os.path.join(directorio_datos, "transacciones_1000.xlsx")
    df_1000 = pd.DataFrame({
        "ID_Transaccion": [f"TRX-{i+1:04d}" for i in range(1000)],
        "Monto_Entero": datos_1000,
    })
    df_1000.to_excel(ruta_xlsx_1000, index=False, engine="openpyxl")
    archivos_creados["xlsx_1000"] = ruta_xlsx_1000

    # Guardar 5000 en TXT
    ruta_txt_5000 = os.path.join(directorio_datos, "transacciones_5000.txt")
    with open(ruta_txt_5000, "w", encoding="utf-8") as f:
        for val in datos_5000:
            f.write(f"{val}\n")
    archivos_creados["txt_5000"] = ruta_txt_5000

    # Guardar 5000 en XLSX usando pandas + openpyxl
    ruta_xlsx_5000 = os.path.join(directorio_datos, "transacciones_5000.xlsx")
    df_5000 = pd.DataFrame({
        "ID_Transaccion": [f"TRX-{i+1:05d}" for i in range(5000)],
        "Monto_Entero": datos_5000,
    })
    df_5000.to_excel(ruta_xlsx_5000, index=False, engine="openpyxl")
    archivos_creados["xlsx_5000"] = ruta_xlsx_5000

    return archivos_creados


def cargar_archivo_datos(ruta_archivo):
    """
    Lee un archivo TXT o XLSX y extrae la lista de números enteros junto con
    metadatos de lectura (tiempo de carga, formato, ruta, total de registros).
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe.")

    t0 = time.perf_counter()
    ext = os.path.splitext(ruta_archivo)[1].lower()
    numeros = []

    if ext == ".txt":
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                limpia = linea.strip()
                if not limpia or limpia.startswith("#"):
                    continue
                # Soportar números separados por coma, espacio o salto de línea
                partes = limpia.replace(",", " ").split()
                for p in partes:
                    try:
                        numeros.append(int(float(p)))
                    except ValueError:
                        continue
    elif ext == ".xlsx":
        df = pd.read_excel(ruta_archivo, engine="openpyxl")
        # Buscar columna numérica (priorizando 'Monto_Entero' o la última columna numérica)
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
            numeros = [int(x) for x in df[col_objetivo].dropna().tolist()]
    else:
        raise ValueError(f"Formato no permitido: '{ext}'. Solo se permiten archivos .TXT y .XLSX.")

    t1 = time.perf_counter()
    return {
        "ruta": ruta_archivo,
        "nombre_archivo": os.path.basename(ruta_archivo),
        "formato": ext.upper().replace(".", ""),
        "datos": numeros,
        "total_registros": len(numeros),
        "tiempo_lectura_ms": (t1 - t0) * 1000.0,
    }


def obtener_resumen_resultados(lista):
    """
    Requerimiento 5D: Mostrar primeros 20 elementos, últimos 20 elementos y total de registros.
    Calcula además mínimo, máximo y suma manualmente sin usar funciones de ordenamiento.
    """
    n = len(lista)
    if n == 0:
        return {
            "total_registros": 0,
            "primeros_20": [],
            "ultimos_20": [],
            "minimo": 0,
            "maximo": 0,
            "promedio": 0.0,
        }

    primeros_20 = lista[:20]
    ultimos_20 = lista[-20:] if n >= 20 else lista[:]

    minimo = lista[0]
    maximo = lista[0]
    suma = 0
    for x in lista:
        if x < minimo:
            minimo = x
        if x > maximo:
            maximo = x
        suma += x

    return {
        "total_registros": n,
        "primeros_20": primeros_20,
        "ultimos_20": ultimos_20,
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
    Requerimiento 5E: Exportar resultados guardando:
    - Archivo ordenado
    - Tiempo de ejecución
    - Algoritmo utilizado
    Soporta exportación tanto a TXT como a XLSX (con hoja de Metadatos y hoja de Datos Ordenados).
    """
    os.makedirs(directorio_salida, exist_ok=True)
    marca_tiempo = time.strftime("%Y%m%d_%H%M%S")
    nombre_limpio = (
        algoritmo_utilizado.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
    )
    n = len(datos_ordenados)
    rutas_generadas = {}

    if formato.upper() in ("TXT", "AMBOS"):
        ruta_txt = os.path.join(directorio_salida, f"ordenado_{n}_{nombre_limpio}_{marca_tiempo}.txt")
        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write("# =================================================================\n")
            f.write("# REPORTE DE EXPORTACIÓN - SISTEMA DE PROCESAMIENTO MASIVO DE DATOS\n")
            f.write("# =================================================================\n")
            f.write(f"# Archivo de origen   : {archivo_origen}\n")
            f.write(f"# Algoritmo utilizado : {algoritmo_utilizado}\n")
            f.write(f"# Orden aplicado      : {orden}\n")
            f.write(f"# Tiempo de ejecución : {tiempo_ejecucion_seg:.6f} segundos ({tiempo_ejecucion_seg*1000:.4f} ms)\n")
            f.write(f"# Total de registros  : {n}\n")
            f.write(f"# Comparaciones       : {comparaciones}\n")
            f.write(f"# Intercambios/Movs   : {intercambios}\n")
            f.write(f"# Primeros 20         : {datos_ordenados[:20]}\n")
            f.write(f"# Últimos 20          : {datos_ordenados[-20:]}\n")
            f.write("# =================================================================\n")
            for val in datos_ordenados:
                f.write(f"{val}\n")
        rutas_generadas["TXT"] = ruta_txt

    if formato.upper() in ("XLSX", "AMBOS"):
        ruta_xlsx = os.path.join(directorio_salida, f"ordenado_{n}_{nombre_limpio}_{marca_tiempo}.xlsx")
        df_datos = pd.DataFrame({
            "Posicion_Ordenada": list(range(1, n + 1)),
            "Monto_Entero": datos_ordenados,
        })
        df_meta = pd.DataFrame({
            "Parametro": [
                "Archivo de Origen",
                "Algoritmo Utilizado",
                "Orden Aplicado",
                "Tiempo de Ejecución (segundos)",
                "Tiempo de Ejecución (milisegundos)",
                "Total de Registros Procesados",
                "Comparaciones Realizadas",
                "Intercambios / Movimientos",
                "Primeros 20 Elementos",
                "Últimos 20 Elementos",
            ],
            "Valor": [
                str(archivo_origen),
                str(algoritmo_utilizado),
                str(orden),
                f"{tiempo_ejecucion_seg:.6f} s",
                f"{tiempo_ejecucion_seg * 1000:.4f} ms",
                str(n),
                str(comparaciones),
                str(intercambios),
                str(datos_ordenados[:20]),
                str(datos_ordenados[-20:]),
            ],
        })
        with pd.ExcelWriter(ruta_xlsx, engine="openpyxl") as writer:
            df_meta.to_excel(writer, sheet_name="Resumen_Ejecucion", index=False)
            df_datos.to_excel(writer, sheet_name="Datos_Ordenados", index=False)
        rutas_generadas["XLSX"] = ruta_xlsx

    return rutas_generadas
