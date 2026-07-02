import streamlit as st
import pandas as pd
import json
import os
import datetime
import pytz
from fpdf import FPDF

st.set_page_config(page_title="🏆 Quiniela Real Unión 2026", layout="centered")

DATA_FILE = "quiniela_data_v3.json"

if "usuario_logueado" not in st.session_state:
    st.session_state["usuario_logueado"] = None

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "partidos": [
                {"id": 1, "fecha": "03/07", "hora": "12:00", "fase": "16vos", "eq1": "🇦🇺 Australia", "eq2": "🇪🇬 Egipto", "goles_eq1": None, "goles_eq2": None},
                {"id": 2, "fecha": "03/07", "hora": "16:00", "fase": "16vos", "eq1": "🇦🇷 Argentina", "eq2": "🇨🇻 Cabo Verde", "goles_eq1": None, "goles_eq2": None},
                {"id": 3, "fecha": "03/07", "hora": "20:00", "fase": "16vos", "eq1": "🇨🇴 Colombia", "eq2": "🇬🇭 Ghana", "goles_eq1": None, "goles_eq2": None},
                {"id": 4, "fecha": "04/07", "hora": "12:00", "fase": "Octavos 1", "eq1": "🇨🇦 Canadá", "eq2": "🇲🇦 Marruecos", "goles_eq1": None, "goles_eq2": None},
                {"id": 5, "fecha": "04/07", "hora": "16:00", "fase": "Octavos 2", "eq1": "🇵🇾 Paraguay", "eq2": "🇫🇷 Francia", "goles_eq1": None, "goles_eq2": None},
                {"id": 6, "fecha": "05/07", "hora": "12:00", "fase": "Octavos 3", "eq1": "🇧🇷 Brasil", "eq2": "🇳🇴 Noruega", "goles_eq1": None, "goles_eq2": None},
                {"id": 7, "fecha": "05/07", "hora": "16:00", "fase": "Octavos 4", "eq1": "🇲🇽 México", "eq2": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "goles_eq1": None, "goles_eq2": None},
                {"id": 8, "fecha": "06/07", "hora": "12:00", "fase": "Octavos 5", "eq1": "Ganador 🇵🇹/🇭🇷", "eq2": "Ganador 🇪🇸/🇦🇹", "goles_eq1": None, "goles_eq2": None},
                {"id": 9, "fecha": "06/07", "hora": "16:00", "fase": "Octavos 6", "eq1": "🇺🇸 Estados Unidos", "eq2": "🇧🇪 Bélgica", "goles_eq1": None, "goles_eq2": None},
                {"id": 10, "fecha": "07/07", "hora": "12:00", "fase": "Octavos 7", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 11, "fecha": "07/07", "hora": "16:00", "fase": "Octavos 8", "eq1": "Ganador 🇨🇭/🇩🇿", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 12, "fecha": "09/07", "hora": "16:00", "fase": "Cuartos 1", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 13, "fecha": "10/07", "hora": "16:00", "fase": "Cuartos 2", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 14, "fecha": "11/07", "hora": "12:00", "fase": "Cuartos 3", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 15, "fecha": "11/07", "hora": "16:00", "fase": "Cuartos 4", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 16, "fecha": "14/07", "hora": "16:00", "fase": "Semifinal 1", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 17, "fecha": "15/07", "hora": "16:00", "fase": "Semifinal 2", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 18, "fecha": "18/07", "hora": "16:00", "fase": "3er Lugar", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None},
                {"id": 19, "fecha": "19/07", "hora": "15:00", "fase": "FINAL", "eq1": "Por definir", "eq2": "Por definir", "goles_eq1": None, "goles_eq2": None}
            ],
            "jugadores": {}
        }
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

def generar_pdf(usuario, apuestas, partidos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "COMPROBANTE OFICIAL - REAL UNIÓN", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(190, 10, f"Jugador: {usuario}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(90, 10, "Partido", border=1)
    pdf.cell(50, 10, "Tu Pronóstico", border=1, align='C')
    pdf.cell(50, 10, "Estado", border=1, align='C')
    pdf.ln()
    pdf.set_font("Arial", '', 9)
    for p in partidos:
        pid = str(p["id"])
        if pid in apuestas:
            ap = apuestas[pid]
            estado = "FINALIZADO" if p["goles_eq1"] is not None else "PENDIENTE"
            pdf.cell(90, 8, f"{p['fase']}: {p['eq1']} vs {p['eq2']}", border=1)
            pdf.cell(50, 8, f"{ap['eq1']} - {ap['eq2']}", border=1, align='C')
            pdf.cell(50, 8, estado, border=1, align='C')
            pdf.ln()
    return pdf.output(dest='S').encode('latin-1')

data = load_data()
tz_chile = pytz.timezone("America/Santiago")
ahora_chile = datetime.datetime.now(tz_chile)

st.title("🏆 Quiniela Real Unión 2026")

tab1, tab2, tab3 = st.tabs(["📊 Ranking", "📝 Mis Apuestas", "⚙️ Admin"])

with tab1:
    ranking = []
    for jugador, info in data["jugadores"].items():
        if not info.get("aprobado", False): continue
        puntos = 0; plenos = 0
        for p in data["partidos"]:
            pid = str(p["id"])
            if p["goles_eq1"] is not None and pid in info["predicciones"]:
                r1, r2 = p["goles_eq1"], p["goles_eq2"]
                pr1, pr2 = info["predicciones"][pid]["eq1"], info["predicciones"][pid]["eq2"]
                if r1 == pr1 and r2 == pr2: puntos += 3; plenos += 1
                elif (r1>r2 and pr1>pr2) or (r1<r2 and pr1<pr2) or (r1==r2 and pr1==pr2): puntos += 1
        ranking.append({"Jugador": jugador, "Puntos": puntos, "Plenos": plenos})
    if ranking:
        df = pd.DataFrame(ranking).sort_values(by=["Puntos", "Plenos"], ascending=False)
        st.dataframe(df, use_container_width=True)

with tab2:
    usuario_sesion = st.session_state["usuario_logueado"]
    if usuario_sesion is None:
        u_raw = st.text_input("Nombre de usuario:").strip().title()
        if u_raw:
            if u_raw not in data["jugadores"]:
                c = st.text_input("Crea una clave:", type="password")
                if st.button("Registrar"):
                    data["jugadores"][u_raw] = {"aprobado": False, "clave": c, "predicciones": {}}
                    save_data(data); st.session_state["usuario_logueado"] = u_raw; st.rerun()
            else:
                c = st.text_input("Clave:", type="password")
                if st.button("Entrar") and c == data["jugadores"][u_raw]["clave"]:
                    st.session_state["usuario_logueado"] = u_raw; st.rerun()
    else:
        st.write(f"👤 **{usuario_sesion}**")
        if st.button("🔴 Cerrar Sesión"): st.session_state["usuario_logueado"] = None; st.rerun()
        if not data["jugadores"][usuario_sesion].get("aprobado"): st.warning("Bloqueado por pago.")
        else:
            for p in data["partidos"]:
                pid = str(p["id"])
                st.write(f"**{p['fase']} ({p['fecha']} {p['hora']})**")
                try:
                    dt = tz_chile.localize(datetime.datetime(2026, int(p['fecha'].split('/')[1]), int(p['fecha'].split('/')[0]), int(p['hora'].split(':')[0]), int(p['hora'].split(':')[1])))
                    cerrado = ahora_chile >= dt
                except: cerrado = False
                
                if p["goles_eq1"] is not None: st.error("Partido finalizado.")
                elif cerrado: st.warning("Apuestas cerradas.")
                else:
                    c1, c2 = st.columns(2)
                    pr1 = c1.number_input(f"{p['eq1']}", value=data["jugadores"][usuario_sesion]["predicciones"].get(pid, {}).get("eq1", 0), key=f"p1_{pid}")
                    pr2 = c2.number_input(f"{p['eq2']}", value=data["jugadores"][usuario_sesion]["predicciones"].get(pid, {}).get("eq2", 0), key=f"p2_{pid}")
                    if st.button("Guardar", key=f"s_{pid}"):
                        data["jugadores"][usuario_sesion]["predicciones"][pid] = {"eq1": pr1, "eq2": pr2}
                        save_data(data); st.rerun()
            st.download_button("📥 Descargar Ticket PDF", generar_pdf(usuario_sesion, data["jugadores"][usuario_sesion]["predicciones"], data["partidos"]), f"{usuario_sesion}.pdf", "application/pdf")

with tab3:
    if st.text_input("Admin Key:", type="password") == "temix.1234":
        for j in data["jugadores"]:
            if st.checkbox(j, data["jugadores"][j].get("aprobado")): data["jugadores"][j]["aprobado"] = True
        save_data(data)
