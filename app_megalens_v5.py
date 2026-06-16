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
                    <span style='color:#3ABFC4'>Mega</span><span style='background:linear-gradient(90deg,#6DB33F,#3ABFC4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text'> Analytics</span>
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
        <div style='width:64px;height:64px;margin:0 auto 8px;
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
        <h1 style='color:rgba(255,255,255,0.55);margin:0;font-size:40px;font-weight:800;letter-spacing:2px;line-height:1'>
            Megalens
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
    with st.expander("⚙️ Configuración", expanded=False):
        col_cliente = st.text_input("Columna de cliente", value="Cliente")
        col_ciudad  = st.text_input("Columna de ciudad",  value="Ciudad")
        umbral      = st.number_input("Umbral mínimo ($)", value=10000, step=1000)
        col_hoja    = st.text_input("Hoja del Excel (vacío = primera hoja)", value="")

# ── Modo de carga ────────────────────────────────────────────
modo = st.radio("¿Cómo quieres cargar tu base de datos?",
                ["Base consolidada (un solo archivo)", "Bases separadas por año (2025 + 2026)"],
                horizontal=True, key="modo_carga")

COLS_BASE = ["Cliente", "Ciudad", "Zona", "Mensajero"]

def preparar_base(df_raw, anio, col_cli="Cliente"):
    df_raw.columns = df_raw.columns.str.strip()
    # Detectar columnas de meses (sin año) como Ene, Feb, Mar...
    cols_meses = [c for c in df_raw.columns if c.capitalize() in MESES_ORDEN]
    cols_info  = [c for c in df_raw.columns if c in COLS_BASE]
    df_out = df_raw[cols_info + cols_meses].copy()
    # Renombrar meses a formato Mes-AA
    sufijo = str(anio)[-2:]
    rename_map = {m: f"{m.capitalize()}-{sufijo}" for m in cols_meses}
    df_out = df_out.rename(columns=rename_map)
    df_out[col_cli] = df_out[col_cli].fillna("").astype(str).str.strip()
    df_out = df_out[df_out[col_cli] != ""]
    # Limpiar numéricos
    for c in [rename_map[m] for m in cols_meses]:
        df_out[c] = pd.to_numeric(
            df_out[c].astype(str).str.replace(r"[\$\s,]", "", regex=True).str.strip().replace(["", "-"], "0"),
            errors="coerce"
        ).fillna(0)
    return df_out

if modo == "Bases separadas por año (2025 + 2026)":
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("**Base 2025**")
        archivo_25 = st.file_uploader("Sube el Excel de 2025", type=["xlsx"], key="up25")
        hoja_25 = st.text_input("Hoja 2025 (vacío = primera)", value="", key="hoja25")
    with col_u2:
        st.markdown("**Base 2026**")
        archivo_26 = st.file_uploader("Sube el Excel de 2026", type=["xlsx"], key="up26")
        hoja_26 = st.text_input("Hoja 2026 (vacío = primera)", value="", key="hoja26")

    archivo = None
    if archivo_25 and archivo_26:
        try:
            h25 = hoja_25.strip() if hoja_25.strip() else 0
            h26 = hoja_26.strip() if hoja_26.strip() else 0
            raw25 = pd.read_excel(archivo_25, sheet_name=h25)
            raw26 = pd.read_excel(archivo_26, sheet_name=h26)
            df25 = preparar_base(raw25, 2025)
            df26 = preparar_base(raw26, 2026)

            # Full outer merge por Cliente
            cols_info_25 = [c for c in df25.columns if c in COLS_BASE]
            cols_info_26 = [c for c in df26.columns if c in COLS_BASE]
            meses_25 = [c for c in df25.columns if c not in COLS_BASE]
            meses_26 = [c for c in df26.columns if c not in COLS_BASE]

            df_merged = pd.merge(
                df25, df26[["Cliente"] + meses_26],
                on="Cliente", how="outer"
            )
            # Rellenar NaN en meses
            for c in meses_25 + meses_26:
                if c in df_merged.columns:
                    df_merged[c] = df_merged[c].fillna(0)
            # Rellenar info de ciudad/zona/mensajero
            for c in ["Ciudad", "Zona", "Mensajero"]:
                if c in df_merged.columns:
                    df_merged[c] = df_merged[c].fillna("")

            st.success(f"Bases combinadas: {len(df_merged):,} clientes | {len(meses_25)} meses 2025 + {len(meses_26)} meses 2026")

            # Guardar en buffer para reutilizar
            buffer_merged = io.BytesIO()
            df_merged.to_excel(buffer_merged, index=False)
            buffer_merged.seek(0)
            archivo = buffer_merged
            col_hoja = ""
        except Exception as e:
            st.error(f"Error al combinar bases: {e}")
            st.exception(e)
    elif archivo_25 or archivo_26:
        st.info("Sube ambos archivos para combinar las bases.")
else:
    archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"], key="up_consolidado")

if archivo:
    try:
        hoja = col_hoja if col_hoja.strip() else 0
        if isinstance(archivo, io.BytesIO):
            df = pd.read_excel(archivo)
        else:
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
        # ── Gráfico Tendencia YTD ────────────────────────────────
        st.subheader("Tendencia YTD — Ventas vs Variación")

        todos_pares_ytd = [(m, c, a) for a in anios for m, c in data_por_anio[a]]

        # Separar por año
        pares_26 = [(m, c) for m, c, a in todos_pares_ytd if a == max(anios)]
        pares_25 = {m: c for m, c, a in todos_pares_ytd if a == min(anios)}

        if not pares_26:
            st.info("Se necesitan datos de al menos 2 años para esta vista.")
        else:
            meses_graf = []
            ventas_26  = []
            var_pct    = []
            labels_x   = []

            for m, c in pares_26:
                vta26 = df[c].sum()
                col25 = pares_25.get(m)
                vta25 = df[col25].sum() if col25 else 0
                var   = ((vta26 - vta25) / vta25 * 100) if vta25 > 0 else 0
                anio_label = max(anios)
                labels_x.append(f"{m} {anio_label}")
                ventas_26.append(vta26)
                var_pct.append(round(var, 1))

            # KPIs
            ytd_total_26 = sum(ventas_26[:mes_ytd])
            ytd_total_25 = sum(
                df[pares_25[m]].sum() if m in pares_25 else 0
                for m, _ in pares_26[:mes_ytd]
            )
            var_ytd = ((ytd_total_26 - ytd_total_25) / ytd_total_25 * 100) if ytd_total_25 > 0 else 0

            k1, k2 = st.columns(2)
            color_var = "#27AE60" if var_ytd >= 0 else "#E74C3C"
            k1.markdown(f"""
            <div style='background:linear-gradient(135deg,#0D2E35,#1A5C6B);
                padding:16px;border-radius:10px;text-align:center;'>
                <p style='color:rgba(255,255,255,0.6);margin:0;font-size:12px;letter-spacing:2px;text-transform:uppercase'>Var % Vtas YTD</p>
                <p style='color:{color_var};margin:4px 0 0;font-size:28px;font-weight:800'>{var_ytd:+.1f}%</p>
            </div>""", unsafe_allow_html=True)
            k2.markdown(f"""
            <div style='background:linear-gradient(135deg,#0D2E35,#1E7A3E);
                padding:16px;border-radius:10px;text-align:center;'>
                <p style='color:rgba(255,255,255,0.6);margin:0;font-size:12px;letter-spacing:2px;text-transform:uppercase'>Ventas YTD</p>
                <p style='color:#3ABFC4;margin:4px 0 0;font-size:28px;font-weight:800'>${ytd_total_26/1e6:.1f} Mill</p>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gráfico combinado
            fig_ytd = go.Figure()

            # Barras variación
            colores_barras = ["#3ABFC4" if v >= 0 else "#E74C3C" for v in var_pct]
            fig_ytd.add_trace(go.Bar(
                x=labels_x, y=var_pct,
                name="Var % Vtas",
                marker_color=colores_barras,
                opacity=0.85,
                text=[f"{v:+.1f}%" for v in var_pct],
                textposition="inside",
                textfont=dict(color="white", size=11, family="Arial Bold"),
                yaxis="y1"
            ))

            # Línea ventas
            fig_ytd.add_trace(go.Scatter(
                x=labels_x, y=ventas_26,
                name="Ventas",
                mode="lines+markers+text",
                line=dict(color="#1A5C6B", width=2.5),
                marker=dict(size=8, color="#1A5C6B",
                            line=dict(width=2, color="white")),
                text=[f"{v/1e6:.1f} mill." for v in ventas_26],
                textposition="top center",
                textfont=dict(size=10, color="#1A5C6B"),
                yaxis="y2"
            ))

            fig_ytd.update_layout(
                title="Var % Vtas y Ventas por Mes",
                xaxis=dict(title="Mes", tickangle=-30),
                yaxis=dict(title="Var % Vtas", zeroline=True,
                           zerolinecolor="#999", zerolinewidth=1.5,
                           ticksuffix="%"),
                yaxis2=dict(title="Ventas ($)", overlaying="y", side="right",
                            showgrid=False, tickprefix="$"),
                legend=dict(orientation="h", y=1.12),
                plot_bgcolor="#FAFAFA",
                paper_bgcolor="white",
                height=500,
                bargap=0.35,
                hovermode="x unified"
            )
            st.plotly_chart(fig_ytd, use_container_width=True)

        st.divider()

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

            # Clientes activos 2 meses consecutivos recientes
            if idx_ref >= 1:
                mes_ant2_label, mes_ant2_col = todos_pares[idx_ref - 1]
                compro_ant2 = df[mes_ant2_col] >= umbral
                mask_2m = compro_reciente & compro_ant2
            else:
                mask_2m = pd.Series([False] * len(df), index=df.index)

            # Clientes en fuga
            mask_fuga = compro_ant & ~compro_reciente

            # Construir dataframes con valores numéricos para ordenamiento correcto
            cols_base_df = [col_cliente] + ([col_ciudad] if col_ciudad in df.columns else [])

            df_nuevos    = df[mask_nuevos][cols_base_df + [mes_rec_col]].copy()
            df_retomados = df[mask_retomados][cols_base_df + [mes_rec_col]].copy()
            df_2m        = df[mask_2m][cols_base_df + [mes_ant_col, mes_rec_col]].copy()
            df_fuga      = df[mask_fuga][cols_base_df + [mes_ant_col]].copy()

            # Renombrar columnas
            df_nuevos    = df_nuevos.rename(columns={mes_rec_col: f"Venta {mes_rec_label}"})
            df_retomados = df_retomados.rename(columns={mes_rec_col: f"Venta {mes_rec_label}"})
            df_2m        = df_2m.rename(columns={mes_ant_col: f"Venta {mes_ant_label}", mes_rec_col: f"Venta {mes_rec_label}"})
            df_2m["Var. valor ($)"] = df_2m[f"Venta {mes_rec_label}"] - df_2m[f"Venta {mes_ant_label}"]
            df_fuga      = df_fuga.rename(columns={mes_ant_col: f"Última venta ({mes_ant_label})"})

            # Metas por categoría
            st.markdown("**Metas por categoría** (opcional)")
            mc1, mc2, mc3, mc4 = st.columns(4)
            with mc1: meta_nuevos   = st.number_input("Meta Nuevos",    min_value=0, value=0, step=1, key="meta_n")
            with mc2: meta_activos  = st.number_input("Meta Activos 2m",min_value=0, value=0, step=1, key="meta_a")
            with mc3: meta_retomados= st.number_input("Meta Retomados", min_value=0, value=0, step=1, key="meta_r")
            with mc4: meta_fuga     = st.number_input("Meta Fuga",      min_value=0, value=0, step=1, key="meta_f")

            st.markdown("<br>", unsafe_allow_html=True)

            col_venta_n = f"Venta {mes_rec_label}"
            col_venta_r = f"Venta {mes_rec_label}"
            col_venta_2m_ant = f"Venta {mes_ant_label}"
            col_venta_2m_rec = f"Venta {mes_rec_label}"
            col_venta_f = f"Última venta ({mes_ant_label})"

            def header_cuadrante(n, meta, color, emoji, titulo, caption, n_ant=None):
                vs_meta = f" · Meta: {meta}" if meta > 0 else ""
                cumple = "✅" if meta > 0 and n >= meta else ("❌" if meta > 0 else "")
                ant_txt = f"<span style='color:#999;font-size:11px;margin-left:8px'>ant: {n_ant}</span>" if n_ant is not None else ""
                return f"""<div style='background:{color}22;border:2px solid {color};
                    border-radius:10px;padding:10px 14px;margin-bottom:8px'>
                    <div style='display:flex;justify-content:space-between;align-items:center'>
                        <span style='color:{color};font-size:15px;font-weight:700'>{emoji} {titulo}</span>
                        <span style='color:{color};font-size:20px;font-weight:800'>{n} {cumple}{ant_txt}</span>
                    </div>
                    <p style='color:#666;font-size:12px;margin:4px 0 0'>{caption}{vs_meta}</p>
                </div>"""

            # Calcular conteos del mes anterior para referencia
            if idx_ref >= 2:
                mes_prev2_label, mes_prev2_col = todos_pares[idx_ref - 2]
                compro_prev2 = df[mes_prev2_col] >= umbral
                # Nuevos mes anterior: compraron en ant pero no en los 3 antes de ant
                meses_3_ant_prev = todos_pares[max(0, idx_ref-4):idx_ref-1]
                if meses_3_ant_prev:
                    no_c3_prev = pd.Series([True]*len(df), index=df.index)
                    for _, cc in meses_3_ant_prev:
                        no_c3_prev = no_c3_prev & (df[cc] < umbral)
                    mask_nuevos_ant = compro_ant & no_c3_prev
                else:
                    mask_nuevos_ant = compro_ant & ~compro_prev2
                mask_retomados_ant = compro_ant & ~compro_prev2 & ~mask_nuevos_ant
                mask_2m_ant = compro_ant & compro_prev2
                mask_fuga_ant = compro_prev2 & ~compro_ant
                n_ant_nuevos    = mask_nuevos_ant.sum()
                n_ant_activos   = mask_2m_ant.sum()
                n_ant_retomados = mask_retomados_ant.sum()
                n_ant_fuga      = mask_fuga_ant.sum()
            else:
                n_ant_nuevos = n_ant_activos = n_ant_retomados = n_ant_fuga = None

            q1, q2 = st.columns(2)
            q3, q4 = st.columns(2)

            with q1:
                st.markdown(header_cuadrante(len(df_nuevos), meta_nuevos, "#6DB33F", "🆕", "Clientes Nuevos",
                    f"Compraron en {mes_rec_label} pero no en los 3 meses anteriores.", n_ant=n_ant_nuevos), unsafe_allow_html=True)
                if len(df_nuevos) > 0:
                    st.dataframe(df_nuevos.style.format({col_venta_n: "${:,.0f}"}),
                                 hide_index=True, use_container_width=True, height=220)
                else:
                    st.info("Sin clientes nuevos.")

            with q2:
                st.markdown(header_cuadrante(len(df_2m), meta_activos, "#3ABFC4", "⭐", "Activos 2 Meses",
                    f"Compraron tanto en {mes_ant_label} como en {mes_rec_label}.", n_ant=n_ant_activos), unsafe_allow_html=True)
                if len(df_2m) > 0:
                    st.dataframe(df_2m.style.format({
                        col_venta_2m_ant: "${:,.0f}",
                        col_venta_2m_rec: "${:,.0f}",
                        "Var. valor ($)": "${:+,.0f}"
                    }), hide_index=True, use_container_width=True, height=220)
                else:
                    st.info("Sin clientes activos 2 meses.")

            with q3:
                st.markdown(header_cuadrante(len(df_retomados), meta_retomados, "#8E44AD", "🔄", "Clientes Retomados",
                    f"No compraron en {mes_ant_label} pero sí en {mes_rec_label}.", n_ant=n_ant_retomados), unsafe_allow_html=True)
                if len(df_retomados) > 0:
                    st.dataframe(df_retomados.style.format({col_venta_r: "${:,.0f}"}),
                                 hide_index=True, use_container_width=True, height=220)
                else:
                    st.info("Sin clientes retomados.")

            with q4:
                st.markdown(header_cuadrante(len(df_fuga), meta_fuga, "#E67E22", "⚠️", "Clientes en Fuga",
                    f"Compraron en {mes_ant_label} pero no en {mes_rec_label}.", n_ant=n_ant_fuga), unsafe_allow_html=True)
                if len(df_fuga) > 0:
                    st.dataframe(df_fuga.style.format({col_venta_f: "${:,.0f}"}),
                                 hide_index=True, use_container_width=True, height=220)
                else:
                    st.info("Sin clientes en fuga.")

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

        tab3, tab4, tab6 = st.tabs(["Top clientes", "Análisis por cliente", "Tabla completa"])

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

                    # Construir dataframe para mostrar con formato limpio
                    filas_tabla = {"": ["Cliente", "Prom. compradores", "Dif. vs prom."]}
                    for m in meses_disp:
                        cli_v  = fila.get(m, 0)
                        prom_v = fila.get(f"Prom {m}", 0)
                        dif    = cli_v - prom_v
                        filas_tabla[m] = [
                            f"${cli_v:,.0f}",
                            f"${prom_v:,.0f}",
                            f"{dif:+,.0f}"
                        ]
                    ytd_v   = fila.get("YTD", 0)
                    ytd_p   = fila.get("YTD Promedio", 0)
                    ytd_dif = ytd_v - ytd_p
                    filas_tabla["YTD"] = [
                        f"${ytd_v:,.0f}",
                        f"${ytd_p:,.0f}",
                        f"{ytd_dif:+,.0f}"
                    ]
                    df_display = pd.DataFrame(filas_tabla).set_index("")

                    def color_fila(row):
                        styles = []
                        for v in row:
                            if row.name == "Cliente":
                                styles.append("color:#3ABFC4;font-weight:600")
                            elif row.name == "Dif. vs prom.":
                                try:
                                    num = float(str(v).replace(",","").replace("+","").replace("$",""))
                                    styles.append("color:#27AE60;font-weight:600" if num >= 0 else "color:#E74C3C;font-weight:600")
                                except:
                                    styles.append("")
                            else:
                                styles.append("color:#555")
                        return styles

                    st.dataframe(
                        df_display.style.apply(color_fila, axis=1),
                        use_container_width=True
                    )
            else:
                st.info("No hay datos para este cliente con los meses seleccionados.")


            pass  # contenido manejado arriba en sección de clientes
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
                # Tabla de cuadrantes FODA
                col_q1, col_q2 = st.columns(2)
                col_q3, col_q4 = st.columns(2)

                def tabla_cuadrante(col_widget, cat, color_bg, color_border, emoji):
                    grupo = df_foda[df_foda["categoria"] == cat][[
                        col_cliente] + ([col_ciudad] if col_ciudad in df.columns else []) +
                        ["vta_actual", "var_pct"]
                    ].sort_values("vta_actual", ascending=False).copy()
                    grupo = grupo.rename(columns={
                        "vta_actual": f"Venta {mes_foda_label}",
                        "var_pct": "Var. vs mes ant. (%)"
                    })
                    with col_widget:
                        st.markdown(f"""
                        <div style='background:{color_bg};border:2px solid {color_border};
                            border-radius:10px;padding:12px;margin-bottom:8px'>
                            <h4 style='color:{color_border};margin:0;font-size:15px'>
                                {emoji} {cat}s <span style='font-size:12px;font-weight:400'>({len(grupo)} clientes)</span>
                            </h4>
                        </div>""", unsafe_allow_html=True)
                        if len(grupo) > 0:
                            st.dataframe(grupo.style.format({
                                f"Venta {mes_foda_label}": "${:,.0f}",
                                "Var. vs mes ant. (%)": "{:+.1f}%"
                            }), hide_index=True, use_container_width=True, height=220)
                        else:
                            st.info(f"Sin clientes en {cat}.")

                tabla_cuadrante(col_q1, "Oportunidad", "#EAF7F7", "#3ABFC4", "🔵")
                tabla_cuadrante(col_q2, "Fortaleza",   "#EAF3DE", "#6DB33F", "💪")
                tabla_cuadrante(col_q3, "Debilidad",   "#FEFAE0", "#B8860B", "⚡")
                tabla_cuadrante(col_q4, "Amenaza",     "#FEF0E7", "#E67E22", "⚠️")

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
