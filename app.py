import streamlit as st
import pandas as pd
import json
import os

# Configuración de la página
st.set_page_config(page_title="🏆 Quiniela Pro Mundial 2026", layout="centered")

DATA_FILE = "quiniela_pro_data.json"

# Inicialización de la base de datos con los 19 partidos reales
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "partidos": [
                {"id": 1, "fecha": "03/07", "fase": "16vos", "eq1": "Australia", "eq2": "Egipto", "goles_eq1": None, "goles_eq2": None},
                {"id": 2, "fecha": "03/07", "fase": "16vos", "eq1": "Argentina", "eq2": "Cabo Verde", "goles_eq1": None, "goles_eq2": None},
                {"id": 3, "fecha": "03/07", "fase": "16vos", "eq1": "Colombia", "eq2": "Ghana", "goles_eq1": None, "goles_eq2": None},
                {"id": 4, "fecha": "04/07", "fase": "Octavos 1", "eq1": "Canadá", "eq2": "Marruecos", "goles_eq1": None, "goles_eq2": None},
                {"id": 5, "fecha": "04/07", "fase": "Octavos 2", "eq1": "Paraguay", "eq2": "Francia", "goles_eq1": None, "goles_eq2": None},
                {"id": 6, "fecha": "05/07", "fase": "Octavos 3", "eq1": "Brasil", "eq2": "Noruega", "goles_eq1": None, "goles_eq2": None},
                {"id": 7, "fecha": "05/07", "fase": "Octavos 4", "eq1": "México", "eq2": "Inglaterra", "goles_eq1": None, "goles_eq2": None},
                {"id": 8, "fecha": "06/07", "fase": "Octavos 5", "eq1": "Ganador POR/CRO", "eq2": "Ganador ESP/AUT", "goles_eq1": None, "goles_eq2": None},
                {"id": 9, "fecha": "06/07", "fase": "Octavos 6", "eq1": "Estados Unidos", "eq2": "Bélgica", "goles_eq1": None, "goles_eq2": None},
                {"id": 10, "fecha": "07/07", "fase": "Octavos 7", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 11, "fecha": "07/07", "fase": "Octavos 8", "eq1": "Ganador SUI/ALG", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 12, "fecha": "09/07", "fase": "Cuartos 1", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 13, "fecha": "10/07", "fase": "Cuartos 2", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 14, "fecha": "11/07", "fase": "Cuartos 3", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 15, "fecha": "11/07", "fase": "Cuartos 4", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 16, "fecha": "14/07", "fase": "Semifinal 1", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 17, "fecha": "15/07", "fase": "Semifinal 2", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 18, "fecha": "18/07", "fase": "3er Lugar", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 19, "fecha": "19/07", "fase": "FINAL", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None}
            ],
            "jugadores": {}
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def resolver_llaves(partidos):
    p_map = {p["id"]: p for p in partidos}
    def get_winner(pid):
        p = p_map[pid]
        if p["goles_eq1"] is None or p["goles_eq2"] is None: return None
        if p["goles_eq1"] > p["goles_eq2"]: return p["eq1"]
        if p["goles_eq2"] > p["goles_eq1"]: return p["eq2"]
        return p.get("ganador_manual", None)
    
    def get_loser(pid):
        p = p_map[pid]
        if p["goles_eq1"] is None or p["goles_eq2"] is None: return None
        if p["goles_eq1"] < p["goles_eq2"]: return p["eq1"]
        if p["goles_eq2"] < p["goles_eq1"]: return p["eq1"]
        return p.get("perdedor_manual", None)

    if get_winner(2): p_map[10]["eq1"] = get_winner(2)
    if get_winner(1): p_map[10]["eq2"] = get_winner(1)
    if get_winner(3): p_map[11]["eq2"] = get_winner(3)
    if get_winner(6): p_map[12]["eq1"] = get_winner(6)
    if get_winner(5): p_map[12]["eq2"] = get_winner(5)
    if get_winner(10): p_map[13]["eq1"] = get_winner(10)
    if get_winner(11): p_map[13]["eq2"] = get_winner(11)
    if get_winner(7): p_map[14]["eq1"] = get_winner(7)
    if get_winner(8): p_map[14]["eq2"] = get_winner(8)
    if get_winner(4): p_map[15]["eq1"] = get_winner(4)
    if get_winner(9): p_map[15]["eq2"] = get_winner(9)
    if get_winner(12): p_map[16]["eq1"] = get_winner(12)
    if get_winner(13): p_map[16]["eq2"] = get_winner(13)
    if get_winner(14): p_map[17]["eq1"] = get_winner(14)
    if get_winner(15): p_map[17]["eq2"] = get_winner(15)
    if get_loser(16): p_map[18]["eq1"] = get_loser(16)
    if get_loser(17): p_map[18]["eq2"] = get_loser(17)
    if get_winner(16): p_map[19]["eq1"] = get_winner(16)
    if get_winner(17): p_map[19]["eq2"] = get_winner(17)

data = load_data()
resolver_llaves(data["partidos"])

st.title("🏆 Quiniela Pro Mundial 2026")
st.write("---")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard Completo", "📝 Mis Predicciones", "⚙️ Panel Admin"])

# --- PESTAÑA 1: DASHBOARD COMPLETO ---
with tab1:
    st.subheader("Leaderboard General (Desempate por Plenos)")
    ranking = []
    
    for jugador, info in data["jugadores"].items():
        if not info.get("aprobado", False): continue
        puntos = 0
        plenos = 0
        preds = info.get("predicciones", {})
        
        for p in data["partidos"]:
            pid = str(p["id"])
            if p["goles_eq1"] is not None and pid in preds:
                r1, r2 = p["goles_eq1"], p["goles_eq2"]
                pred1, pred2 = preds[pid]["eq1"], preds[pid]["eq2"]
                if r1 == pred1 and r2 == pred2:
                    puntos += 3
                    plenos += 1
                elif (r1 > r2 and pred1 > pred2) or (r1 < r2 and pred1 < pred2) or (r1 == r2 and pred1 == pred2):
                    puntos += 1
        ranking.append({"Jugador": jugador, "Puntos Totales": puntos, "Plenos (3 pts)": plenos})
    
    if ranking:
        df_rank = pd.DataFrame(ranking).sort_values(by=["Puntos Totales", "Plenos (3 pts)"], ascending=[False, False]).reset_index(drop=True)
        df_rank.index += 1
        st.dataframe(df_rank, use_container_width=True)
        
        st.write("---")
        st.subheader("🔍 Auditoría y Detalle por Jugador")
        j_select = st.selectbox("Selecciona un jugador para auditar sus puntos:", df_rank["Jugador"].tolist())
        
        if j_select:
            detalle_data = []
            player_preds = data["jugadores"][j_select]["predicciones"]
            for p in data["partidos"]:
                pid = str(p["id"])
                p_text = f"{p['eq1']} vs {p['eq2']}"
                real_text = f"{p['goles_eq1']} - {p['goles_eq2']}" if p["goles_eq1"] is not None else "Pendiente"
                
                pred_text = "No apostó"
                pts_ganados = 0
                if pid in player_preds:
                    pr1, pr2 = player_preds[pid]["eq1"], player_preds[pid]["eq2"]
                    pred_text = f"{pr1} - {pr2}"
                    if p["goles_eq1"] is not None:
                        r1, r2 = p["goles_eq1"], p["goles_eq2"]
                        if r1 == pr1 and r2 == pr2: pts_ganados = 3
                        elif (r1 > r2 and pr1 > pr2) or (r1 < r2 and pr1 < pr2) or (r1 == r2 and pr1 == pr2): pts_ganados = 1
                
                detalle_data.append({
                    "Fase/Partido": f"{p['fase']}: {p_text}",
                    "Su Apuesta": pred_text,
                    "Resultado Real": real_text,
                    "Pts Ganados": pts_ganados if p["goles_eq1"] is not None else "-"
                })
            st.table(pd.DataFrame(detalle_data))
    else:
        st.info("Aún no hay posiciones disponibles (los jugadores deben estar aprobados por el Admin).")

# --- PESTAÑA 2: MIS PREDICCIONES (ACCESO PRIVADO CON CONTRASEÑA) ---
with tab2:
    usuario = st.text_input("Ingresa tu nombre completo (Ej: Carlos Silva):").strip()
    
    if usuario:
        # CASO A: JUGADOR NUEVO (REGISTRO)
        if usuario not in data["jugadores"]:
            st.info(f"✨ El usuario **{usuario}** no está registrado en el sistema. Configura tu acceso aquí:")
            nueva_clave = st.text_input("Crea una contraseña para tu cuenta:", type="password", key="reg_pass")
            
            if st.button("Crear Cuenta y Registrarme"):
                if nueva_clave:
                    data["jugadores"][usuario] = {
                        "aprobado": False, 
                        "clave": nueva_clave,
                        "predicciones": {}
                    }
                    save_data(data)
                    st.success("¡Registro Exitoso! Ahora introduce tu contraseña abajo para ingresar a tu panel.")
                    st.rerun()
                else:
                    st.error("Por favor introduce una contraseña válida.")
        
        # CASO B: JUGADOR EXISTENTE (LOGIN)
        else:
            info_usuario = data["jugadores"][usuario]
            clave_ingresada = st.text_input("Introduce tu contraseña personal:", type="password", key="login_pass")
            
            if clave_ingresada:
                if clave_ingresada != info_usuario.get("clave", ""):
                    st.error("❌ Contraseña incorrecta. Protegemos tu cuenta de accesos no autorizados.")
                else:
                    # VALIDACIÓN DE PAGO
                    if not info_usuario.get("aprobado", False):
                        st.warning(f"🚨 **Hola {usuario}.** Tu cuenta está validada, pero se encuentra **Bloqueada por Pago**. Avisa al administrador apenas realices tu transferencia para activar tu cupo.")
                    else:
                        st.success(f"🔓 **Acceso Concedido.** Bienvenido {usuario}. Gestiona tus pronósticos:")
                        
                        for p in data["partidos"]:
                            pid = str(p["id"])
                            st.write(f"**{p['fase']} ({p['fecha']})**")
                            
                            if "Por definir" in p["eq1"] or "Por definir" in p["eq2"]:
                                st.info(f"🔒 Partido bloqueado. Esperando definición de equipos de fases previas.")
                            elif p["goles_eq1"] is not None:
                                st.error(f"🏁 Partido Finalizado Oficialmente: {p['eq1']} {p['goles_eq1']} - {p['goles_eq2']} {p['eq2']}. Tu apuesta fija fue: {info_usuario['predicciones'].get(pid, {}).get('eq1', '-')}-{info_usuario['predicciones'].get(pid, {}).get('eq2', '-')}")
                            else:
                                col1, col2, col3 = st.columns([2,1,2])
                                val1 = info_usuario["predicciones"].get(pid, {}).get("eq1", 0)
                                val2 = info_usuario["predicciones"].get(pid, {}).get("eq2", 0)
                                
                                with col1: pr1 = st.number_input(f"Goles {p['eq1']}", min_value=0, step=1, value=val1, key=f"p1_{pid}")
                                with col3: pr2 = st.number_input(f"Goles {p['eq2']}", min_value=0, step=1, value=val2, key=f"p2_{pid}")
                                
                                if st.button("Guardar Apuesta", key=f"save_{pid}"):
                                    info_usuario["predicciones"][pid] = {"eq1": pr1, "eq2": pr2}
                                    save_data(data)
                                    st.success("¡Apuesta guardada correctamente!")
                            
                            # --- SISTEMA ANTI-COPIA ---
                            ya_aposto = pid in info_usuario["predicciones"]
                            with st.expander("👁️ Ver qué apostaron los demás muchachos"):
                                if not ya_aposto:
                                    st.warning("🔒 Para evitar copias, debes registrar y guardar tu propia apuesta primero para poder desbloquear los pronósticos de los demás.")
                                else:
                                    otros_datos = []
                                    for otro_j, otro_info in data["jugadores"].items():
                                        if otro_j != usuario and otro_info.get("aprobado", False):
                                            o_pred = otro_info["predicciones"].get(pid, None)
                                            o_txt = f"{o_pred['eq1']} - {o_pred['eq2']}" if o_pred else "No ha apostado"
                                            otros_datos.append({"Jugador": otro_j, "Apuesta": o_txt})
                                    if otros_datos:
                                        st.table(pd.DataFrame(otros_datos))
                                    else:
                                        st.info("Nadie más ha apostado en este partido aún.")
                            st.divider()

# --- PESTAÑA 3: PANEL ADMIN (APROBACIÓN & MARCADORES) ---
with tab3:
    st.subheader("Control Maestro de la Quiniela")
    clave = st.text_input("Contraseña de Administrador:", type="password")
    
    if clave == "temix.1234":
        st.success("Autenticación Exitosa.")
        
        st.write("### 💰 Control de Acceso y Pagos")
        jugadores_lista = list(data["jugadores"].keys())
        if jugadores_lista:
            for j in jugadores_lista:
                status_actual = data["jugadores"][j].get("aprobado", False)
                label = f"Aprobado (Activo)" if status_actual else "PENDIENTE DE PAGO (Bloqueado)"
                nuevo_status = st.checkbox(f"Jugador: {j} -> Estado: {label}", value=status_actual, key=f"pay_{j}")
                if nuevo_status != status_actual:
                    data["jugadores"][j]["aprobado"] = nuevo_status
                    save_data(data)
                    st.rerun()
        else:
            st.info("No hay jugadores registrados en el sistema todavía.")
            
        st.divider()
        
        st.write("### ⚽ Registro de Marcadores Oficiales")
        for p in data["partidos"]:
            if "Por definir" in p["eq1"] or "Por definir" in p["eq2"]: continue
            st.write(f"**{p['fase']}: {p['eq1']} vs {p['eq2']}**")
            col1, col2 = st.columns(2)
            v1 = p["goles_eq1"] if p["goles_eq1"] is not None else 0
            v2 = p["goles_eq2"] if p["goles_eq2"] is not None else 0
            
            with col1: rg1 = st.number_input(f"Goles Final {p['eq1']}", min_value=0, step=1, value=v1, key=f"r1_{p['id']}")
            with col2: rg2 = st.number_input(f"Goles Final {p['eq2']}", min_value=0, step=1, value=v2, key=f"r2_{p['id']}")
            
            ganador_m = p.get("ganador_manual", p["eq1"])
            if rg1 == rg2 and p["fase"] != "16vos":
                ganador_m = st.selectbox(f"¿Quién avanzó por Penales?", [p["eq1"], p["eq2"]], key=f"pen_{p['id']}")
            
            if st.button("Publicar Resultado Oficial", key=f"btn_r_{p['id']}"):
                p["goles_eq1"] = int(rg1)
                p["goles_eq2"] = int(rg2)
                if rg1 == rg2 and p["fase"] != "16vos":
                    p["ganador_manual"] = ganador_m
                    p["perdedor_manual"] = p["eq2"] if ganador_m == p["eq1"] else p["eq1"]
                save_data(data)
                st.success("Marcador e historial de posiciones actualizados.")
                st.rerun()
            st.write("---")

   

                   
                 
