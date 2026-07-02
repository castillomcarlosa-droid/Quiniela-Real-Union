import streamlit as st
import pandas as pd
import json
import os
import datetime
import pytz
from fpdf import FPDF
import io

st.set_page_config(page_title="🏆 Quiniela Real Unión 2026", layout="centered")
DATA_FILE = "quiniela_data_v3.json"

# [--- SECCIÓN DE CARGA Y LÓGICA MANTENIDA ---]
# (Mantenemos las funciones load_data, save_data y resolver_llaves igual que antes para no romper tu app)
# ... [Pega aquí las funciones load_data, save_data y resolver_llaves del código anterior] ...

# --- FUNCIÓN GENERADORA DE PDF ---
def generar_pdf(usuario, apuestas, partidos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="TICKET DE APUESTAS - REAL UNIÓN", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Jugador: {usuario}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Fecha emisión: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.line(10, 35, 200, 35)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, "Partido", border=1)
    pdf.cell(50, 10, "Tu Apuesta", border=1)
    pdf.cell(40, 10, "Estado", border=1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for p in partidos:
        pid = str(p["id"])
        if pid in apuestas:
            ap = apuestas[pid]
            estado = "FINALIZADO" if p["goles_eq1"] is not None else "PENDIENTE"
            pdf.cell(100, 8, f"{p['fase']}: {p['eq1']} vs {p['eq2']}", border=1)
            pdf.cell(50, 8, f"{ap['eq1']} - {ap['eq2']}", border=1, align='C')
            pdf.cell(40, 8, estado, border=1, align='C')
            pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

# --- PARTE DE LA INTERFAZ DE USUARIO ---
# ... (Mantenemos todo el flujo de pestañas anterior) ...
# REEMPLAZA EL BLOQUE DE "Comprobante de Apuestas" por este nuevo:

if hay_apuestas:
    st.write("### 🧾 Comprobante Oficial (PDF)")
    pdf_data = generar_pdf(usuario_sesion, info_usuario["predicciones"], data["partidos"])
    st.download_button(
        label="📥 Descargar mi Ticket Oficial (PDF)",
        data=pdf_data,
        file_name=f"Ticket_{usuario_sesion.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
