import streamlit as st
import numpy as np
from fpdf import FPDF

# Modelos de painéis Absen para locação
painel_modelos = {
    "KLCOB V2 Series - 0.78mm": {"pitch": 0.78, "res_x": 768, "res_y": 432, "largura": 600, "altura": 337.5},
    "KLCOB V2 Series - 0.93mm": {"pitch": 0.93, "res_x": 640, "res_y": 360, "largura": 600, "altura": 337.5},
    "KLCOB V2 Series - 1.25mm": {"pitch": 1.25, "res_x": 480, "res_y": 270, "largura": 600, "altura": 337.5},
    "KLCOB V2 Series - 1.56mm": {"pitch": 1.56, "res_x": 384, "res_y": 216, "largura": 600, "altura": 337.5},
    "CPS Series - 1.8mm": {"pitch": 1.8, "res_x": 178, "res_y": 267, "largura": 320, "altura": 480},
    "CPS Series - 2.0mm": {"pitch": 2.0, "res_x": 160, "res_y": 240, "largura": 320, "altura": 480},
    "CPS Series - 2.5mm": {"pitch": 2.5, "res_x": 128, "res_y": 192, "largura": 320, "altura": 480},
    "NX Series - 1.2mm": {"pitch": 1.2, "res_x": 800, "res_y": 450, "largura": 960, "altura": 540},
    "NX Series - 1.5mm": {"pitch": 1.5, "res_x": 640, "res_y": 360, "largura": 960, "altura": 540},
    "NX Series - 1.8mm": {"pitch": 1.8, "res_x": 533, "res_y": 300, "largura": 960, "altura": 540},
    "NX Series - 2.5mm": {"pitch": 2.5, "res_x": 384, "res_y": 216, "largura": 960, "altura": 540},
    "NX Series - 3.7mm": {"pitch": 3.7, "res_x": 260, "res_y": 146, "largura": 960, "altura": 540},
}

# Modelos de processadores NovaStar
processadores = {
    "Novastar VX1000": {"max_pixels": 6500000, "portas": 10},
    "Novastar VX600": {"max_pixels": 3900000, "portas": 6},
    "Novastar VX400": {"max_pixels": 2300000, "portas": 4},
    "Novastar H2 com H_20xRJ45": {"max_pixels": 13000000, "portas": 20},
    "Novastar H2 com H_16xRJ45+2xFiber": {"max_pixels": 10400000, "portas": 16},
    "Novastar H5 com H_20xRJ45": {"max_pixels": 13000000, "portas": 20},
    "Novastar H5 com H_16xRJ45+2xFiber": {"max_pixels": 10400000, "portas": 16},
}

# Função para calcular a configuração do painel
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
    
    st.subheader("Resultados")
    st.write(f"Número de módulos na largura: {resultados['num_modulos_x']:.2f}")
    st.write(f"Número de módulos na altura: {resultados['num_modulos_y']:.2f}")
    st.write(f"Total de módulos: {resultados['total_modulos']:.0f}")
    st.write(f"Resolução total: {resultados['total_pixels_x']} x {resultados['total_pixels_y']}")
    st.write(f"Número de portas necessárias: {resultados['num_portas']:.0f}")
