"""
DASHBOARD WEB INTERACTIVO (STREAMLIT)
"Sistema de Procesamiento y Ordenamiento Masivo de Datos Financieros"
Examen Parcial — Algoritmos de Ordenamiento y Búsqueda
Alumno: Emiliano Cab Martínez

Ejecución:
    streamlit run app_dashboard.py
"""

import os
import tempfile
import pandas as pd
import streamlit as st

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

st.set_page_config(
    page_title="Sistema Financiero - Ordenamiento y Búsqueda Masiva",
    page_icon="📊",
    layout="wide",
)

# Inicializar datasets oficiales si no existen
archivos_oficiales = generar_datasets_financieros("datos", semilla=42)

if "info_archivo" not in st.session_state:
    info_init = cargar_archivo_datos(archivos_oficiales["txt_1000"])
    st.session_state["info_archivo"] = info_init
    st.session_state["datos_originales"] = info_init["datos"].copy()
    st.session_state["datos_actuales"] = info_init["datos"].copy()
    st.session_state["esta_ordenado"] = False
    st.session_state["ascendente"] = True
    st.session_state["ultimo_ordenamiento"] = None

st.title("📊 Sistema de Procesamiento y Ordenamiento Masivo de Datos")
st.caption(
    "**Examen Parcial — Estructura de Datos** | **Alumno:** Emiliano Cab Martínez | "
    "**Librería Propia Base:** `MyLinkedList.py` (`Node` y `MyLinkedList`) | "
    "**Algoritmos:** Internos (`ADA1`/`ADA2`) y Externos (`MetOrdena`) sin `.sort()` ni `sorted()`"
)

# Barra lateral de estado
with st.sidebar:
    st.header("⚙️ Estado del Sistema")
    info_act = st.session_state["info_archivo"]
    st.metric("Archivo Activo", info_act["nombre_archivo"])
    st.metric("Librería / TDA Base", f"MyLinkedList ({len(st.session_state['datos_actuales']):,} nodos)")
    if st.session_state["esta_ordenado"] and st.session_state["ultimo_ordenamiento"]:
        ult = st.session_state["ultimo_ordenamiento"]
        st.success(f"Ordenado con: {ult['algoritmo']} ({ult['orden']})")
        st.metric("Tiempo de Ordenamiento", f"{ult['tiempo_ms']:.4f} ms")
    else:
        st.warning("Estado: Nodos Originales en MyLinkedList (Sin Ordenar)")

    st.divider()
    st.markdown("### 📦 Librerías Propias Integradas")
    st.markdown(
        "- **`MyLinkedList.py` (TDA Lista Enlazada Propia)**\n"
        "- `librerias/ordenamientos_internos.py`\n"
        "- `librerias/ordenamientos_externos.py`\n"
        "- `librerias/busquedas.py`\n"
        "- `librerias/manejo_archivos.py`\n"
        "- `librerias/codigo_defectuoso.py`\n"
        "- `librerias/comparador.py`"
    )

tabs = st.tabs([
    "📂 1. Carga y Vista (20/20)",
    "⚡ 2. Ordenamiento Interno/Externo",
    "🔍 3. Búsquedas (Secuencial, Binaria, Hash)",
    "🛠️ 4. Corrección de Código Defectuoso",
    "📈 5. Comparación y Benchmarks",
    "💾 6. Exportación de Resultados",
])

# =====================================================================
# TAB 1: CARGA DE ARCHIVOS Y VISTA 20/20
# =====================================================================
with tabs[0]:
    st.subheader("A) Carga de Archivos Financieros (TXT / XLSX - 1,000 y 5,000 Enteros)")
    col_a, col_b = st.columns([2, 1])

    with col_a:
        seleccion = st.selectbox(
            "Selecciona uno de los datasets oficiales del examen:",
            options=[
                ("1,000 Números Enteros — Formato TXT (datos/transacciones_1000.txt)", archivos_oficiales["txt_1000"]),
                ("1,000 Números Enteros — Formato XLSX (datos/transacciones_1000.xlsx)", archivos_oficiales["xlsx_1000"]),
                ("5,000 Números Enteros — Formato TXT (datos/transacciones_5000.txt)", archivos_oficiales["txt_5000"]),
                ("5,000 Números Enteros — Formato XLSX (datos/transacciones_5000.xlsx)", archivos_oficiales["xlsx_5000"]),
            ],
            format_func=lambda x: x[0],
        )
        if st.button("📥 Cargar Archivo Seleccionado en MyLinkedList", type="primary"):
            nueva_info = cargar_archivo_datos(seleccion[1])
            st.session_state["info_archivo"] = nueva_info
            st.session_state["datos_originales"] = nueva_info["datos"].copy()
            st.session_state["datos_actuales"] = nueva_info["datos"].copy()
            st.session_state["esta_ordenado"] = False
            st.session_state["ultimo_ordenamiento"] = None
            st.rerun()

    with col_b:
        archivo_subido = st.file_uploader("O sube un archivo propio (.txt o .xlsx):", type=["txt", "xlsx"])
        if archivo_subido is not None:
            sufijo = os.path.splitext(archivo_subido.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=sufijo) as tmp:
                tmp.write(archivo_subido.getbuffer())
                ruta_tmp = tmp.name
            nueva_info = cargar_archivo_datos(ruta_tmp)
            nueva_info["nombre_archivo"] = archivo_subido.name
            st.session_state["info_archivo"] = nueva_info
            st.session_state["datos_originales"] = nueva_info["datos"].copy()
            st.session_state["datos_actuales"] = nueva_info["datos"].copy()
            st.session_state["esta_ordenado"] = False
            st.session_state["ultimo_ordenamiento"] = None

    st.divider()
    st.subheader("D) Resumen de Registros Activos: Primeros 20, Últimos 20 y Total")
    resumen = obtener_resumen_resultados(st.session_state["datos_actuales"])
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total de Registros", f"{resumen['total_registros']:,}")
    m2.metric("Valor Mínimo", f"{resumen['minimo']:,}")
    m3.metric("Valor Máximo", f"{resumen['maximo']:,}")
    m4.metric("Promedio Financiero", f"{resumen['promedio']:,.2f}")

    c_p20, c_u20 = st.columns(2)
    with c_p20:
        st.markdown("**Primeros 20 elementos:**")
        st.dataframe(
            pd.DataFrame({
                "Índice": list(range(len(resumen["primeros_20"]))),
                "Valor (Monto Entero)": resumen["primeros_20"],
            }),
            use_container_width=True,
            hide_index=True,
        )
    with c_u20:
        st.markdown("**Últimos 20 elementos:**")
        n_tot = resumen["total_registros"]
        st.dataframe(
            pd.DataFrame({
                "Índice": list(range(max(0, n_tot - 20), n_tot)),
                "Valor (Monto Entero)": resumen["ultimos_20"],
            }),
            use_container_width=True,
            hide_index=True,
        )

# =====================================================================
# TAB 2: ORDENAMIENTOS INTERNOS Y EXTERNOS
# =====================================================================
with tabs[1]:
    st.subheader("B) Ejecución de Librerías Propias de Ordenamiento (Interno y Externo)")
    c1, c2, c3 = st.columns(3)

    with c1:
        tipo_procesamiento = st.radio(
            "Separación de procesamiento:",
            ["Interno (En Memoria RAM - ADA1/ADA2)", "Externo (Archivos Auxiliares F1/F2 - MetOrdena)"],
        )
    with c2:
        if "Interno" in tipo_procesamiento:
            alg_clave = st.selectbox(
                "Algoritmo Interno:",
                options=list(CATALOGO_INTERNOS.keys()),
                format_func=lambda k: CATALOGO_INTERNOS[k][0],
                index=4,
            )
        else:
            alg_clave = st.selectbox(
                "Algoritmo Externo:",
                options=list(CATALOGO_EXTERNOS.keys()),
                format_func=lambda k: CATALOGO_EXTERNOS[k][0],
            )
    with c3:
        sentido = st.radio("Orden de salida:", ["Ascendente (Menor a Mayor)", "Descendente (Mayor a Menor)"])
        es_asc = "Ascendente" in sentido

    if st.button("🚀 Ejecutar Ordenamiento Ahora", type="primary"):
        if "Interno" in tipo_procesamiento:
            _, fn = CATALOGO_INTERNOS[alg_clave]
            res_ord = fn(st.session_state["datos_originales"], ascendente=es_asc, retornar_metricas=True)
        else:
            _, fn = CATALOGO_EXTERNOS[alg_clave]
            if alg_clave in ("mezcla_directa", "mezcla_equilibrada"):
                res_ord = fn(
                    st.session_state["datos_originales"],
                    ascendente=es_asc,
                    retornar_metricas=True,
                    dir_auxiliar=os.path.join("resultados", "auxiliares_externos"),
                )
            else:
                res_ord = fn(st.session_state["datos_originales"], ascendente=es_asc, retornar_metricas=True)

        st.session_state["datos_actuales"] = res_ord["datos"]
        st.session_state["esta_ordenado"] = True
        st.session_state["ascendente"] = es_asc
        st.session_state["ultimo_ordenamiento"] = res_ord

    if st.session_state["ultimo_ordenamiento"]:
        ro = st.session_state["ultimo_ordenamiento"]
        st.success(
            f"✅ **{ro['algoritmo']}** ({ro['tipo']}) ejecutado en **{ro['tiempo_ms']:.4f} ms** "
            f"({ro['tiempo_seg']:.6f} s) | Verificación O(n): **{'100% Ordenado' if ro['verificado'] else 'Error'}**"
        )
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Tiempo (ms)", f"{ro['tiempo_ms']:.4f} ms")
        k2.metric("Comparaciones", f"{ro['comparaciones']:,}")
        k3.metric("Intercambios / Movs", f"{ro['intercambios']:,}")
        k4.metric("Complejidad", ro["complejidad"])

        res_post = obtener_resumen_resultados(ro["datos"])
        col_p, col_u = st.columns(2)
        with col_p:
            st.markdown("**Primeros 20 elementos ordenados:**")
            st.code(str(res_post["primeros_20"]))
        with col_u:
            st.markdown("**Últimos 20 elementos ordenados:**")
            st.code(str(res_post["ultimos_20"]))

# =====================================================================
# TAB 3: MÉTODOS DE BÚSQUEDA
# =====================================================================
with tabs[2]:
    st.subheader("C) Métodos de Búsqueda sobre MyLinkedList: Secuencial, Binaria y Tabla Hash")
    datos_busq = st.session_state["datos_actuales"]
    sugeridos = [
        datos_busq.head.data if datos_busq.head else 0,
        datos_busq[len(datos_busq) // 2] if len(datos_busq) > 0 else 0,
        datos_busq.tail.data if datos_busq.tail else 0,
    ]
    st.info(f"💡 Valores presentes en la MyLinkedList actual para probar: `{sugeridos[0]}`, `{sugeridos[1]}`, `{sugeridos[2]}`")

    cb1, cb2 = st.columns([1, 2])
    with cb1:
        valor_buscar = st.number_input("Valor entero a buscar:", value=int(sugeridos[1]), step=1)
    with cb2:
        metodo_sel = st.radio(
            "Selecciona método:",
            ["Comparar los 3 Métodos Simultáneamente", "Búsqueda Secuencial", "Búsqueda Binaria", "Búsqueda por Tabla Hash"],
            horizontal=True,
        )

    if st.button("🔎 Ejecutar Búsqueda", type="primary"):
        if not st.session_state["esta_ordenado"]:
            _, fn_qs = CATALOGO_INTERNOS["quicksort"]
            ro = fn_qs(st.session_state["datos_originales"], ascendente=True, retornar_metricas=True)
            st.session_state["datos_actuales"] = ro["datos"]
            st.session_state["esta_ordenado"] = True
            st.session_state["ascendente"] = True
            st.session_state["ultimo_ordenamiento"] = ro
            datos_busq = ro["datos"]

        res_b = ejecutar_benchmark_busquedas(datos_busq, int(valor_buscar), ascendente=st.session_state["ascendente"])
        if metodo_sel == "Búsqueda Secuencial":
            res_b = [res_b[0]]
        elif metodo_sel == "Búsqueda Binaria":
            res_b = [res_b[1]]
        elif metodo_sel == "Búsqueda por Tabla Hash":
            res_b = [res_b[2]]

        filas_b = []
        for r in res_b:
            filas_b.append({
                "Método de Búsqueda": r["metodo"],
                "Complejidad": r["complejidad"],
                "Encontrado": "SÍ" if r["encontrado"] else "NO",
                "Primer Índice": r["indice_primero"],
                "Total Apariciones": r["total_apariciones"],
                "Posiciones": str(r["todas_posiciones"][:10]),
                "Comparaciones": r["comparaciones"],
                "Tiempo (ms)": f"{r['tiempo_ms']:.5f} ms",
            })
        st.table(pd.DataFrame(filas_b))

# =====================================================================
# TAB 4: CORRECCIÓN DE CÓDIGO DEFECTUOSO
# =====================================================================
with tabs[3]:
    st.subheader("4) Identificación y Corrección de Código Defectuoso (5 Categorías del Examen)")
    casos = ejecutar_todos_los_casos_defectuosos()
    for c in casos:
        with st.expander(f"Caso {c['id']}: {c['categoria']}", expanded=True):
            col_err, col_fix = st.columns(2)
            with col_err:
                st.error("❌ Código Defectuoso Original")
                st.code(c["codigo_defectuoso"], language="python")
                st.markdown(f"**Fallo en ejecución:** `{c['resultado_defectuoso']}`")
            with col_fix:
                st.success("✅ Código Corregido Funcional")
                st.code(c["codigo_corregido"], language="python")
                st.markdown(f"**Resultado verificado:** `{c['resultado_corregido']}`")
            st.markdown(f"**🔍 Identificación del Error:** {c['identificacion_error']}")
            st.markdown(f"**🛠️ Explicación Técnica de la Corrección:** {c['explicacion_solucion']}")

# =====================================================================
# TAB 5: COMPARACIÓN DE ESCENARIOS Y BENCHMARK
# =====================================================================
with tabs[4]:
    st.subheader("6) Tabla de Comparación Básica por Escenario")
    st.dataframe(pd.DataFrame(TABLA_COMPARACION_ESCENARIOS), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader(f"⏱️ Benchmark Empírico en Vivo ({len(st.session_state['datos_originales']):,} registros)")
    if st.button("⚡ Ejecutar Benchmark de los 10 Algoritmos (7 Internos + 3 Externos)", type="primary"):
        resultados_bench = ejecutar_benchmark_ordenamientos(st.session_state["datos_originales"], ascendente=True)
        df_bench = pd.DataFrame(resultados_bench)
        st.dataframe(df_bench, use_container_width=True, hide_index=True)
        st.bar_chart(df_bench.set_index("algoritmo")["tiempo_ms"])

# =====================================================================
# TAB 6: EXPORTACIÓN DE RESULTADOS
# =====================================================================
with tabs[5]:
    st.subheader("E) Exportar Resultados (Archivo Ordenado, Tiempo de Ejecución y Algoritmo Utilizado)")
    if st.button("💾 Generar y Exportar Archivos Ordenados (TXT y XLSX)", type="primary"):
        if not st.session_state["esta_ordenado"] or not st.session_state["ultimo_ordenamiento"]:
            _, fn_qs = CATALOGO_INTERNOS["quicksort"]
            ro = fn_qs(st.session_state["datos_originales"], ascendente=True, retornar_metricas=True)
            st.session_state["datos_actuales"] = ro["datos"]
            st.session_state["esta_ordenado"] = True
            st.session_state["ultimo_ordenamiento"] = ro

        uo = st.session_state["ultimo_ordenamiento"]
        rutas = exportar_resultados(
            datos_ordenados=st.session_state["datos_actuales"],
            algoritmo_utilizado=uo["algoritmo"],
            tiempo_ejecucion_seg=uo["tiempo_seg"],
            orden=uo["orden"],
            comparaciones=uo["comparaciones"],
            intercambios=uo["intercambios"],
            archivo_origen=st.session_state["info_archivo"]["nombre_archivo"],
            directorio_salida="resultados",
            formato="AMBOS",
        )
        st.success(f"Archivos exportados exitosamente:\n- TXT: `{rutas['TXT']}`\n- XLSX: `{rutas['XLSX']}`")
        with open(rutas["TXT"], "rb") as f_txt:
            st.download_button("⬇️ Descargar Resultado TXT", f_txt, file_name=os.path.basename(rutas["TXT"]))
        with open(rutas["XLSX"], "rb") as f_xlsx:
            st.download_button("⬇️ Descargar Resultado XLSX", f_xlsx, file_name=os.path.basename(rutas["XLSX"]))
