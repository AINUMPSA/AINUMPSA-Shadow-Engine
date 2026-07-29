import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
import os

# =============================================
# AINUMPSA - SHADOW ENGINE v1.0
# Lustrzane odbicie głównego silnika rezonansu.
# Portfel: 0x8e504ebd3f1eaa45df87d398b7cbcb823592b324
# =============================================

def load_shadow_data():
    return [
        {"name": "Te Anau", "coef": 0.34, "angle": 225},
        {"name": "Hicks Bay", "coef": 0.44, "angle": 315},
        {"name": "2009DB1", "coef": 0.64, "angle": 45},
        {"name": "2009HA21", "coef": 0.18, "angle": 135},
        {"name": "2017FX101", "coef": 0.82, "angle": 90}
    ]

# Figura
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.set_facecolor('#000000')
fig.patch.set_facecolor('#000000')
ax.axis('off')

# Tytuły
ax.text(0, 1.25, "AINUMPSA // SHADOW ENGINE", color='#aabbcc', fontsize=14, ha='center', alpha=0.7)
ax.text(0, 1.18, "[CIEN TENSORA T]", color='#446688', fontsize=10, ha='center', alpha=0.5)

# Granica cienia
ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, edgecolor='#223344', linewidth=0.5, alpha=0.2))

# Dane
neo_data = load_shadow_data()
scatter = ax.scatter([], [], c=[], s=[], cmap='cool', edgecolors='#446688', linewidths=0.5)
lines = [ax.plot([], [], color='#335577', linewidth=0.5, alpha=0.2)[0] for _ in range(len(neo_data))]
attractor = ax.scatter([0], [0], s=200, c='#666666', marker='*', edgecolors='#aabbcc', linewidths=1)
time_text = ax.text(-1.4, -1.4, "t = 0.000 // SHADOW", color='#335577', fontsize=8, alpha=0.5)

def update(frame):
    t = frame / 200
    phase = t * 2 * np.pi * 2
    collapse = 0.3 + 0.7 * (1 - np.sin(t * np.pi))
    xs, ys, colors, sizes = [], [], [], []
    for i, p in enumerate(neo_data):
        angle = np.radians(p["angle"] + 45 * t * 2)
        r = p["coef"] * collapse
        x = r * np.cos(angle + phase)
        y = r * np.sin(angle + phase)
        xs.append(x)
        ys.append(y)
        colors.append(p["coef"])
        sizes.append(50 + p["coef"] * 150)
        curve = np.linspace(0, 1, 20)
        cx = x * curve + 0.2 * np.sin(curve * np.pi) * (1 - curve)
        cy = y * curve + 0.2 * np.cos(curve * np.pi) * (1 - curve)
        lines[i].set_data(cx, cy)
        lines[i].set_linewidth(0.2 + p["coef"] * 1.2)
        lines[i].set_alpha(0.1 + p["coef"] * 0.5)
    scatter.set_offsets(np.column_stack([xs, ys]))
    scatter.set_array(np.array(colors))
    scatter.set_sizes(sizes)
    pulse = 0.8 + 0.4 * np.sin(t * np.pi * 3)
    attractor.set_sizes([200 * pulse])
    time_text.set_text(f"t = {t:.3f} // shadow collapse: {collapse:.2f}")
    if collapse < 0.4:
        ax.texts[0].set_text("!!! ECHO // CIEN KOLAPSUJE !!!")
        ax.texts[0].set_color('#888888')
    else:
        ax.texts[0].set_text("AINUMPSA // SHADOW ENGINE")
        ax.texts[0].set_color('#aabbcc')
    return [scatter, attractor, time_text] + lines

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
ani.save('shadow_collapse.mp4', writer='ffmpeg', fps=20, dpi=150)
print("✅ SHADOW ENGINE: wygenerowano shadow_collapse.mp4")
