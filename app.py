# streamlit_app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ======================
# 🚀 ブーメラン物理シミュレーション関数
# ======================

def simulate_boomerang(
    v0, angle_deg, mass, omega, Cd, Cl, area, duration=10, dt=0.01
):
    # 初期値設定
    angle_rad = np.radians(angle_deg)
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)
    x, y = 0.0, 0.0

    rho = 1.225  # 空気密度 (kg/m^3)
    g = 9.81     # 重力加速度 (m/s^2)

    # 履歴を保存するリスト
    x_list = [x]
    y_list = [y]

    for _ in np.arange(0, duration, dt):
        v = np.sqrt(vx**2 + vy**2)
        if v == 0: v = 0.0001  # 0除算防止

        # 単位ベクトル
        v_dir = np.array([vx, vy]) / v
        lift_dir = np.array([-v_dir[1], v_dir[0]])  # 揚力は速度に直交

        # 力を計算
        drag = -0.5 * rho * v**2 * Cd * area * v_dir
        lift = 0.5 * rho * v**2 * Cl * area * lift_dir
        gravity = np.array([0, -mass * g])

        # 合力
        total_force = drag + lift + gravity

        # 加速度 → 速度 → 位置
        ax, ay = total_force / mass
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        # もし地面に落ちたら止める
        if y < 0:
            break

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list

# ======================
# 🧑‍🎨 Streamlit UI部分
# ======================

st.title("🪃 ブーメラン物理シミュレーター")

st.sidebar.header("📊 シミュレーション設定")

# 入力スライダー
v0 = st.sidebar.slider("初速 (m/s)", 5, 30, 15)
angle = st.sidebar.slider("投げる角度 (度)", 0, 90, 45)
mass = st.sidebar.slider("質量 (kg)", 0.1, 2.0, 0.5)
omega = st.sidebar.slider("回転速度 ω(rad/s)", 0.0, 50.0, 10.0)
Cd = st.sidebar.slider("空気抵抗係数 Cd", 0.0, 2.0, 0.8)
Cl = st.sidebar.slider("揚力係数 Cl", 0.0, 2.0, 1.2)
area = st.sidebar.slider("表面積 (m²)", 0.01, 0.5, 0.05)

# 実行
if st.button("▶ シミュレーション開始"):
    x, y = simulate_boomerang(v0, angle, mass, omega, Cd, Cl, area)

    # グラフ描画
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("X位置 (m)")
    ax.set_ylabel("Y位置 (m)")
    ax.set_title("ブーメランの軌道")
    st.pyplot(fig)
