# main.py

import streamlit as st
import matplotlib.pyplot as plt
from simulator.boomerang import simulate_boomerang  # ← モジュール読み込み！

st.title("🪃 ブーメラン物理シミュレーター")

st.sidebar.header("📊 パラメータ設定")

v0 = st.sidebar.slider("初速 (m/s)", 5, 30, 15)
angle = st.sidebar.slider("角度 (°)", 0, 90, 45)
mass = st.sidebar.slider("質量 (kg)", 0.1, 2.0, 0.5)
omega = st.sidebar.slider("回転速度 (rad/s)", 0.0, 50.0, 10.0)
Cd = st.sidebar.slider("空気抵抗 Cd", 0.0, 2.0, 0.8)
Cl = st.sidebar.slider("揚力 Cl", 0.0, 2.0, 1.2)
area = st.sidebar.slider("表面積 (m²)", 0.01, 0.5, 0.05)

if st.button("▶ シミュレーション実行"):
    x, y = simulate_boomerang(v0, angle, mass, omega, Cd, Cl, area)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("X位置 (m)")
    ax.set_ylabel("Y位置 (m)")
    ax.set_title("ブーメラン軌道")
    st.pyplot(fig)
