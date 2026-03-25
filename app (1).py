import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diseño de Capacidad M/M/1", layout="centered")

# -----------------------------
# TÍTULO
# -----------------------------
st.title("📊 Diseño de Capacidad en Sistemas M/M/1")
st.markdown("""
Herramienta para determinar la **tasa mínima de servicio (μ)** requerida
para cumplir un nivel de servicio en sistemas de colas.
""")

# -----------------------------
# ENTRADAS
# -----------------------------
st.sidebar.header("⚙️ Parámetros de entrada")

lambda_rate = st.sidebar.number_input(
    "Tasa de llegada λ (clientes/hora)",
    min_value=0.1,
    value=30.0
)

Wq_max_min = st.sidebar.number_input(
    "Tiempo máximo en cola (minutos)",
    min_value=0.1,
    value=2.0
)

Wq_max = Wq_max_min / 60  # a horas

# -----------------------------
# CÁLCULO PRINCIPAL
# -----------------------------
a = 1
b = -lambda_rate
c = -lambda_rate / Wq_max

discriminant = b**2 - 4*a*c

if discriminant > 0:

    mu_min = (-b + math.sqrt(discriminant)) / (2*a)
    mu_practico = math.ceil(mu_min)

    # Métricas
    rho = lambda_rate / mu_practico
    Lq = (lambda_rate**2) / (mu_practico * (mu_practico - lambda_rate))
    L = lambda_rate / (mu_practico - lambda_rate)
    Wq = Lq / lambda_rate
    W = L / lambda_rate

    # -----------------------------
    # RESULTADOS
    # -----------------------------
    st.subheader("📌 Resultados principales")

    col1, col2 = st.columns(2)

    col1.metric("μ mínimo teórico", f"{mu_min:.2f}")
    col2.metric("μ recomendado", f"{mu_practico}")

    st.subheader("📊 Indicadores del sistema")

    col1, col2 = st.columns(2)

    col1.metric("Utilización (ρ)", f"{rho:.4f}")
    col1.metric("Clientes en cola (Lq)", f"{Lq:.4f}")
    col1.metric("Tiempo en cola (Wq)", f"{Wq*60:.2f} min")

    col2.metric("Clientes en sistema (L)", f"{L:.4f}")
    col2.metric("Tiempo total (W)", f"{W*60:.2f} min")

    # -----------------------------
    # VALIDACIÓN
    # -----------------------------
    st.subheader("✅ Validación")

    if Wq <= Wq_max:
        st.success("El sistema cumple el nivel de servicio.")
    else:
        st.error("El sistema NO cumple el nivel de servicio.")

    # -----------------------------
    # GRÁFICO DE SENSIBILIDAD
    # -----------------------------
    st.subheader("📈 Análisis de sensibilidad: μ vs Wq")

    mu_values = np.linspace(lambda_rate + 1, lambda_rate * 2, 100)
    Wq_values = lambda_rate / (mu_values * (mu_values - lambda_rate))

    fig, ax = plt.subplots()
    ax.plot(mu_values, Wq_values * 60)  # en minutos
    ax.axhline(Wq_max_min, linestyle='--')
    ax.axvline(mu_practico, linestyle='--')

    ax.set_xlabel("μ (clientes/hora)")
    ax.set_ylabel("Wq (minutos)")
    ax.set_title("Sensibilidad del tiempo de espera")

    st.pyplot(fig)

    # -----------------------------
    # INTERPRETACIÓN
    # -----------------------------
    st.subheader("🧠 Interpretación gerencial")

    st.markdown(f"""
    - Para cumplir un tiempo máximo de espera de **{Wq_max_min} minutos**, 
      se requiere una capacidad mínima de **{mu_practico} clientes/hora**.
    
    - La utilización del sistema es **{rho*100:.2f}%**, lo que indica:
        - Sistema eficiente
        - Sin sobrecarga crítica
    
    - El gráfico muestra que:
        - Pequeñas variaciones en μ cerca de λ generan grandes cambios en Wq
        - Se requiere margen de capacidad (holgura operativa)
    
    📌 **Conclusión:**
    
    Diseñar con μ cercano a λ es un error. Para cumplir estándares exigentes,
    se necesita capacidad suficiente para absorber variabilidad y evitar congestión.
    """)

else:
    st.error("Error en los cálculos. Verifique los parámetros.")