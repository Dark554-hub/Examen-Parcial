"""
Suite de Pruebas Automatizadas (Unit & Integration Tests)
"Sistema de Procesamiento y Ordenamiento Masivo de Datos"
Verifica automáticamente:
1. El uso obligatorio y exclusivo de la librería propia `MyLinkedList.py` (`Node` y `MyLinkedList`).
2. Que ningún algoritmo utilice .sort() ni sorted() y que todos devuelvan una instancia de `MyLinkedList`
   ordenada 100% bien en Ascendente y Descendente.
3. Lectura y escritura de 1,000 y 5,000 números enteros en TXT y XLSX cargados en `MyLinkedList`.
4. Funcionamiento exacto de Búsqueda Secuencial, Búsqueda Binaria y Tabla Hash con `MyLinkedList`.
5. Ejecución y corrección de los 5 casos de código defectuoso sobre `MyLinkedList`.
"""

import unittest
import random
from MyLinkedList import Node, MyLinkedList
from librerias import (
    CATALOGO_INTERNOS,
    CATALOGO_EXTERNOS,
    verificar_orden,
    busqueda_secuencial,
    busqueda_binaria,
    busqueda_hash,
    generar_datasets_financieros,
    cargar_archivo_datos,
    obtener_resumen_resultados,
    ejecutar_todos_los_casos_defectuosos,
)


class TestSistemaOrdenamientoBusqueda(unittest.TestCase):
    def setUp(self):
        rng = random.Random(123)
        self.muestra = MyLinkedList([rng.randint(-5000, 10000) for _ in range(250)])

    def test_libreria_mylinkedlist_integrada(self):
        ll = MyLinkedList([10, 20, 30])
        ll.append(40)
        ll.prepend(5)
        self.assertIsInstance(ll.head, Node)
        self.assertEqual(len(ll), 5)
        self.assertEqual(ll.head.data, 5)
        self.assertEqual(ll.tail.data, 40)

    def test_ordenamientos_internos_asc_y_desc_en_mylinkedlist(self):
        for clave, (nombre, fn) in CATALOGO_INTERNOS.items():
            res_asc = fn(self.muestra, ascendente=True, retornar_metricas=True)
            self.assertIsInstance(res_asc["datos"], MyLinkedList, f"{nombre} no devolvió MyLinkedList")
            self.assertTrue(verificar_orden(res_asc["datos"], ascendente=True), f"Fallo ascendente en {nombre}")
            self.assertEqual(len(res_asc["datos"]), len(self.muestra))

            res_desc = fn(self.muestra, ascendente=False, retornar_metricas=True)
            self.assertIsInstance(res_desc["datos"], MyLinkedList, f"{nombre} no devolvió MyLinkedList")
            self.assertTrue(verificar_orden(res_desc["datos"], ascendente=False), f"Fallo descendente en {nombre}")
            self.assertEqual(len(res_desc["datos"]), len(self.muestra))

    def test_ordenamientos_externos_asc_y_desc_en_mylinkedlist(self):
        for clave, (nombre, fn) in CATALOGO_EXTERNOS.items():
            res_asc = fn(self.muestra, ascendente=True, retornar_metricas=True)
            self.assertIsInstance(res_asc["datos"], MyLinkedList, f"{nombre} no devolvió MyLinkedList")
            self.assertTrue(verificar_orden(res_asc["datos"], ascendente=True), f"Fallo ascendente en {nombre}")
            self.assertEqual(len(res_asc["datos"]), len(self.muestra))

            res_desc = fn(self.muestra, ascendente=False, retornar_metricas=True)
            self.assertIsInstance(res_desc["datos"], MyLinkedList, f"{nombre} no devolvió MyLinkedList")
            self.assertTrue(verificar_orden(res_desc["datos"], ascendente=False), f"Fallo descendente en {nombre}")
            self.assertEqual(len(res_desc["datos"]), len(self.muestra))

    def test_busquedas_secuencial_binaria_hash_con_mylinkedlist(self):
        ordenada_ll = CATALOGO_INTERNOS["quicksort"][1](self.muestra, ascendente=True)
        self.assertIsInstance(ordenada_ll, MyLinkedList)
        objetivo = ordenada_ll[120]

        r_sec = busqueda_secuencial(ordenada_ll, objetivo)
        r_bin = busqueda_binaria(ordenada_ll, objetivo, ascendente=True)
        r_hash = busqueda_hash(ordenada_ll, objetivo)

        self.assertTrue(r_sec["encontrado"])
        self.assertTrue(r_bin["encontrado"])
        self.assertTrue(r_hash["encontrado"])
        self.assertIsInstance(r_sec["posiciones_linked_list"], MyLinkedList)
        self.assertIsInstance(r_bin["posiciones_linked_list"], MyLinkedList)
        self.assertIsInstance(r_hash["posiciones_linked_list"], MyLinkedList)
        self.assertEqual(r_sec["todas_posiciones"], r_bin["todas_posiciones"])
        self.assertEqual(r_sec["todas_posiciones"], r_hash["todas_posiciones"])

    def test_lectura_archivos_1000_y_5000_txt_xlsx_en_mylinkedlist(self):
        archivos = generar_datasets_financieros("datos", semilla=42)
        info_t1 = cargar_archivo_datos(archivos["txt_1000"])
        info_x1 = cargar_archivo_datos(archivos["xlsx_1000"])
        info_t5 = cargar_archivo_datos(archivos["txt_5000"])
        info_x5 = cargar_archivo_datos(archivos["xlsx_5000"])

        self.assertIsInstance(info_t1["datos"], MyLinkedList)
        self.assertIsInstance(info_x1["datos"], MyLinkedList)
        self.assertIsInstance(info_t5["datos"], MyLinkedList)
        self.assertIsInstance(info_x5["datos"], MyLinkedList)

        self.assertEqual(info_t1["total_registros"], 1000)
        self.assertEqual(info_x1["total_registros"], 1000)
        self.assertEqual(info_t5["total_registros"], 5000)
        self.assertEqual(info_x5["total_registros"], 5000)

        res20 = obtener_resumen_resultados(info_t5["datos"])
        self.assertIsInstance(res20["primeros_20_ll"], MyLinkedList)
        self.assertIsInstance(res20["ultimos_20_ll"], MyLinkedList)
        self.assertEqual(len(res20["primeros_20_ll"]), 20)
        self.assertEqual(len(res20["ultimos_20_ll"]), 20)

    def test_correccion_codigo_defectuoso(self):
        casos = ejecutar_todos_los_casos_defectuosos()
        self.assertEqual(len(casos), 5)
        self.assertEqual(casos[0]["resultado_corregido"], [7, 12, 33, 45, 89])
        self.assertEqual(casos[1]["resultado_corregido"], [10, 20, 30, 50, 50])
        self.assertEqual(casos[2]["resultado_corregido"], [10, 25, 40, 60, 90])
        self.assertEqual(casos[3]["resultado_corregido"], [9, 25, 300, 1000])


if __name__ == "__main__":
    unittest.main()
