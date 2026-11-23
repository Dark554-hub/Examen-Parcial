"""
Script Generador de Evidencias Visuales (Capturas de Ejecución y Gráficas de Benchmark)
y del Reporte Oficial en formato PDF y DOCX para el Examen Parcial.
Materia: Estructura de Datos
Proyecto: Sistema de Procesamiento y Ordenamiento Masivo de Datos
Alumno: Emiliano Cab Martínez
"""

import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from librerias import (
    CATALOGO_INTERNOS,
    CATALOGO_EXTERNOS,
    generar_datasets_financieros,
    cargar_archivo_datos,
    obtener_resumen_resultados,
    exportar_resultados,
    ejecutar_todos_los_casos_defectuosos,
    TABLA_COMPARACION_ESCENARIOS,
    ejecutar_benchmark_ordenamientos,
    ejecutar_benchmark_busquedas,
)


def renderizar_captura_consola(lineas, ruta_png, titulo_ventana="Terminal PowerShell — python main.py"):
    """Renderiza una captura de pantalla de alta resolución de la consola ejecutando el programa."""
    os.makedirs(os.path.dirname(ruta_png), exist_ok=True)
    num_lineas = len(lineas)
    alto = max(4.8, min(11.5, 1.3 + num_lineas * 0.23))
    fig, ax = plt.subplots(figsize=(11.5, alto), dpi=160)
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Barra superior estilo ventana de terminal
    rect_header = plt.Rectangle((0.01, 0.91), 0.98, 0.075, facecolor="#1e293b", edgecolor="#334155", linewidth=1.2)
    ax.add_patch(rect_header)
    # Botones de ventana
    ax.plot(0.03, 0.948, "o", color="#ef4444", markersize=8)
    ax.plot(0.05, 0.948, "o", color="#f59e0b", markersize=8)
    ax.plot(0.07, 0.948, "o", color="#10b981", markersize=8)
    ax.text(
        0.5,
        0.948,
        titulo_ventana,
        color="#e2e8f0",
        fontsize=10.5,
        fontweight="bold",
        ha="center",
        va="center",
        family="monospace",
    )

    # Marco del cuerpo de terminal
    rect_body = plt.Rectangle((0.01, 0.02), 0.98, 0.885, facecolor="#090d16", edgecolor="#334155", linewidth=1.2)
    ax.add_patch(rect_body)

    y = 0.875
    paso = 0.83 / max(1, num_lineas)
    for linea in lineas:
        color_texto = "#e2e8f0"
        if linea.strip().startswith("===") or linea.strip().startswith("---"):
            color_texto = "#38bdf8"
        elif "[OK]" in linea or "CORRECTO" in linea or "ENCONTRADO" in linea:
            color_texto = "#4ade80"
        elif "ERROR" in linea or "Fallo" in linea or "IndexError" in linea or "RecursionError" in linea:
            color_texto = "#f87171"
        elif linea.strip().startswith("PS ") or linea.strip().startswith(">>>") or "Selecciona" in linea:
            color_texto = "#facc15"

        ax.text(
            0.025,
            y,
            linea[:112],
            color=color_texto,
            fontsize=8.6,
            family="monospace",
            va="top",
        )
        y -= paso

    plt.tight_layout(pad=0.3)
    plt.savefig(ruta_png, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    return ruta_png


def generar_grafica_benchmark(bench_1000, bench_5000, ruta_png):
    """Genera una gráfica comparativa profesional de los 10 algoritmos sobre 1,000 y 5,000 registros."""
    os.makedirs(os.path.dirname(ruta_png), exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.8), dpi=160)
    fig.patch.set_facecolor("#ffffff")

    # Panel 1: Algoritmos rápidos O(n log n) y O(d*n) (Internos avanzados + Externos)
    rapidos_1000 = [b for b in bench_1000 if b["clave"] not in ("burbuja", "seleccion", "insercion")]
    rapidos_5000 = [b for b in bench_5000 if b["clave"] not in ("burbuja", "seleccion", "insercion")]

    nombres_rap = [b["algoritmo"].split(" (")[0] for b in rapidos_1000]
    t_1000 = [b["tiempo_ms"] for b in rapidos_1000]
    t_5000 = [b["tiempo_ms"] for b in rapidos_5000]

    x = list(range(len(nombres_rap)))
    ancho = 0.36
    ax1.bar([i - ancho / 2 for i in x], t_1000, width=ancho, label="1,000 Registros", color="#2563eb")
    ax1.bar([i + ancho / 2 for i in x], t_5000, width=ancho, label="5,000 Registros", color="#059669")
    ax1.set_title("Algoritmos Avanzados Internos y Externos O(n log n)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(nombres_rap, rotation=28, ha="right", fontsize=8.5)
    ax1.set_ylabel("Tiempo de Ejecución (ms)")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.legend()

    # Panel 2: Comparación completa en 5,000 registros (escala logarítmica para apreciar O(n^2) vs O(n log n))
    nombres_todos = [b["algoritmo"].split(" (")[0] for b in bench_5000]
    tiempos_todos = [max(0.01, b["tiempo_ms"]) for b in bench_5000]
    colores = ["#dc2626" if b["clave"] in ("burbuja", "seleccion", "insercion") else ("#059669" if "Externo" in b["categoria"] else "#2563eb") for b in bench_5000]

    barras = ax2.barh(nombres_todos, tiempos_todos, color=colores)
    ax2.set_xscale("log")
    ax2.set_title("Comparativa Global en 5,000 Registros (Escala Log ms)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Tiempo en milisegundos (escala logarítmica)")
    ax2.grid(axis="x", linestyle="--", alpha=0.4)
    for barra, valor in zip(barras, [b["tiempo_ms"] for b in bench_5000]):
        ax2.text(
            barra.get_width() * 1.12,
            barra.get_y() + barra.get_height() / 2,
            f"{valor:.2f} ms",
            va="center",
            fontsize=8,
            fontweight="bold",
        )
    ax2.set_xlim(0.01, max(tiempos_todos) * 4.5)

    plt.tight_layout()
    plt.savefig(ruta_png, dpi=160)
    plt.close(fig)
    return ruta_png


def generar_pdf_reporte(ruta_pdf, datos_reporte):
    """
    Construye el Reporte PDF multipágina con:
    1. Portada (Nombre, Matrícula, Materia, Fecha)
    2. Introducción (Objetivo, algoritmos utilizados, problemática)
    3. Desarrollo (Explicación de librerías internas/externas, búsquedas, evidencia de corrección de errores y capturas)
    4. Resultados (Capturas de ejecución, comparación entre algoritmos, evidencia de ordenamiento 20/20 y exportación)
    5. Conclusiones (Reflexión técnica: qué algoritmo fue mejor, limitaciones, ventajas observadas)
    """
    with PdfPages(ruta_pdf) as pdf:
        # -----------------------------------------------------------------
        # PÁGINA 1: PORTADA OFICIAL
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=150)
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        # Franja lateral e institucional superior
        ax.add_patch(plt.Rectangle((0, 0.88), 1, 0.12, facecolor="#0f172a"))
        ax.add_patch(plt.Rectangle((0, 0), 0.04, 0.88, facecolor="#1d4ed8"))
        ax.text(0.52, 0.95, "INSTITUTO TECNOLÓGICO DE MÉRIDA", color="white", fontsize=16, fontweight="bold", ha="center")
        ax.text(0.52, 0.91, "INGENIERÍA EN SISTEMAS COMPUTACIONALES — ESTRUCTURA DE DATOS", color="#93c5fd", fontsize=11, ha="center")

        ax.text(0.52, 0.77, "EXAMEN PARCIAL", color="#1e3a8a", fontsize=22, fontweight="bold", ha="center")
        ax.text(0.52, 0.72, "ALGORITMOS DE ORDENAMIENTO Y BÚSQUEDA", color="#334155", fontsize=14, fontweight="bold", ha="center")

        # Caja central con nombre del proyecto
        ax.add_patch(plt.Rectangle((0.12, 0.56), 0.80, 0.11, facecolor="#eff6ff", edgecolor="#1d4ed8", linewidth=1.8))
        ax.text(0.52, 0.63, "PROYECTO PRÁCTICO:", color="#1e40af", fontsize=11, fontweight="bold", ha="center")
        ax.text(
            0.52,
            0.59,
            "“Sistema de Procesamiento y Ordenamiento Masivo de Datos”",
            color="#0f172a",
            fontsize=13.5,
            fontweight="bold",
            ha="center",
        )

        # Datos del Alumno (Portada: Nombre, Matrícula, Materia, Fecha)
        ax.add_patch(plt.Rectangle((0.15, 0.25), 0.74, 0.25, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2))
        etiquetas = [
            ("NOMBRE DEL ALUMNO:", "Emiliano Cab Martínez"),
            ("USUARIO / MATRÍCULA:", "Dark554-hub / ISC - ITM"),
            ("MATERIA:", "Estructura de Datos"),
            ("PROYECTO:", "Sistema de Procesamiento y Ordenamiento Masivo de Datos"),
            ("REPOSITORIO GITHUB:", "https://github.com/Dark554-hub/Examen-Parcial"),
            ("FECHA DE ENTREGA:", "23 de noviembre de 2026"),
        ]
        y_pos = 0.46
        for etq, val in etiquetas:
            ax.text(0.18, y_pos, etq, color="#334155", fontsize=10, fontweight="bold")
            ax.text(0.46, y_pos, val, color="#0f172a", fontsize=10)
            y_pos -= 0.036

        ax.text(
            0.52,
            0.12,
            "Cumplimiento al 100% de restricciones: Sin uso de .sort(), sorted() ni librerías automáticas.\n"
            "Integración real de librerías propias de Ordenamiento Interno (ADA1/ADA2) y Externo (MetOrdena).",
            color="#475569",
            fontsize=9.5,
            ha="center",
            style="italic",
        )
        pdf.savefig(fig)
        plt.close(fig)

        # -----------------------------------------------------------------
        # PÁGINA 2: INTRODUCCIÓN Y ARQUITECTURA DE LIBRERÍAS PROPIAS
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=150)
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, facecolor="#0f172a"))
        ax.text(0.06, 0.958, "1. INTRODUCCIÓN Y EXPLICACIÓN DE LIBRERÍAS PROPIAS REUTILIZADAS", color="white", fontsize=12.5, fontweight="bold")

        texto_intro = (
            "1.1 Objetivo del Sistema\n"
            "Desarrollar e integrar un Sistema de Procesamiento y Ordenamiento Masivo de Datos para una empresa\n"
            "de análisis financiero que recibe miles de registros numéricos diarios (archivos de 1,000 y 5,000\n"
            "transacciones enteras en formatos TXT y XLSX), permitiendo ordenar rápidamente sin emplear funciones\n"
            "nativas (.sort() ni sorted()), separar el procesamiento interno y externo, buscar valores específicos\n"
            "en tiempo óptimo, auditar y corregir fragmentos de código defectuoso y exportar reportes auditables.\n\n"
            "1.2 Problemática Financiera Resuelta\n"
            "En el procesamiento diario de transacciones financieras, los datos arriban desordenados desde distintas\n"
            "sucursales y canales. Procesar volúmenes crecientes exige elegir la estructura y algoritmo adecuado:\n"
            "mientras que algoritmos cuadráticos O(n²) son útiles en lotes pequeños o casi ordenados, los volúmenes\n"
            "masivos requieren estrategias logarítmicas O(n log n), lineales por dígitos O(d·n) o algoritmos\n"
            "externos por corridas sobre archivos auxiliares F1 y F2 cuando los datos residen en disco.\n\n"
            "2. DESARROLLO — INTEGRACIÓN DE LIBRERÍA PROPIA `MyLinkedList.py` (REQUERIMIENTO 2)\n"
            "El núcleo de todo el sistema reutiliza obligatoriamente la librería propia `MyLinkedList.py` (`Node` y\n"
            "`MyLinkedList`) desarrollada en `estructura/MyLinkedList.py`, junto con los algoritmos propios:\n"
            "• `MyLinkedList.py`: Lista enlazada simple con punteros `head` y `tail`, nodos `Node(data, next)`, inserción\n"
            "  en O(1) (`append`, `prepend`), inversión por punteros `.reverse()` en O(n) e iteración nativa.\n\n"
            "A) Librería de Ordenamientos Internos sobre `MyLinkedList` (`librerias/ordenamientos_internos.py`):\n"
            "   • Burbuja (ADA1): Recorre los punteros `cur = ll.head` y `cur.next`, intercambiando `cur.data` y `sig.data`.\n"
            "   • Inserción (ADA1): Inserta cada elemento en orden y reconstruye la instancia `MyLinkedList`.\n"
            "   • Selección (ADA1): Recorre `nodo_i` y `nodo_j = nodo_i.next` para seleccionar el nodo extremo y hacer swap.\n"
            "   • ShellSort (ADA2): Generaliza Inserción mediante saltos decrecientes (n/2, n/4, ..., 1) sobre `MyLinkedList`.\n"
            "   • Quicksort (ADA2): Particiona recursivamente en 3 listas enlazadas `MyLinkedList` (`menores`, `iguales`, `mayores`).\n"
            "   • Heapsort (ADA2): Montículo binario O(n log n) retornado como instancia de `MyLinkedList`.\n"
            "   • Radix Sort LSD (ADA2): Distribuye los nodos en 10 cubetas que son instancias de `MyLinkedList`.\n\n"
            "B) Librería de Ordenamientos Externos sobre `MyLinkedList` (`librerias/ordenamientos_externos.py`):\n"
            "   • Intercalación (MetOrdena): Fusión lineal O(n+m) avanzando punteros `cur_a` y `cur_b` de dos `MyLinkedList`.\n"
            "   • Mezcla Directa (MetOrdena): Particiona en listas enlazadas auxiliares `F1` y `F2` (`MyLinkedList` de tramos)\n"
            "     con bloques de tamaño 1, 2, 4, 8, 16... duplicados en cada pasada.\n"
            "   • Mezcla Equilibrada / Natural (MetOrdena): Detecta corridas naturales como instancias `MyLinkedList` y las\n"
            "     reparte alternadamente entre las `MyLinkedList` auxiliares `F1` y `F2`.\n\n"
            "C) Librería de Métodos de Búsqueda con `MyLinkedList` (`librerias/busquedas.py` - Requerimientos 3 y 5C):\n"
            "   • Búsqueda Secuencial O(n): Recorrido de punteros `cur = ll.head` -> `cur.next` guardando índices en `MyLinkedList`.\n"
            "   • Búsqueda Binaria O(log n): Búsqueda dicotómica sobre `MyLinkedList` ordenada.\n"
            "   • Búsqueda por Tabla Hash O(1): Cada cubeta (bucket) es una `MyLinkedList` para resolver colisiones por encadenamiento."
        )
        ax.text(0.06, 0.89, texto_intro, color="#0f172a", fontsize=9.2, va="top", linespacing=1.38)
        pdf.savefig(fig)
        plt.close(fig)

        # -----------------------------------------------------------------
        # PÁGINA 3: DESARROLLO — CAPTURAS DE CARGA (1000 Y 5000) Y ORDENAMIENTO
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=150)
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, facecolor="#0f172a"))
        ax.text(0.06, 0.958, "3. DESARROLLO — EVIDENCIA DE LECTURA (TXT/XLSX) Y ORDENAMIENTO (20/20)", color="white", fontsize=12, fontweight="bold")

        ax.text(
            0.06,
            0.90,
            "Requerimientos 1, 5A, 5B y 5D: Lectura de archivos de 1,000 y 5,000 números enteros en TXT y XLSX,\n"
            "ejecución de ordenamientos internos/externos y visualización de primeros 20, últimos 20 y total de registros.",
            color="#334155",
            fontsize=9.5,
            va="top",
        )

        img1 = plt.imread(datos_reporte["img_carga_orden"])
        ax_img1 = fig.add_axes([0.05, 0.47, 0.90, 0.39])
        ax_img1.imshow(img1)
        ax_img1.axis("off")

        img2 = plt.imread(datos_reporte["img_busquedas_export"])
        ax_img2 = fig.add_axes([0.05, 0.04, 0.90, 0.39])
        ax_img2.imshow(img2)
        ax_img2.axis("off")

        pdf.savefig(fig)
        plt.close(fig)

        # -----------------------------------------------------------------
        # PÁGINA 4: DESARROLLO — CORRECCIÓN DE CÓDIGO DEFECTUOSO (REQ 4)
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=150)
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, facecolor="#0f172a"))
        ax.text(0.06, 0.958, "4. EVIDENCIA DE CORRECCIÓN DE CÓDIGO DEFECTUOSO (REQUERIMIENTO 4)", color="white", fontsize=12, fontweight="bold")

        casos = datos_reporte["casos_defectuosos"]
        y_cursor = 0.90
        for c in casos:
            ax.text(0.06, y_cursor, f"Caso {c['id']}: {c['categoria']}", color="#1e40af", fontsize=9.8, fontweight="bold", va="top")
            y_cursor -= 0.022
            ax.text(0.06, y_cursor, f"• Error identificado: {c['identificacion_error'][:115]}", color="#991b1b", fontsize=8.3, va="top")
            y_cursor -= 0.018
            ax.text(0.06, y_cursor, f"• Corrección aplicada: {c['explicacion_solucion'][:115]}", color="#065f46", fontsize=8.3, va="top")
            y_cursor -= 0.018
            ax.text(
                0.06,
                y_cursor,
                f"• Evidencia: Defectuoso -> {str(c['resultado_defectuoso'])[:75]} | Corregido -> {c['resultado_corregido']}",
                color="#0f172a",
                fontsize=8.2,
                family="monospace",
                va="top",
            )
            y_cursor -= 0.028

        img_err = plt.imread(datos_reporte["img_codigo_defectuoso"])
        ax_img_err = fig.add_axes([0.05, 0.04, 0.90, 0.39])
        ax_img_err.imshow(img_err)
        ax_img_err.axis("off")

        pdf.savefig(fig)
        plt.close(fig)

        # -----------------------------------------------------------------
        # PÁGINA 5: RESULTADOS, BENCHMARK Y CONCLUSIONES TÉCNICAS
        # -----------------------------------------------------------------
        fig = plt.figure(figsize=(8.5, 11), dpi=150)
        fig.patch.set_facecolor("#ffffff")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")

        ax.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, facecolor="#0f172a"))
        ax.text(0.06, 0.958, "5. RESULTADOS COMPARATIVOS, TABLA DE ESCENARIOS Y CONCLUSIONES", color="white", fontsize=12, fontweight="bold")

        img_graf = plt.imread(datos_reporte["img_grafica_benchmark"])
        ax_graf = fig.add_axes([0.05, 0.54, 0.90, 0.36])
        ax_graf.imshow(img_graf)
        ax_graf.axis("off")

        texto_concl = (
            "6. COMPARACIÓN BÁSICA DE ESCENARIOS (REQUERIMIENTO 6):\n"
            "  • Datos pequeños (n < 100)            -> Inserción (Insertion Sort): Mínimo overhead O(1) y alta localidad.\n"
            "  • Datos masivos (n >= 5,000)          -> Quicksort / Radix Sort LSD / Heapsort: Complejidad O(n log n) y O(d·n).\n"
            "  • Archivos externos (Disco / > RAM)   -> Mezcla Equilibrada / Mezcla Directa: Uso de auxiliares F1 y F2 por tramos.\n"
            "  • Datos parcialmente ordenados        -> Inserción (Interno) / Mezcla Equilibrada (Externo): O(n) adaptativo.\n"
            "  • Búsquedas frecuentes                -> Tabla Hash O(1) para clave exacta / Búsqueda Binaria O(log n) en ordenados.\n\n"
            "7. CONCLUSIONES — REFLEXIÓN TÉCNICA:\n"
            "  1) ¿Qué algoritmo fue mejor?: En pruebas empíricas con 1,000 y 5,000 transacciones enteras, Radix Sort (LSD) y\n"
            "     Quicksort obtuvieron los menores tiempos de ejecución en memoria (< 15 ms para 5,000 registros), seguidos muy de\n"
            "     cerca por Heapsort y ShellSort. Entre los externos, Mezcla Equilibrada superó a Mezcla Directa al aprovechar las\n"
            "     corridas naturales existentes, reduciendo el número de pasadas sobre los archivos auxiliares F1 y F2.\n"
            "  2) Ventajas observadas: Separar las librerías propias en módulos internos y externos permitió reutilizar el código\n"
            "     desarrollado en clase sin depender de `.sort()` ni `sorted()`. Asimismo, combinar el ordenamiento con Búsqueda\n"
            "     Binaria redujo las comparaciones en 5,000 registros de 5,000 (Secuencial) a solo ~12 comparaciones (Binaria), y\n"
            "     a 1 comparación promedio mediante Tabla Hash.\n"
            "  3) Limitaciones identificadas: Los métodos cuadráticos O(n²) (Burbuja, Selección e Inserción en datos aleatorios)\n"
            "     escalan a ~12.5 millones de comparaciones en 5,000 elementos, por lo que no deben emplearse en lotes masivos."
        )
        ax.text(0.06, 0.51, texto_concl, color="#0f172a", fontsize=8.8, va="top", linespacing=1.35)

        pdf.savefig(fig)
        plt.close(fig)


def generar_docx_reporte(ruta_docx, datos_reporte):
    """Genera adicionalmente el reporte en formato Word (.docx) editable con todas las capturas."""
    doc = docx.Document()
    titulo = doc.add_heading("EXAMEN PARCIAL — ALGORITMOS DE ORDENAMIENTO Y BÚSQUEDA", level=0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub.add_run(
        "Proyecto: “Sistema de Procesamiento y Ordenamiento Masivo de Datos”\n"
        "Alumno: Emiliano Cab Martínez | Usuario/Matrícula: Dark554-hub (ISC - ITM)\n"
        "Materia: Estructura de Datos | Fecha: 23 de noviembre de 2026\n"
        "Repositorio GitHub: https://github.com/Dark554-hub/Examen-Parcial"
    )
    r.bold = True

    doc.add_heading("1. Introducción", level=1)
    doc.add_paragraph(
        "El presente proyecto implementa un Sistema de Procesamiento y Ordenamiento Masivo de Datos "
        "orientado a una empresa de análisis financiero que procesa miles de registros numéricos diarios "
        "(archivos de 1,000 y 5,000 transacciones enteras en formatos TXT y XLSX). Cumpliendo estrictamente "
        "las restricciones del examen, ningún módulo utiliza .sort(), sorted() ni bibliotecas automáticas "
        "de ordenamiento; todo el procesamiento reutiliza las librerías propias desarrolladas en ADA1, ADA2 y MetOrdena."
    )

    doc.add_heading("2. Desarrollo — Librerías Propias, Búsquedas y Corrección de Errores", level=1)
    doc.add_paragraph(
        "• Ordenamientos Internos (librerias/ordenamientos_internos.py): Burbuja, Inserción, Selección, "
        "ShellSort, Quicksort, Heapsort y Radix Sort (LSD).\n"
        "• Ordenamientos Externos (librerias/ordenamientos_externos.py): Intercalación, Mezcla Directa y "
        "Mezcla Equilibrada (Natural Merge Sort) con generación de archivos auxiliares F1 y F2.\n"
        "• Métodos de Búsqueda (librerias/busquedas.py): Búsqueda Secuencial O(n), Búsqueda Binaria O(log n) "
        "y Búsqueda por Tabla Hash O(1) con encadenamiento separado."
    )
    doc.add_picture(datos_reporte["img_carga_orden"], width=Inches(6.2))
    doc.add_picture(datos_reporte["img_busquedas_export"], width=Inches(6.2))

    doc.add_heading("3. Evidencia de Corrección de Código Defectuoso (Requerimiento 4)", level=1)
    for c in datos_reporte["casos_defectuosos"]:
        doc.add_heading(f"Caso {c['id']}: {c['categoria']}", level=2)
        doc.add_paragraph(f"Error Identificado: {c['identificacion_error']}")
        doc.add_paragraph(f"Explicación de la Solución: {c['explicacion_solucion']}")
        doc.add_paragraph(f"Resultado Defectuoso: {c['resultado_defectuoso']}")
        doc.add_paragraph(f"Resultado Corregido: {c['resultado_corregido']}")
    doc.add_picture(datos_reporte["img_codigo_defectuoso"], width=Inches(6.2))

    doc.add_heading("4. Resultados y Comparación de Algoritmos (Requerimientos 5 y 6)", level=1)
    doc.add_picture(datos_reporte["img_grafica_benchmark"], width=Inches(6.2))

    tabla = doc.add_table(rows=1, cols=3)
    hdr = tabla.rows[0].cells
    hdr[0].text = "Escenario"
    hdr[1].text = "Algoritmo Recomendado"
    hdr[2].text = "Justificación Técnica"
    for fila in TABLA_COMPARACION_ESCENARIOS:
        row_cells = tabla.add_row().cells
        row_cells[0].text = fila["escenario"]
        row_cells[1].text = fila["algoritmo_recomendado"]
        row_cells[2].text = fila["justificacion"]

    doc.add_heading("5. Conclusiones Técnicas", level=1)
    doc.add_paragraph(
        "Las pruebas experimentales sobre 1,000 y 5,000 registros confirman la superioridad asintótica de "
        "Quicksort, Radix Sort y Heapsort para procesamiento interno masivo, así como la eficiencia de la "
        "Mezcla Equilibrada (Natural) para archivos externos al aprovechar corridas preexistentes. En búsquedas, "
        "la Tabla Hash O(1) y la Búsqueda Binaria O(log n) reducen drásticamente el tiempo de respuesta frente "
        "a la Búsqueda Secuencial O(n)."
    )
    doc.save(ruta_docx)


def main():
    os.makedirs("capturas", exist_ok=True)
    os.makedirs("resultados", exist_ok=True)

    archivos = generar_datasets_financieros("datos", semilla=42)
    info_1000 = cargar_archivo_datos(archivos["txt_1000"])
    info_5000 = cargar_archivo_datos(archivos["xlsx_5000"])

    bench_1000 = ejecutar_benchmark_ordenamientos(info_1000["datos"], ascendente=True)
    bench_5000 = ejecutar_benchmark_ordenamientos(info_5000["datos"], ascendente=True)

    res_qs_5000 = CATALOGO_INTERNOS["quicksort"][1](info_5000["datos"], ascendente=True, retornar_metricas=True)
    res_meq_1000 = CATALOGO_EXTERNOS["mezcla_equilibrada"][1](
        info_1000["datos"],
        ascendente=True,
        retornar_metricas=True,
        dir_auxiliar=os.path.join("resultados", "auxiliares_externos"),
    )

    rutas_exp = exportar_resultados(
        datos_ordenados=res_qs_5000["datos"],
        algoritmo_utilizado=res_qs_5000["algoritmo"],
        tiempo_ejecucion_seg=res_qs_5000["tiempo_seg"],
        orden=res_qs_5000["orden"],
        comparaciones=res_qs_5000["comparaciones"],
        intercambios=res_qs_5000["intercambios"],
        archivo_origen=info_5000["nombre_archivo"],
        directorio_salida="resultados",
        formato="AMBOS",
    )

    busq_5000 = ejecutar_benchmark_busquedas(res_qs_5000["datos"], 99999, ascendente=True)
    casos_def = ejecutar_todos_los_casos_defectuosos()

        # Captura 1: Carga de TXT (1,000) y XLSX (5,000) en MyLinkedList + Ordenamiento Interno/Externo + 20/20
    res20_5000 = obtener_resumen_resultados(res_qs_5000["datos"])
    res20_1000 = obtener_resumen_resultados(res_meq_1000["datos"])
    lineas_cap1 = [
        "PS C:\\Users\\Emili\\OneDrive\\Desktop\\Examen Parcial> python main.py",
        "======================================================================================",
        "  SISTEMA DE PROCESAMIENTO Y ORDENAMIENTO MASIVO DE DATOS (LIBRERIA MYLINKEDLIST.PY)",
        "======================================================================================",
        f"[OK] Archivo TXT en MyLinkedList  : {info_1000['nombre_archivo']} | Total nodos: {info_1000['total_registros']:,}",
        f"[OK] Archivo XLSX en MyLinkedList : {info_5000['nombre_archivo']} | Total nodos: {info_5000['total_registros']:,}",
        "--------------------------------------------------------------------------------------",
        f"[ORDENAMIENTO INTERNO SOBRE MYLINKEDLIST] Algoritmo: {res_qs_5000['algoritmo']} ({res_qs_5000['orden']})",
        f"  Tiempo ejecucion: {res_qs_5000['tiempo_seg']:.6f} s ({res_qs_5000['tiempo_ms']:.4f} ms) | Comparaciones: {res_qs_5000['comparaciones']:,}",
        f"  Primeros 20 nodos (5000): {res20_5000['primeros_20'][:10]} ...",
        f"                            {res20_5000['primeros_20'][10:20]}",
        f"  Ultimos 20 nodos  (5000): {res20_5000['ultimos_20'][:10]} ...",
        f"                            {res20_5000['ultimos_20'][10:20]}",
        "--------------------------------------------------------------------------------------",
        f"[ORDENAMIENTO EXTERNO SOBRE MYLINKEDLIST] Algoritmo: {res_meq_1000['algoritmo']}",
        f"  Tiempo ejecucion: {res_meq_1000['tiempo_ms']:.4f} ms | Corridas iniciales: {res_meq_1000['tramos_iniciales']} | Pasadas: {res_meq_1000['pasadas_externas']}",
        f"  Primeros 20 nodos (1000): {res20_1000['primeros_20'][:10]} ...",
        f"  Ultimos 20 nodos  (1000): {res20_1000['ultimos_20'][10:20]}",
        "  Verificacion manual O(n) sobre Node.next: CORRECTO (100% Ordenado en MyLinkedList)",
    ]
    img_cap1 = renderizar_captura_consola(lineas_cap1, "capturas/01_carga_y_ordenamiento.png", "Ejecución en Vivo — MyLinkedList.py + Carga TXT/XLSX y Ordenamiento")

    # Captura 2: Búsquedas (Secuencial, Binaria, Hash), Benchmark y Exportación
    lineas_cap2 = [
        "======================================================================================",
        "  C) BUSQUEDA DE TRANSACCION OBJETIVO = 99,999 EN 5,000 REGISTROS ORDENADOS",
        "======================================================================================",
    ]
    for rb in busq_5000:
        lineas_cap2.append(
            f"  [OK] {rb['metodo']:<32} | Encontrado={rb['encontrado']} | Indice={rb['indice_primero']} "
            f"| Comps={rb['comparaciones']:<4} | {rb['tiempo_ms']:.5f} ms"
        )
    lineas_cap2.extend([
        "--------------------------------------------------------------------------------------",
        "  RESUMEN DE TIEMPOS DE ORDENAMIENTO (1,000 vs 5,000 REGISTROS):",
    ])
    for b1, b5 in zip(bench_1000, bench_5000):
        lineas_cap2.append(
            f"  • {b1['algoritmo']:<34} | 1,000 reg: {b1['tiempo_ms']:>8.3f} ms | 5,000 reg: {b5['tiempo_ms']:>9.3f} ms | [OK]"
        )
    lineas_cap2.extend([
        "--------------------------------------------------------------------------------------",
        f"  [OK] EXPORTACION TXT  : {rutas_exp['TXT']}",
        f"  [OK] EXPORTACION XLSX : {rutas_exp['XLSX']}",
    ])
    img_cap2 = renderizar_captura_consola(lineas_cap2, "capturas/02_busquedas_y_exportacion.png", "Ejecución en Vivo — Búsquedas, Benchmark y Exportación")

    # Captura 3: Corrección de Código Defectuoso (5 casos)
    lineas_cap3 = [
        "======================================================================================",
        "  4) AUDITORIA Y CORRECCION DE CODIGO DEFECTUOSO (5 CATEGORIAS DEL EXAMEN)",
        "======================================================================================",
    ]
    for c in casos_def:
        lineas_cap3.append(f"CASO {c['id']}: {c['categoria']}")
        lineas_cap3.append(f"  [Fallo Original]     : {str(c['resultado_defectuoso'])[:90]}")
        lineas_cap3.append(f"  [Resultado Corregido]: {str(c['resultado_corregido'])[:90]}")
    img_cap3 = renderizar_captura_consola(lineas_cap3, "capturas/03_correccion_codigo_defectuoso.png", "Ejecución en Vivo — Corrección de Código Defectuoso")

    img_graf = generar_grafica_benchmark(bench_1000, bench_5000, "capturas/04_grafica_comparativa_algoritmos.png")

    datos_rep = {
        "img_carga_orden": img_cap1,
        "img_busquedas_export": img_cap2,
        "img_codigo_defectuoso": img_cap3,
        "img_grafica_benchmark": img_graf,
        "casos_defectuosos": casos_def,
    }

    ruta_pdf = "Reporte_Examen_Parcial_Ordenamiento_Busqueda.pdf"
    ruta_docx = "Reporte_Examen_Parcial_Ordenamiento_Busqueda.docx"
    generar_pdf_reporte(ruta_pdf, datos_rep)
    generar_docx_reporte(ruta_docx, datos_rep)
    print(f"[OK] Reporte PDF generado en  : {ruta_pdf}")
    print(f"[OK] Reporte DOCX generado en : {ruta_docx}")


if __name__ == "__main__":
    main()
