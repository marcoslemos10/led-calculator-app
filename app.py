import streamlit as st
import numpy as np
import pandas as pd
from fpdf import FPDF

# Modelos de painéis Absen (Exemplo, pode ser atualizado com mais modelos)
painel_modelos = {
    "Absen PL2.5": {"pitch": 2.5, "res_x": 192, "res_y": 192, "largura": 480, "altura": 480},
    "Absen PL3.9": {"pitch": 3.9, "res_x": 128, "res_y": 128, "largura": 500, "altura": 500},
}

# Modelos de processadores Novastar (Exemplo, pode ser atualizado)
processadores = {
    "Novastar MCTRL660": {"max_pixels": 650000, "portas": 4},
    "Novastar VX6s": {"max_pixels": 1300000, "portas": 6},
}

# Função para calcular configuração do painel
def calcular_painel(modelo_painel, largura_total, altura_total, processador):
    painel = painel_modelos[modelo_painel]
    proc = processadores[processador]
    
    # Número de módulos
    num_modulos_x = largura_total / painel["largura"]
    num_modulos_y = altura_total / painel["altura"]
    total_modulos = num_modulos_x * num_modulos_y
    
    # Resolução total
    total_pixels_x = num_modulos_x * painel["res_x"]
    total_pixels_y = num_modulos_y * painel["res_y"]
    total_pixels = total_pixels_x * total_pixels_y
    
    # Cálculo de portas
    num_portas = np.ceil(total_pixels / proc["max_pixels"])
    
    return {
        "num_modulos_x": num_modulos_x,
        "num_modulos_y": num_modulos_y,
        "total_modulos": total_modulos,
        "total_pixels_x": total_pixels_x,
        "total_pixels_y": total_pixels_y,
        "total_pixels": total_pixels,
        "num_portas": num_portas,
    }

# Streamlit Web App Interface
st.set_page_config(page_title="Calculadora de Painel LED", layout="wide")
st.title("Calculadora de Painel LED - Absen + Novastar")

# Sidebar para entrada de dados
st.sidebar.header("Configuração do Painel")
modelo_painel = st.sidebar.selectbox("Escolha o modelo de painel:", list(painel_modelos.keys()))
largura_total = st.sidebar.number_input("Largura total do painel (mm):", min_value=1000, value=5000)
altura_total = st.sidebar.number_input("Altura total do painel (mm):", min_value=1000, value=3000)
processador = st.sidebar.selectbox("Escolha o processador:", list(processadores.keys()))

if st.sidebar.button("Calcular"):
    resultados = calcular_painel(modelo_painel, largura_total, altura_total, processador)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resultados")
        st.write(f"Número de módulos na largura: {resultados['num_modulos_x']:.2f}")
        st.write(f"Número de módulos na altura: {resultados['num_modulos_y']:.2f}")
        st.write(f"Total de módulos: {resultados['total_modulos']:.0f}")
        st.write(f"Resolução total: {resultados['total_pixels_x']} x {resultados['total_pixels_y']}")
        st.write(f"Número de portas necessárias: {resultados['num_portas']:.0f}")
    
    with col2:
        st.subheader("Geração de PDF")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Relatório de Configuração do Painel LED", ln=True, align='C')
        pdf.cell(200, 10, f"Modelo do painel: {modelo_painel}", ln=True)
        pdf.cell(200, 10, f"Largura total: {largura_total} mm", ln=True)
        pdf.cell(200, 10, f"Altura total: {altura_total} mm", ln=True)
        pdf.cell(200, 10, f"Processador: {processador}", ln=True)
        pdf.cell(200, 10, f"Número de módulos: {resultados['total_modulos']:.0f}", ln=True)
        pdf.cell(200, 10, f"Resolução total: {resultados['total_pixels_x']} x {resultados['total_pixels_y']}", ln=True)
        pdf.cell(200, 10, f"Número de portas necessárias: {resultados['num_portas']:.0f}", ln=True)
        pdf.output("painel_led_config.pdf")
        st.success("PDF gerado com sucesso!")
