"""
Paquete de Librerías Propias - Sistema de Procesamiento y Ordenamiento Masivo de Datos.
Examen Parcial - Estructura de Datos.
Autor: Emiliano Cab Martínez

Integración obligatoria de la librería propia `MyLinkedList.py` (`Node` y `MyLinkedList`)
desarrollada en `c:\\Users\\Emili\\OneDrive\\Desktop\\estructura\\MyLinkedList.py`.
"""

from MyLinkedList import Node, MyLinkedList
from librerias.ordenamientos_internos import (
    asegurar_linked_list,
    ordenamiento_burbuja,
    ordenamiento_insercion,
    ordenamiento_seleccion,
    shell_sort,
    quicksort,
    heapsort,
    radix_sort,
    verificar_orden,
    CATALOGO_INTERNOS,
)
from librerias.ordenamientos_externos import (
    intercalar_listas,
    ordenamiento_intercalacion,
    mezcla_directa,
    mezcla_equilibrada,
    CATALOGO_EXTERNOS,
)
from librerias.busquedas import (
    busqueda_secuencial,
    busqueda_binaria,
    busqueda_hash,
    TablaHashTransacciones,
)
from librerias.manejo_archivos import (
    generar_datasets_financieros,
    cargar_archivo_datos,
    obtener_resumen_resultados,
    exportar_resultados,
)
from librerias.codigo_defectuoso import ejecutar_todos_los_casos_defectuosos
from librerias.comparador import (
    TABLA_COMPARACION_ESCENARIOS,
    ejecutar_benchmark_ordenamientos,
    ejecutar_benchmark_busquedas,
)

__all__ = [
    "Node",
    "MyLinkedList",
    "asegurar_linked_list",
    "ordenamiento_burbuja",
    "ordenamiento_insercion",
    "ordenamiento_seleccion",
    "shell_sort",
    "quicksort",
    "heapsort",
    "radix_sort",
    "verificar_orden",
    "CATALOGO_INTERNOS",
    "intercalar_listas",
    "ordenamiento_intercalacion",
    "mezcla_directa",
    "mezcla_equilibrada",
    "CATALOGO_EXTERNOS",
    "busqueda_secuencial",
    "busqueda_binaria",
    "busqueda_hash",
    "TablaHashTransacciones",
    "generar_datasets_financieros",
    "cargar_archivo_datos",
    "obtener_resumen_resultados",
    "exportar_resultados",
    "ejecutar_todos_los_casos_defectuosos",
    "TABLA_COMPARACION_ESCENARIOS",
    "ejecutar_benchmark_ordenamientos",
    "ejecutar_benchmark_busquedas",
]
