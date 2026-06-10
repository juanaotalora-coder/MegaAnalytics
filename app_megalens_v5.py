import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import re

st.set_page_config(page_title="Análisis Megalens", layout="wide")

# ── Autenticación simple ──────────────────────────────────────
import hmac

def check_password():
    def password_entered():
        contrasena = st.secrets.get("APP_PASSWORD", "") if hasattr(st, "secrets") else ""
        if contrasena and hmac.compare_digest(st.session_state["password"], contrasena):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if st.session_state.get("authenticated", False):
        return True

    st.markdown("""
    <div style='max-width:440px;margin:60px auto;text-align:center'>
        <div style='
            background:linear-gradient(135deg,#0D2E35 0%,#1A5C6B 40%,#1E7A3E 100%);
            padding:40px 36px;border-radius:16px;
            box-shadow:0 8px 32px rgba(58,191,196,0.25);
            position:relative;overflow:hidden;
        '>
            <div style='
                position:absolute;top:-40px;right:-40px;
                width:180px;height:180px;
                background:radial-gradient(circle,rgba(58,191,196,0.15) 0%,transparent 70%);
                border-radius:50%;
            '></div>
            <div style='position:relative;z-index:1'>
                <div style='width:64px;height:64px;margin:0 auto 16px;
                    filter:drop-shadow(0 4px 12px rgba(58,191,196,0.5))'>
                    <svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'>
  <defs>
    <linearGradient id='lg2' x1='0%25' y1='0%25' x2='100%25' y2='100%25'>
      <stop offset='0%25' style='stop-color:%233ABFC4'/>
      <stop offset='100%25' style='stop-color:%236DB33F'/>
    </linearGradient>
  </defs>
  <path d='M30 4 C44 4 56 14 56 28 C56 44 44 57 30 57 C16 57 4 44 4 28 C4 14 16 4 30 4 Z' fill='url(%23lg2)'/>
  <path d='M30 54 Q30 35 30 8' stroke='rgba(255,255,255,0.25)' stroke-width='1.2' fill='none'/>
  <text x='30' y='36' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='22' fill='white' letter-spacing='1'>M</text>
</svg>
                </div>
                <h1 style='color:white;font-size:32px;font-weight:800;margin:0;letter-spacing:2px'>
                    <span style='color:#3ABFC4'>Mega</span>
                    <span style='
                        background:linear-gradient(90deg,#6DB33F,#3ABFC4);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;
                    '> Analytics</span>
                </h1>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.text_input("Contraseña", type="password", key="password",
                  on_change=password_entered, placeholder="Ingresa la contraseña")

    if "authenticated" in st.session_state and not st.session_state["authenticated"]:
        st.error("Contraseña incorrecta.")

    return False

if not check_password():
    st.stop()

st.markdown("""
<div style='
    background:linear-gradient(135deg,#0D2E35 0%,#1A5C6B 40%,#1E7A3E 100%);
    padding:28px 36px;border-radius:16px;margin-bottom:24px;
    box-shadow:0 8px 32px rgba(58,191,196,0.25);
    position:relative;overflow:hidden;
'>
    <div style='position:absolute;top:-50px;right:-50px;width:220px;height:220px;
        background:radial-gradient(circle,rgba(58,191,196,0.15) 0%,transparent 70%);border-radius:50%'></div>
    <div style='position:absolute;bottom:-40px;left:35%;width:160px;height:160px;
        background:radial-gradient(circle,rgba(109,179,63,0.12) 0%,transparent 70%);border-radius:50%'></div>
    <div style='position:relative;z-index:1;text-align:center'>
        <div style='width:64px;height:64px;margin:0 auto 14px;
            filter:drop-shadow(0 4px 16px rgba(58,191,196,0.5))'>
            <svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'>
  <defs>
    <linearGradient id='lg2' x1='0%25' y1='0%25' x2='100%25' y2='100%25'>
      <stop offset='0%25' style='stop-color:%233ABFC4'/>
      <stop offset='100%25' style='stop-color:%236DB33F'/>
    </linearGradient>
  </defs>
  <path d='M30 4 C44 4 56 14 56 28 C56 44 44 57 30 57 C16 57 4 44 4 28 C4 14 16 4 30 4 Z' fill='url(%23lg2)'/>
  <path d='M30 54 Q30 35 30 8' stroke='rgba(255,255,255,0.25)' stroke-width='1.2' fill='none'/>
  <text x='30' y='36' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='22' fill='white' letter-spacing='1'>M</text>
</svg>
        </div>
        <h1 style='color:white;margin:0;font-size:40px;font-weight:800;letter-spacing:2px;line-height:1'>
            <span style='color:#3ABFC4'>Mega</span>
            <span style='background:linear-gradient(90deg,#6DB33F,#3ABFC4);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text'> Analytics</span>
        </h1>
        <p style='color:rgba(255,255,255,0.55);margin:8px 0 0;font-size:12px;
            letter-spacing:3px;text-transform:uppercase'>
            Laboratorios Oftálmicos &nbsp;·&nbsp; Análisis de Clientes y Ventas
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

MESES_ORDEN = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

with st.sidebar:
    st.header("Configuración")
    col_cliente = st.text_input("Columna de cliente", value="Cliente")
    col_ciudad  = st.text_input("Columna de ciudad",  value="Ciudad")
    umbral      = st.number_input("Umbral mínimo para contar como venta ($)", value=10000, step=1000)
    col_hoja    = st.text_input("Hoja del Excel (vacío = primera hoja)", value="")

archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo:
    try:
        hoja = col_hoja if col_hoja.strip() else 0
        df = pd.read_excel(archivo, sheet_name=hoja)
        df.columns = df.columns.str.strip()

        # Detectar columnas Mes-Año
        patron = re.compile(r'^([A-Za-záéíóúÁÉÍÓÚ]{3,4})[\s\-–—_]+(\d{2,4})$')
        cols_ventas = {}
        for col in df.columns:
            m = patron.match(str(col).strip())
            if m:
                mes_str = m.group(1).capitalize()
                anio_str = m.group(2)
                anio = int(anio_str) if len(anio_str) == 4 else 2000 + int(anio_str)
                if mes_str in MESES_ORDEN:
                    mes_idx = MESES_ORDEN.index(mes_str)
                    cols_ventas[(anio, mes_idx)] = col

        if not cols_ventas:
            st.error("No se encontraron columnas con formato Mes-Año (ej: Ene-25, Feb-26).")
            st.write("Columnas detectadas:", list(df.columns))
            st.stop()

        # Limpiar numéricos
        for col in cols_ventas.values():
            df[col] = (
                df[col].astype(str)
                .str.replace(r'[\$\s,]', '', regex=True)
                .str.strip()
                .replace(['', '-', '$-', ' -   '], '0')
                .pipe(pd.to_numeric, errors='coerce')
                .fillna(0)
            )

        # Eliminar filas sin cliente (filas vacías o de totales)
        df = df[df[col_cliente].notna()].copy()
        df = df[df[col_cliente].astype(str).str.strip().replace("nan","") != ""].copy()
        df[col_cliente] = df[col_cliente].astype(str).str.strip()
        if col_ciudad in df.columns:
            df[col_ciudad] = df[col_ciudad].fillna("").astype(str).str.strip()



        anios = sorted(set(k[0] for k in cols_ventas))

        def cols_de_anio(anio):
            pares = sorted([(k[1], v) for k, v in cols_ventas.items() if k[0] == anio])
            return [(MESES_ORDEN[idx], col) for idx, col in pares]

        data_por_anio = {a: cols_de_anio(a) for a in anios}

        # ── YTD dinámico basado en fecha actual ──────────────────────
        from datetime import date
        import calendar as _cal
        hoy = date.today()
        dias_en_mes = _cal.monthrange(hoy.year, hoy.month)[1]
        dias_restantes = dias_en_mes - hoy.day
        # Si faltan 3 días o menos para cerrar el mes, incluir mes actual
        if dias_restantes <= 3:
            mes_ytd = hoy.month
        else:
            mes_ytd = hoy.month - 1
            if mes_ytd == 0:
                mes_ytd = 12

        mes_ytd_label = MESES_ORDEN[mes_ytd - 1] if mes_ytd <= 12 else MESES_ORDEN[-1]
        st.success(f"Archivo cargado: {len(df):,} clientes | Años detectados: {', '.join(str(a) for a in anios)} | YTD calculado hasta: {mes_ytd_label}")

        cols_orden = [v for k,v in sorted(cols_ventas.items())]

        # ── Revisión de calidad de datos ─────────────────────────────
        st.subheader("Revisión de calidad de datos")

        # Aplicar df de sesión si existe
        if "df_fusionado" in st.session_state:
            df = st.session_state["df_fusionado"].copy()

        # 1. Duplicados exactos
        dupes_exactos = df[df.duplicated(subset=[col_cliente] + cols_orden, keep=False)]
        pares_dupes = []
        if len(dupes_exactos) > 0:
            for nombre, grupo in dupes_exactos.groupby(col_cliente):
                if len(grupo) > 1:
                    pares_dupes.append(nombre)

        eliminaciones_aprobadas = set()
        if pares_dupes:
            with st.expander("⚠️ Registros duplicados exactos detectados", expanded=True):
                st.caption("Marca los que quieras eliminar (se conserva solo una fila).")
                for nombre in pares_dupes:
                    if st.checkbox(f"Eliminar duplicado: {nombre}", key=f"dup_{nombre}"):
                        eliminaciones_aprobadas.add(nombre)
                if eliminaciones_aprobadas:
                    if st.button("Eliminar duplicados seleccionados"):
                        for nombre in eliminaciones_aprobadas:
                            idx_dupes = df[df[col_cliente] == nombre].index[1:]
                            df = df.drop(idx_dupes)
                        st.session_state["df_fusionado"] = df
                        st.success("Duplicados eliminados.")
                        st.rerun()
        else:
            st.success("No se detectaron duplicados exactos.")

        # 2. Agrupación manual
        clientes_alfa = sorted(df[col_cliente].unique().tolist())

        with st.expander("Crear grupos de clientes (cadenas, franquicias, etc.)"):
            st.caption("Cada grupo agrupa múltiples clientes en uno solo sumando sus ventas.")

            if "num_grupos" not in st.session_state:
                st.session_state["num_grupos"] = 0

            col_btn1, col_btn2 = st.columns([1, 4])
            with col_btn1:
                if st.button("+ Agregar grupo"):
                    st.session_state["num_grupos"] += 1
                    st.rerun()
            with col_btn2:
                if st.session_state["num_grupos"] > 0:
                    if st.button("Resetear grupos"):
                        st.session_state["num_grupos"] = 0
                        for k in list(st.session_state.keys()):
                            if k.startswith("grupo_nombre_") or k.startswith("grupo_miembros_"):
                                del st.session_state[k]
                        st.rerun()

            grupos_definidos = []
            for g in range(st.session_state["num_grupos"]):
                st.markdown(f"**Grupo {g+1}**")
                c1, c2 = st.columns([1, 2])
                with c1:
                    nombre_grupo = st.text_input(f"Nombre del grupo", key=f"grupo_nombre_{g}",
                                                  placeholder="Ej: OPTICA CIENTIFICA Y CIA")
                with c2:
                    miembros = st.multiselect(f"Clientes que pertenecen a este grupo",
                                              options=clientes_alfa,
                                              key=f"grupo_miembros_{g}")
                if nombre_grupo and len(miembros) >= 2:
                    grupos_definidos.append((nombre_grupo, miembros))

            if grupos_definidos:
                if st.button("Aplicar grupos"):
                    for nombre_grupo, miembros in grupos_definidos:
                        filas = df[df[col_cliente].isin(miembros)]
                        if len(filas) == 0:
                            continue
                        idx_base = filas.index[0]
                        for idx in filas.index[1:]:
                            for col in cols_orden:
                                df.at[idx_base, col] = df.at[idx_base, col] + df.at[idx, col]
                            df = df.drop(idx)
                        df.at[idx_base, col_cliente] = nombre_grupo
                    st.session_state["df_fusionado"] = df
                    st.session_state["num_grupos"] = 0
                    for k in list(st.session_state.keys()):
                        if k.startswith("grupo_nombre_") or k.startswith("grupo_miembros_"):
                            del st.session_state[k]
                    st.success("Grupos aplicados correctamente.")
                    st.rerun()

        st.divider()

        # data_filtrada = todos los meses (sin filtro de meses general)
        data_filtrada = {a: data_por_anio[a] for a in anios}

        # ── Selector de 3 meses para recurrencia ─────────────────────
        st.subheader("Meses de referencia para recurrencia")
        st.caption("Elige exactamente 3 meses que definen un cliente recurrente.")
        cols_rec = st.columns(len(anios))
        meses_3m = {}
        for i, anio in enumerate(anios):
            opciones = [m for m, _ in data_por_anio[anio]]
            with cols_rec[i]:
                sel3 = st.multiselect(
                    f"3 meses recurrencia {anio}",
                    opciones,
                    default=opciones[-3:] if len(opciones) >= 3 else opciones,
                    max_selections=3,
                    key=f"rec_{anio}"
                )
                if len(sel3) != 3:
                    st.warning(f"Selecciona exactamente 3 meses para {anio}")
                meses_3m[anio] = sel3

        st.divider()

        # ── Métricas ─────────────────────────────────────────────────
        def calcular(pares, meses_rec):
            if not pares:
                return {}, {}, 0, 0, {}
            activos = {m: int((df[c] >= umbral).sum()) for m, c in pares}
            ventas  = {m: df[c].sum() for m, c in pares}
            # Recurrencia: solo en los 3 meses seleccionados
            pares_rec = [(m, c) for m, c in pares if m in meses_rec]
            if len(pares_rec) == 3:
                mat = pd.concat([(df[c] >= umbral).astype(int).rename(m) for m, c in pares_rec], axis=1)
                n_3m = int((mat.sum(axis=1) == 3).sum())
            else:
                n_3m = 0
            prom_act = sum(activos.values()) / len(activos) if activos else 1
            pct_3m = n_3m / prom_act * 100 if prom_act > 0 else 0
            prom_compras = {m: (ventas[m] / activos[m] if activos[m] > 0 else 0) for m in activos}
            return activos, ventas, n_3m, pct_3m, prom_compras

        metr = {a: calcular(data_filtrada[a], meses_3m.get(a, [])) for a in anios}

        # ── Tabla resumen ────────────────────────────────────────────
        st.subheader("Resumen de clientes activos")
        COLORES = ["#2E86C1", "#1E8449", "#6C3483", "#A93226"]

        for i, anio in enumerate(anios):
            activos, ventas, n_3m, pct_3m, prom_compras = metr[anio]
            if not activos:
                continue
            meses = list(activos.keys())
            color = COLORES[i % len(COLORES)]
            n_cols = len(meses) + 2

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#EAF7F7 0%,#F0F7EA 100%);
                        border:1px solid #3ABFC4;border-radius:10px;padding:14px 10px 10px;
                        margin-bottom:16px;box-shadow:0 2px 6px rgba(58,191,196,0.1)'>
            """, unsafe_allow_html=True)

            h = st.columns(n_cols)
            with h[0]:
                st.markdown(f"<div style='background:{color};color:white;text-align:center;padding:6px 2px;border-radius:4px;font-size:12px;font-weight:600'>Clientes Activos<br>YTD {anio}</div>", unsafe_allow_html=True)
            for j, m in enumerate(meses):
                with h[j+1]:
                    st.markdown(f"<div style='background:{color};color:white;text-align:center;padding:6px 2px;font-size:13px;font-weight:600'>{m}</div>", unsafe_allow_html=True)
            with h[-1]:
                st.markdown("<div style='background:#E67E22;color:white;text-align:center;padding:6px 2px;border-radius:4px;font-size:13px;font-weight:600'>3 meses</div>", unsafe_allow_html=True)

            v = st.columns(n_cols)
            with v[0]:
                st.markdown("<div style='padding:4px'></div>", unsafe_allow_html=True)
            for j, m in enumerate(meses):
                with v[j+1]:
                    st.markdown(f"<div style='text-align:center;font-size:20px;font-weight:700;color:#3D3D3D;padding:6px 0'>{activos[m]}</div>", unsafe_allow_html=True)
            with v[-1]:
                st.markdown(f"<div style='text-align:center;font-size:20px;font-weight:700;color:#3D3D3D;padding:6px 0'>{n_3m}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background:linear-gradient(90deg,#3ABFC4,#6DB33F);color:white;
                        text-align:center;padding:10px;border-radius:6px;
                        font-weight:600;font-size:14px;margin-top:6px'>
                Porcentaje de Fidelización: {pct_3m:.0f}%
            </div>
            </div>
            """, unsafe_allow_html=True)
            with st.popover("ℹ️ ¿Qué es el Porcentaje de Fidelización?"):
                st.markdown("Proporción de clientes que compraron en los **3 meses seleccionados**, en relación con el promedio mensual de clientes activos del período.")
            st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

        # Variación YoY promedio compras + Últ. 3M
        if len(anios) >= 2:
            a1, a2 = anios[-2], anios[-1]
            prom1, prom2 = metr[a1][4], metr[a2][4]
            meses_c = [m for m in prom1 if m in prom2]

            # Calcular promedio Últ. 3M (solo clientes que compraron los 3 meses)
            def prom_3m_calc(anio, meses_rec):
                pares_rec = [(m, c) for m, c in data_filtrada[anio] if m in meses_rec]
                if len(pares_rec) != 3:
                    return 0
                mask = pd.Series([True] * len(df), index=df.index)
                for m, c in pares_rec:
                    mask = mask & (df[c] >= umbral)
                clientes_rec = df[mask]
                if len(clientes_rec) == 0:
                    return 0
                total = sum(clientes_rec[c].sum() for _, c in pares_rec)
                return total / len(clientes_rec) / 3

            rec_a1 = meses_3m.get(a1, [])
            rec_a2 = meses_3m.get(a2, [])
            p3m_a1 = prom_3m_calc(a1, rec_a1)
            p3m_a2 = prom_3m_calc(a2, rec_a2)
            var_3m = ((p3m_a2 - p3m_a1) / p3m_a1 * 100) if p3m_a1 > 0 else 0
            mostrar_3m = len(rec_a1) == 3 and len(rec_a2) == 3

            if meses_c:
                n_extra = 1 if mostrar_3m else 0
                var_cols = st.columns(len(meses_c) + 1 + n_extra)
                with var_cols[0]:
                    st.markdown(f"<div style='font-size:13px;color:#555;padding-top:8px'>Var Prom. Compras {a1}→{a2}</div>", unsafe_allow_html=True)
                for j, m in enumerate(meses_c):
                    p1, p2 = prom1[m], prom2[m]
                    var = ((p2 - p1) / p1 * 100) if p1 > 0 else 0
                    col_v = "#E74C3C" if var < 0 else "#27AE60"
                    with var_cols[j+1]:
                        st.markdown(f"<div style='text-align:center;color:{col_v};font-weight:500;font-size:15px'>{var:+.0f}%</div>", unsafe_allow_html=True)
                if mostrar_3m:
                    col_v3 = "#E74C3C" if var_3m < 0 else "#27AE60"
                    with var_cols[-1]:
                        st.markdown(f"<div style='text-align:center;color:{col_v3};font-weight:500;font-size:15px;border-left:1px solid #ddd;padding-left:4px'>{var_3m:+.0f}%</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center;font-size:11px;color:#888'>Últ. 3M</div>", unsafe_allow_html=True)

        st.divider()

        # ── Clientes Nuevos y Retomados ──────────────────────────────
        st.subheader("Clientes Nuevos y Retomados")

        # Obtener todos los pares ordenados cronológicamente
        todos_pares = [(m, c) for _, pares in [(a, data_por_anio[a]) for a in anios] for m, c in pares]

        if len(todos_pares) >= 2:
            # Selector de mes de referencia
            opciones_meses = [f"{m} ({a})" for a in anios for m, _ in data_por_anio[a]]
            idx_default = len(opciones_meses) - 1
            mes_ref_sel = st.selectbox("Mes de referencia", opciones_meses,
                                        index=idx_default, key="sel_mes_nuevos")
            idx_ref = opciones_meses.index(mes_ref_sel)
            mes_rec_label, mes_rec_col = todos_pares[idx_ref]

            if idx_ref == 0:
                st.warning("Selecciona un mes con al menos un mes anterior disponible.")
                st.stop()

            # Mes anterior al seleccionado
            mes_ant_label, mes_ant_col = todos_pares[idx_ref - 1]
            # 3 meses antes del seleccionado (si existen)
            meses_3_ant = todos_pares[max(0, idx_ref-3):idx_ref]
            st.caption(f"Comparando {mes_ant_label} → {mes_rec_label}")

            compro_reciente   = df[mes_rec_col] >= umbral
            compro_ant        = df[mes_ant_col] >= umbral

            # Clientes nuevos: compraron en mes reciente pero no en ninguno de los 3 anteriores
            if len(meses_3_ant) > 0:
                no_compro_3ant = pd.Series([True] * len(df), index=df.index)
                for _, c in meses_3_ant:
                    no_compro_3ant = no_compro_3ant & (df[c] < umbral)
                mask_nuevos = compro_reciente & no_compro_3ant
            else:
                mask_nuevos = compro_reciente & ~compro_ant

            # Clientes retomados: no compraron el mes anterior pero sí en el más reciente
            mask_retomados = compro_reciente & ~compro_ant & ~mask_nuevos

            df_nuevos   = df[mask_nuevos][[col_cliente] + ([col_ciudad] if col_ciudad in df.columns else []) + [mes_rec_col]].copy()
            df_retomados = df[mask_retomados][[col_cliente] + ([col_ciudad] if col_ciudad in df.columns else []) + [mes_rec_col]].copy()
            df_nuevos[mes_rec_col] = df_nuevos[mes_rec_col].apply(lambda x: f"${x:,.0f}")
            df_retomados[mes_rec_col] = df_retomados[mes_rec_col].apply(lambda x: f"${x:,.0f}")

            cn1, cn2 = st.columns(2)
            with cn1:
                st.markdown(f"**Clientes Nuevos** en {mes_rec_label}: **{len(df_nuevos)}**")
                st.caption(f"Compraron en {mes_rec_label} pero no en los 3 meses anteriores.")
                if len(df_nuevos) > 0:
                    st.dataframe(df_nuevos.rename(columns={mes_rec_col: f"Venta {mes_rec_label}"}),
                                 hide_index=True, use_container_width=True)
                else:
                    st.info("No hay clientes nuevos en este período.")

            with cn2:
                st.markdown(f"**Clientes Retomados** en {mes_rec_label}: **{len(df_retomados)}**")
                st.caption(f"No compraron en {mes_ant_label} pero sí en {mes_rec_label}.")
                if len(df_retomados) > 0:
                    st.dataframe(df_retomados.rename(columns={
                        mes_ant_col: f"Venta {mes_ant_label}",
                        mes_rec_col: f"Venta {mes_rec_label}"
                    }), hide_index=True, use_container_width=True)
                else:
                    st.info("No hay clientes retomados en este período.")
            # Clientes en fuga
            mask_fuga = compro_ant & ~compro_reciente
            df_fuga = df[mask_fuga][[col_cliente] + ([col_ciudad] if col_ciudad in df.columns else []) + [mes_ant_col]].copy()
            df_fuga[mes_ant_col] = df_fuga[mes_ant_col].apply(lambda x: f"${x:,.0f}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"**Clientes en Fuga** en {mes_rec_label}: **{len(df_fuga)}**")
            st.caption(f"Compraron en {mes_ant_label} pero no en {mes_rec_label}.")
            if len(df_fuga) > 0:
                st.dataframe(df_fuga.rename(columns={
                    mes_ant_col: f"Última venta ({mes_ant_label})"
                }), hide_index=True, use_container_width=True)
            else:
                st.info("No hay clientes en fuga en este período.")

        else:
            st.info("Se necesitan al menos 2 meses de datos para calcular estas métricas.")

        st.divider()

        # ── Gráficas ─────────────────────────────────────────────────
        # ── Selector global de período para pestañas ────────────────
        st.subheader("Período de análisis")
        todos_pares_global = [(f"{m} {a}", m, c, a) for a in anios for m, c in data_por_anio[a]]
        opciones_periodo = [p[0] for p in todos_pares_global] + ["YTD"]
        # Mes actual como predeterminado
        from datetime import date
        mes_actual_label = MESES_ORDEN[date.today().month - 1]
        anio_actual = date.today().year
        default_label = f"{mes_actual_label} {anio_actual}"
        if default_label in opciones_periodo:
            idx_default_periodo = opciones_periodo.index(default_label)
        else:
            idx_default_periodo = len(opciones_periodo) - 1
        periodo_sel = st.selectbox("Selecciona el período a analizar en las pestañas (no aplica en Análisis por cliente)",
                                    opciones_periodo,
                                    index=idx_default_periodo,
                                    key="periodo_global")

        # Calcular columnas y valores según selección
        if periodo_sel == "YTD":
            # Usar todas las columnas dentro del rango YTD
            cols_periodo = []
            for a in anios:
                for m, c in data_por_anio[a]:
                    if MESES_ORDEN.index(m) + 1 <= mes_ytd:
                        cols_periodo.append(c)
            df["_venta_periodo"] = df[cols_periodo].sum(axis=1) if cols_periodo else 0
            periodo_label = f"YTD (Ene–{mes_ytd_label})"
        else:
            match = next((p for p in todos_pares_global if p[0] == periodo_sel), None)
            if match:
                _, mes_p, col_p, anio_p = match
                df["_venta_periodo"] = df[col_p]
                periodo_label = periodo_sel
            else:
                df["_venta_periodo"] = 0
                periodo_label = periodo_sel

        st.divider()

        tab_foda, tab3, tab4, tab6 = st.tabs(["Matriz FODA", "Top clientes", "Análisis por cliente", "Tabla completa"])

        with tab3:
            # YTD: para año actual hasta mes anterior al actual,
            # para años anteriores hasta el mismo mes para comparación justa
            for anio in anios:
                pares_todos = data_por_anio[anio]
                if not pares_todos:
                    continue
                if anio == max(anios):
                    # Año actual: solo hasta mes_ytd
                    cols_ytd = [c for m, c in pares_todos
                                if MESES_ORDEN.index(m) + 1 <= mes_ytd]
                else:
                    # Años anteriores: mismo rango que el año actual
                    cols_ytd = [c for m, c in pares_todos
                                if MESES_ORDEN.index(m) + 1 <= mes_ytd]
                df[f"YTD {anio}"] = df[cols_ytd].sum(axis=1) if cols_ytd else 0
            ytd_cols = [f"YTD {a}" for a in anios if f"YTD {a}" in df.columns]
            top = df.sort_values("_venta_periodo", ascending=True).tail(20)
            top_text = top["_venta_periodo"].apply(lambda x: f"${x:,.0f}")
            fig4 = px.bar(top, x="_venta_periodo", y=col_cliente, orientation="h",
                          title=f"Top 20 clientes — {periodo_label}",
                          text=top_text,
                          color="_venta_periodo", color_continuous_scale="Blues",
                          labels={"_venta_periodo": f"Ventas ({periodo_label})"})
            fig4.update_traces(textposition="outside")
            fig4.update_layout(height=600)
            st.plotly_chart(fig4, use_container_width=True)

            # Top 10 crecimiento solo disponible en YTD
            ultimo = f"YTD {anios[-1]}"
            if len(anios) >= 2 and ultimo in df.columns:
                ant = f"YTD {anios[-2]}"
                if ant in df.columns:
                    df["Crecimiento (%)"] = df.apply(
                        lambda r: ((r[ultimo]-r[ant])/r[ant]*100) if r[ant]>0 else 0, axis=1)
                    df["Var. absoluta ($)"] = df[ultimo] - df[ant]
                    st.subheader("Top 10 mayor crecimiento YoY")
                    tipo_orden = st.radio("Ordenar por:", ["Variación porcentual (%)", "Variación absoluta ($)"],
                                          horizontal=True, key="orden_crec")
                    col_orden = "Crecimiento (%)" if tipo_orden == "Variación porcentual (%)" else "Var. absoluta ($)"
                    cols_top = [col_cliente]+([col_ciudad] if col_ciudad in df.columns else [])+[ant, ultimo, "Crecimiento (%)", "Var. absoluta ($)"]
                    top_crec = df[df[ant]>0].sort_values(col_orden, ascending=False).head(10)
                    st.dataframe(top_crec[cols_top].style.format(
                        {ant:"${:,.0f}", ultimo:"${:,.0f}", "Crecimiento (%)":"{:+.1f}%", "Var. absoluta ($)":"${:+,.0f}"}),
                        hide_index=True, use_container_width=True)


        with tab4:
            st.info("El período de análisis no aplica en esta pestaña. Se muestra el detalle mes a mes del cliente seleccionado.")
            st.subheader("Ventas por cliente")

            # Selector de cliente
            clientes = sorted(df[col_cliente].unique().tolist())
            cliente_sel = st.selectbox("Selecciona un cliente", clientes)

            df_cli = df[df[col_cliente] == cliente_sel].copy()

            # Construir tabla de meses para el cliente seleccionado
            filas = []
            for anio in anios:
                pares = data_filtrada[anio]
                if not pares:
                    continue
                # YTD: acumular solo hasta el último mes disponible de ese año
                ytd_cli = 0
                ytd_prom = 0
                fila = {"Año": str(anio)}
                activos_mes = {}
                for m, c in pares:
                    val_cli = float(df_cli[c].sum()) if len(df_cli) > 0 else 0
                    # Promedio solo de clientes que compraron (> umbral)
                    compradores = df[df[c] >= umbral][c]
                    prom = float(compradores.mean()) if len(compradores) > 0 else 0
                    fila[m] = val_cli
                    fila[f"Prom {m}"] = prom
                    # Solo sumar al YTD si el mes está dentro del rango
                    mes_idx = MESES_ORDEN.index(m) + 1
                    en_ytd = mes_idx <= mes_ytd
                    if en_ytd:
                        ytd_cli += val_cli
                        ytd_prom += prom
                fila["YTD"] = ytd_cli
                fila["YTD Promedio"] = ytd_prom
                filas.append(fila)

            if filas:
                df_tabla = pd.DataFrame(filas).set_index("Año")

                # Separar columnas cliente vs promedio
                meses_cols = [m for m, _ in data_filtrada[anios[0]]] if data_filtrada[anios[0]] else []
                prom_cols  = [f"Prom {m}" for m in meses_cols]

                # Mostrar KPIs
                if len(filas) >= 2:
                    k1, k2, k3, k4 = st.columns(4)
                    ytd_ant = filas[-2]["YTD"]
                    ytd_act = filas[-1]["YTD"]
                    prom_ant = filas[-2]["YTD Promedio"]
                    prom_act = filas[-1]["YTD Promedio"]
                    var_cli = ((ytd_act - ytd_ant) / ytd_ant * 100) if ytd_ant > 0 else 0
                    var_prom = ((prom_act - prom_ant) / prom_ant * 100) if prom_ant > 0 else 0
                    k1.metric(f"YTD {anios[-2]}", f"${ytd_ant:,.0f}")
                    k2.metric(f"YTD {anios[-1]}", f"${ytd_act:,.0f}",
                              delta=f"{var_cli:+.1f}% vs año anterior")
                    k3.metric(f"Prom. compradores YTD {anios[-2]}", f"${prom_ant:,.0f}")
                    k4.metric(f"Prom. compradores YTD {anios[-1]}", f"${prom_act:,.0f}",
                              delta=f"{var_prom:+.1f}% vs año anterior")

                st.markdown("""
                <div style='border-top:1.5px solid #3ABFC4;border-bottom:0.5px solid #6DB33F;
                            margin:20px 0 8px;height:2px;background:linear-gradient(90deg,#3ABFC4,#6DB33F)'></div>
                """, unsafe_allow_html=True)

                # Tabla comparativa: cliente vs promedio
                for fila in filas:
                    anio = fila["Año"]
                    st.markdown(f"**{anio}**")
                    meses_disp = [m for m, _ in (data_filtrada[int(anio)] if int(anio) in data_filtrada else [])]
                    if not meses_disp:
                        continue

                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,#EAF7F7 0%,#F0F7EA 100%);
                                border:1px solid #3ABFC4;border-radius:10px;
                                padding:12px 8px;margin-bottom:12px;
                                box-shadow:0 2px 6px rgba(58,191,196,0.1)'>
                    """, unsafe_allow_html=True)

                    cols_tabla = st.columns(len(meses_disp) + 2)
                    with cols_tabla[0]:
                        st.markdown("<div style='font-size:13px;color:#3D3D3D;padding:4px 0'></div>", unsafe_allow_html=True)
                    for j, m in enumerate(meses_disp):
                        with cols_tabla[j+1]:
                            st.markdown(f"<div style='font-size:13px;font-weight:700;text-align:center;padding:4px 0;color:#3ABFC4'>{m}</div>", unsafe_allow_html=True)
                    with cols_tabla[-1]:
                        st.markdown("<div style='font-size:13px;font-weight:700;text-align:center;padding:4px 0;color:#6DB33F'>YTD</div>", unsafe_allow_html=True)

                    # Fila cliente
                    cols_v = st.columns(len(meses_disp) + 2)
                    with cols_v[0]:
                        st.markdown("<div style='font-size:13px;color:#3D3D3D;font-weight:600;padding:4px 0'>Cliente</div>", unsafe_allow_html=True)
                    for j, m in enumerate(meses_disp):
                        val = fila.get(m, 0)
                        color_v = "#3ABFC4" if val >= umbral else "#999"
                        with cols_v[j+1]:
                            st.markdown(f"<div style='text-align:center;font-size:15px;font-weight:600;color:{color_v};padding:3px 0'>${val:,.0f}</div>", unsafe_allow_html=True)
                    with cols_v[-1]:
                        st.markdown(f"<div style='text-align:center;font-size:15px;font-weight:700;color:#6DB33F;padding:3px 0'>${fila.get('YTD',0):,.0f}</div>", unsafe_allow_html=True)

                    # Fila promedio
                    cols_p = st.columns(len(meses_disp) + 2)
                    with cols_p[0]:
                        st.markdown("<div style='font-size:13px;color:#3D3D3D;padding:4px 0'>Prom. compradores</div>", unsafe_allow_html=True)
                    for j, m in enumerate(meses_disp):
                        val = fila.get(f"Prom {m}", 0)
                        with cols_p[j+1]:
                            st.markdown(f"<div style='text-align:center;font-size:14px;color:#666;padding:3px 0'>${val:,.0f}</div>", unsafe_allow_html=True)
                    with cols_p[-1]:
                        st.markdown(f"<div style='text-align:center;font-size:14px;color:#666;padding:3px 0'>${fila.get('YTD Promedio',0):,.0f}</div>", unsafe_allow_html=True)

                    # Fila diferencia
                    cols_d = st.columns(len(meses_disp) + 2)
                    with cols_d[0]:
                        st.markdown("<div style='font-size:13px;color:#3D3D3D;padding:4px 0;border-top:1px solid #3ABFC4;margin-top:4px'>Dif. vs prom.</div>", unsafe_allow_html=True)
                    for j, m in enumerate(meses_disp):
                        cli_v = fila.get(m, 0)
                        prom_v = fila.get(f"Prom {m}", 0)
                        dif = cli_v - prom_v
                        col_d = "#27AE60" if dif >= 0 else "#E74C3C"
                        with cols_d[j+1]:
                            st.markdown(f"<div style='text-align:center;font-size:13px;font-weight:600;color:{col_d};padding:3px 0;border-top:1px solid #3ABFC4;margin-top:4px'>{dif:+,.0f}</div>", unsafe_allow_html=True)
                    ytd_dif = fila.get("YTD", 0) - fila.get("YTD Promedio", 0)
                    col_ytd_d = "#27AE60" if ytd_dif >= 0 else "#E74C3C"
                    with cols_d[-1]:
                        st.markdown(f"<div style='text-align:center;font-size:13px;font-weight:600;color:{col_ytd_d};padding:3px 0;border-top:1px solid #3ABFC4;margin-top:4px'>{ytd_dif:+,.0f}</div>", unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No hay datos para este cliente con los meses seleccionados.")

        with tab_foda:
            st.subheader("Matriz FODA de Clientes")
            st.caption("Eje X: posición vs promedio de la ciudad | Eje Y: variación vs período anterior")

            # Calcular métricas para FODA usando selector de pestañas
            todos_pares_foda = [(m, c) for a in anios for m, c in data_por_anio[a]]
            if len(todos_pares_foda) >= 2:
                # Encontrar el mes anterior al seleccionado en el selector
                if periodo_sel == "YTD":
                    mes_foda_label = f"YTD {mes_ytd_label}"
                    mes_foda_col = None  # usaremos _venta_periodo
                    mes_prev_label, mes_prev_col = todos_pares_foda[-2]
                else:
                    match_foda = next((p for p in todos_pares_global if p[0] == periodo_sel), None)
                    if match_foda:
                        _, mes_foda_label, mes_foda_col, _ = match_foda
                        idx_foda = todos_pares_foda.index((mes_foda_label, mes_foda_col))
                        if idx_foda > 0:
                            mes_prev_label, mes_prev_col = todos_pares_foda[idx_foda - 1]
                        else:
                            mes_prev_label, mes_prev_col = todos_pares_foda[0]
                    else:
                        mes_foda_label, mes_foda_col = todos_pares_foda[-1]
                        mes_prev_label, mes_prev_col = todos_pares_foda[-2]

                df_foda = df[[col_cliente] + ([col_ciudad] if col_ciudad in df.columns else [])].copy()
                df_foda["vta_actual"] = df["_venta_periodo"]
                df_foda["vta_prev"]   = df[mes_prev_col]
                df_foda = df_foda[df_foda["vta_actual"] >= umbral].copy()

                if col_ciudad in df.columns:
                    prom_ciudad = df_foda.groupby(col_ciudad)["vta_actual"].mean().to_dict()
                    df_foda["prom_ciudad"] = df_foda[col_ciudad].map(prom_ciudad)
                else:
                    df_foda["prom_ciudad"] = df_foda["vta_actual"].mean()

                df_foda["var_pct"] = df_foda.apply(
                    lambda r: ((r["vta_actual"] - r["vta_prev"]) / r["vta_prev"] * 100)
                    if r["vta_prev"] >= umbral else 0, axis=1)
                df_foda["vs_prom"] = df_foda["vta_actual"] - df_foda["prom_ciudad"]

                # Categorizar
                def categorizar(row):
                    sobre = row["vs_prom"] >= 0
                    crece = row["var_pct"] >= 0
                    if sobre and crece:     return "Fortaleza"
                    if not sobre and crece: return "Oportunidad"
                    if sobre and not crece: return "Amenaza"
                    return "Debilidad"

                df_foda["categoria"] = df_foda.apply(categorizar, axis=1)

                color_map = {
                    "Fortaleza":   "#6DB33F",
                    "Oportunidad": "#3ABFC4",
                    "Debilidad":   "#F4C430",
                    "Amenaza":     "#E67E22"
                }

                # Resumen conteos
                conteos = df_foda["categoria"].value_counts()
                c1, c2, c3, c4 = st.columns(4)
                for col_m, cat, emoji in [(c1,"Fortaleza","💪"),(c2,"Oportunidad","🔵"),(c3,"Amenaza","⚠️"),(c4,"Debilidad","⚡")]:
                    with col_m:
                        n = conteos.get(cat, 0)
                        col_bg = color_map[cat]
                        st.markdown(f"""<div style='background:{col_bg};color:white;text-align:center;
                            padding:12px;border-radius:8px;font-weight:600'>
                            {emoji} {cat}<br><span style='font-size:24px'>{n}</span>
                            </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Gráfica scatter
                fig_foda = px.scatter(
                    df_foda, x="vs_prom", y="var_pct",
                    color="categoria",
                    color_discrete_map=color_map,
                    hover_name=col_cliente,
                    hover_data={"vta_actual": ":,.0f", "var_pct": ":.1f", "vs_prom": False},
                    labels={"vs_prom": "Posición vs promedio ciudad",
                            "var_pct": "Variación vs mes anterior (%)",
                            "categoria": "Categoría",
                            "vta_actual": f"Venta {mes_foda_label}"},
                    title=f"Matriz FODA — {periodo_label}",
                    size="vta_actual",
                    size_max=40,
                )
                fig_foda.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="white")))
                fig_foda.add_hline(y=0, line_dash="dot", line_color="#555", line_width=2)
                fig_foda.add_vline(x=0, line_dash="dot", line_color="#555", line_width=2)
                fig_foda.add_annotation(x=0.02, y=0.98, xref="paper", yref="paper",
                    text="Oportunidades", showarrow=False, font=dict(color="#3ABFC4", size=12, family="Arial Black"))
                fig_foda.add_annotation(x=0.98, y=0.98, xref="paper", yref="paper",
                    text="Fortalezas", showarrow=False, font=dict(color="#6DB33F", size=12, family="Arial Black"),
                    xanchor="right")
                fig_foda.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper",
                    text="Debilidades", showarrow=False, font=dict(color="#B8860B", size=12, family="Arial Black"))
                fig_foda.add_annotation(x=0.98, y=0.02, xref="paper", yref="paper",
                    text="Amenazas", showarrow=False, font=dict(color="#E67E22", size=12, family="Arial Black"),
                    xanchor="right")
                fig_foda.update_xaxes(showticklabels=False, zeroline=False)
                fig_foda.update_yaxes(zeroline=False)
                fig_foda.update_layout(height=560, plot_bgcolor="#FAFAFA",
                                       paper_bgcolor="white",
                                       legend=dict(orientation="h", y=-0.15))
                st.plotly_chart(fig_foda, use_container_width=True)

                # Tabla detalle por categoría
                for cat in ["Fortaleza", "Oportunidad", "Amenaza", "Debilidad"]:
                    grupo = df_foda[df_foda["categoria"] == cat][[
                        col_cliente] + ([col_ciudad] if col_ciudad in df.columns else []) +
                        ["vta_actual", "vta_prev", "var_pct", "vs_prom"]
                    ].sort_values("vta_actual", ascending=False).copy()
                    grupo = grupo.rename(columns={
                        "vta_actual": f"Venta {mes_foda_label}",
                        "vta_prev":   f"Venta {mes_prev_label}",
                        "var_pct":    "Var. (%)",
                        "vs_prom":    "Dif. vs prom. ciudad"
                    })
                    if len(grupo) > 0:
                        with st.expander(f"{cat}s ({len(grupo)} clientes)", expanded=False):
                            st.dataframe(grupo.style.format({
                                f"Venta {mes_foda_label}": "${:,.0f}",
                                f"Venta {mes_prev_label}": "${:,.0f}",
                                "Var. (%)":               "{:+.1f}%",
                                "Dif. vs prom. ciudad":   "${:+,.0f}"
                            }), hide_index=True, use_container_width=True)
            else:
                st.info("Se necesitan al menos 2 meses para generar la matriz FODA.")

        with tab6:
            cols_base = [c for c in [col_cliente, col_ciudad] if c in df.columns]
            cols_venta = [c for _, c in sorted(cols_ventas.items())]
            cols_ytd = [c for c in df.columns if c.startswith("YTD")]
            df[f"Ventas {periodo_label}"] = df["_venta_periodo"]
            tabla = df[cols_base + cols_venta + cols_ytd + [f"Ventas {periodo_label}"]]
            st.dataframe(tabla, hide_index=True, use_container_width=True)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                tabla.to_excel(writer, index=False, sheet_name="Datos")
            st.download_button("Descargar en Excel", data=buffer.getvalue(),
                               file_name="resultados_megalens.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)
else:
    st.info("Sube tu archivo Excel para comenzar. Columnas de ventas deben tener formato Mes-Año (ej: ene-25, feb-26).")
