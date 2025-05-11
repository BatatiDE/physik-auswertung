import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Physik Auswertung", layout="centered")
st.title("🧪 Physik-Auswertung: Mischversuch")

st.markdown("---")

# Eingaben
st.header("Eingabewerte")
mw_heiss = st.number_input("m_w, heiß [g]", value=150.00)
mw_kalt = st.number_input("m_w, kalt [g]", value=123.33)
t_heiss = st.number_input("T_heiß [°C]", value=100.0)
t_kalt = st.number_input("T_kalt [°C]", value=22.2)
t_mix_water = st.number_input("T_M (Wasser) [°C]", value=50.4)

m4 = st.number_input("m4 (ohne Stahl) [g]", value=953.85)
m7 = st.number_input("m7 (mit Stahl) [g]", value=1059.48)
t_m_steel = st.number_input("T_M (Stahl) [°C]", value=27.9)
t_s_steel = st.number_input("T_S (Stahl) [°C]", value=98.0)

m5 = st.number_input("m5 (ohne Kupfer) [g]", value=955.74)
m6 = st.number_input("m6 (mit Kupfer) [g]", value=1086.40)
t_m_copper = st.number_input("T_M (Kupfer) [°C]", value=26.2)
t_s_copper = st.number_input("T_S (Kupfer) [°C]", value=96.6)

t_w = st.number_input("T_W [°C]", value=22.2)

# Unsicherheiten
delta_T = st.number_input("ΔT (alle) [K]", value=0.1)
delta_m = st.number_input("Δm (alle) [g]", value=0.01)
delta_C_D = st.number_input("ΔC_D [J/K]", value=10.0)

if st.button("🔍 Auswertung starten"):
    c_w = 4.18
    c_d = (c_w * mw_heiss * (t_heiss - t_mix_water) - c_w * mw_kalt * (t_mix_water - t_kalt)) / (t_mix_water - t_kalt)

    m_w = mw_kalt
    m_s_steel = m7 - m4
    c_s_steel = ((c_w * m_w + c_d) * (t_m_steel - t_w)) / (m_s_steel * (t_s_steel - t_m_steel))

    m_s_copper = m6 - m5
    c_s_copper = ((c_w * m_w + c_d) * (t_m_copper - t_w)) / (m_s_copper * (t_s_copper - t_m_copper))

    C_m_steel = c_s_steel * 56.00
    C_m_copper = c_s_copper * 63.55

    # Fehlerrechnung
    num = (c_w * m_w + c_d) * (t_m_steel - t_w)
    den = m_s_steel * (t_s_steel - t_m_steel)
    dcs_steel = np.sqrt(
        ((-(c_w * m_w + c_d)) / den * delta_T) ** 2 +
        ((num / den + num / (m_s_steel * (t_s_steel - t_m_steel)**2)) * delta_T) ** 2 +
        ((-num / (m_s_steel * (t_s_steel - t_m_steel)**2)) * delta_T) ** 2 +
        ((c_w * (t_m_steel - t_w)) / den * delta_m) ** 2 +
        ((-num / (m_s_steel**2 * (t_s_steel - t_m_steel))) * delta_m) ** 2 +
        (((t_m_steel - t_w) / den) * delta_C_D) ** 2
    )

    num_cu = (c_w * m_w + c_d) * (t_m_copper - t_w)
    den_cu = m_s_copper * (t_s_copper - t_m_copper)
    dcs_copper = np.sqrt(
        ((-(c_w * m_w + c_d)) / den_cu * delta_T) ** 2 +
        ((num_cu / den_cu + num_cu / (m_s_copper * (t_s_copper - t_m_copper)**2)) * delta_T) ** 2 +
        ((-num_cu / (m_s_copper * (t_s_copper - t_m_copper)**2)) * delta_T) ** 2 +
        ((c_w * (t_m_copper - t_w)) / den_cu * delta_m) ** 2 +
        ((-num_cu / (m_s_copper**2 * (t_s_copper - t_m_copper))) * delta_m) ** 2 +
        (((t_m_copper - t_w) / den_cu) * delta_C_D) ** 2
    )

    st.markdown("---")
    st.subheader("📊 Ergebnisse")

    st.latex(f"C_D = {c_d:.1f} \, \mathrm{{J/K}}")

    st.markdown("**Edelstahl:**")
    st.latex(f"c_S = ({c_s_steel:.2f} \pm {dcs_steel:.2f}) \, \mathrm{{J/(g \cdot K)}}")
    st.latex(f"C_m = {C_m_steel:.1f} \, \mathrm{{J/(mol \cdot K)}}")

    st.markdown("**Kupfer:**")
    st.latex(f"c_S = ({c_s_copper:.2f} \pm {dcs_copper:.2f}) \, \mathrm{{J/(g \cdot K)}}")
    st.latex(f"C_m = {C_m_copper:.1f} \, \mathrm{{J/(mol \cdot K)}}")

    st.markdown("---")
    st.subheader("📈 Temperaturverläufe")

    zeit = list(range(0, 95, 5))
    temp_wasser = [22.2, 29.3, 45.0, 50.1, 50.6, 50.6, 50.5, 50.5, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4, 50.4]
    temp_stahl =  [22.2, 25.9, 27.6, 28.1, 29.0, 29.3, 28.5, 28.3, 28.0, 28.0, 27.9, 27.9, 27.9, 27.9, 27.9, 27.9, 27.9, 27.9, 27.9]
    temp_kupfer = [22.2, 25.1, 29.1, 30.7, 29.4, 27.8, 26.9, 26.8, 26.4, 26.3, 26.2, 26.2, 26.2, 26.2, 26.2, 26.2, 26.2, 26.2, 26.2]

    fig, ax = plt.subplots()
    ax.plot(zeit, temp_wasser[:len(zeit)], label='Wasser', marker='o')
    ax.plot(zeit, temp_stahl[:len(zeit)], label='Edelstahl', marker='o')
    ax.plot(zeit, temp_kupfer[:len(zeit)], label='Kupfer', marker='o')
    ax.set_xlabel('Zeit [s]')
    ax.set_ylabel('Temperatur [°C]')
    ax.set_title('Temperaturverlauf (Matplotlib)')
    ax.legend()
    st.pyplot(fig)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=zeit, y=temp_wasser[:len(zeit)], mode='lines+markers', name='Wasser'))
    fig2.add_trace(go.Scatter(x=zeit, y=temp_stahl[:len(zeit)], mode='lines+markers', name='Edelstahl'))
    fig2.add_trace(go.Scatter(x=zeit, y=temp_kupfer[:len(zeit)], mode='lines+markers', name='Kupfer'))
    fig2.update_layout(title='Temperaturverlauf (Plotly)',
                      xaxis_title='Zeit [s]',
                      yaxis_title='Temperatur [°C]')
    st.plotly_chart(fig2)
