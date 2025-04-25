# simulator/boomerang.py

import numpy as np

def simulate_boomerang(
    v0, angle_deg, mass, omega, Cd, Cl, area, duration=10, dt=0.01
):
    """
    ブーメランの軌道を物理シミュレーションする関数
    """

    # 初期設定
    angle_rad = np.radians(angle_deg)
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)
    x, y = 0.0, 0.0

    rho = 1.225  # 空気密度
    g = 9.81     # 重力加速度

    x_list = [x]
    y_list = [y]

    for _ in np.arange(0, duration, dt):
        v = np.sqrt(vx**2 + vy**2)
        if v == 0: v = 0.0001  # 0除算防止

        v_dir = np.array([vx, vy]) / v
        lift_dir = np.array([-v_dir[1], v_dir[0]])

        drag = -0.5 * rho * v**2 * Cd * area * v_dir
        lift = 0.5 * rho * v**2 * Cl * area * lift_dir
        gravity = np.array([0, -mass * g])

        total_force = drag + lift + gravity
        ax, ay = total_force / mass

        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        if y < 0:
            break

        x_list.append(x)
        y_list.append(y)

    return x_list, y_list