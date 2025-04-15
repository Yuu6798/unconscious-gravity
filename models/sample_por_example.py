from models.por_equations import existence_equation

# === Sample Inputs ===
Q = 0.6  # 問いの意味圧
S_q = 0.7  # 照合空間の密度
t = 0.9  # 臨界時間

# === Existence Generation ===
E = existence_equation(Q, S_q, t)
print(f"Generated existence E = Q × S_q × t = {E:.4f}")