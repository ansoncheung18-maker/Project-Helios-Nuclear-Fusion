# ============================================================
# 核聚變專案：Q 值能量增益模擬
# 目標：計算聚變能量增益因子 (Q = P_fusion / P_heating)
# ============================================================

import math
import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("核聚變 Q 值能量增益模擬")
print("="*60)

# ============================================================
# 1. 基本參數
# ============================================================

# 等離子體參數
temperature_keV = 10  # 10 keV ≈ 1.16 億 K
density_m3 = 1e20  # 等離子體密度 (m⁻³)

# 幾何參數 (托卡馬克)
major_radius_m = 6
minor_radius_m = 2
volume_m3 = 2 * math.pi**2 * major_radius_m * (minor_radius_m**2)

# DT 聚變反應率係數 <σv> (m³/s)
# 參考 Bosch-Hale 公式，10 keV 時約 1.1e-22
sigma_v = 1.1e-22  # m³/s

# 每次 DT 聚變釋放能量 (J)
e_fusion_j = 17.6e6 * 1.602e-19  # 17.6 MeV → 2.82e-12 J

# ============================================================
# 2. 聚變功率計算
# ============================================================

# 聚變功率密度 (W/m³)
# P_fusion = (1/4) * n^2 * <σv> * E_fusion
fusion_power_density = 0.25 * (density_m3**2) * sigma_v * e_fusion_j

# 總聚變功率 (W)
fusion_power_w = fusion_power_density * volume_m3
fusion_power_mw = fusion_power_w / 1e6

print("\n【聚變功率計算】")
print(f"等離子體溫度: {temperature_keV} keV (~{temperature_keV*1.16e7:.0f} K)")
print(f"等離子體密度: {density_m3:.1e} m⁻³")
print(f"反應率係數 <σv>: {sigma_v:.2e} m³/s")
print(f"等離子體體積: {volume_m3:.0f} m³")
print(f"聚變功率密度: {fusion_power_density:.2e} W/m³")
print(f"總聚變功率: {fusion_power_mw:.2f} MW")

# ============================================================
# 3. 加熱功率 (維持等離子體所需)
# ============================================================

# 能量約束時間 (ITER 經驗公式)
# tau_E ~ 1.2e-21 * n * a^2 * R
tau_e = 1.2e-21 * density_m3 * (minor_radius_m**2) * major_radius_m

# 等離子體總能量 (J)
plasma_energy_j = 3 * density_m3 * volume_m3 * (temperature_keV * 1.602e-16)

# 加熱功率 (W)
heating_power_w = plasma_energy_j / tau_e
heating_power_mw = heating_power_w / 1e6

print("\n【加熱功率計算】")
print(f"能量約束時間: {tau_e:.2f} 秒")
print(f"等離子體總能量: {plasma_energy_j:.2e} J")
print(f"加熱功率: {heating_power_mw:.2f} MW")

# ============================================================
# 4. Q 值計算
# ============================================================

q_value = fusion_power_w / heating_power_w

print("\n【Q 值計算】")
print(f"聚變功率: {fusion_power_mw:.2f} MW")
print(f"加熱功率: {heating_power_mw:.2f} MW")
print(f"Q 值 = {q_value:.3f}")

if q_value >= 1:
    print("✅ Q ≥ 1，科學可行性達成")
else:
    print("❌ Q < 1，需要更高溫度或密度")

# ============================================================
# 5. Q 值 vs 溫度分析
# ============================================================

temperatures_keV = np.linspace(5, 25, 50)
q_values = []

# 反應率係數函數 (近似)
def sigma_v_DT(T_keV):
    if T_keV < 5:
        return 1e-23
    elif T_keV < 10:
        return 5e-23
    elif T_keV < 15:
        return 1e-22
    else:
        return 1.5e-22

for T in temperatures_keV:
    sv = sigma_v_DT(T)
    p_fusion = 0.25 * (density_m3**2) * sv * e_fusion_j * volume_m3
    tau_e = 1.2e-21 * density_m3 * (minor_radius_m**2) * major_radius_m
    plasma_energy = 3 * density_m3 * volume_m3 * (T * 1.602e-16)
    p_heating = plasma_energy / tau_e
    q = p_fusion / p_heating if p_heating > 0 else 0
    q_values.append(q)

plt.figure(figsize=(10, 6))
plt.plot(temperatures_keV, q_values, 'b-', linewidth=2)
plt.axhline(y=1, color='r', linestyle='--', label='Q = 1 (科學可行性門檻)')
plt.axhline(y=10, color='g', linestyle='--', label='Q = 10 (商業可行性門檻)')
plt.xlabel('等離子體溫度 (keV)')
plt.ylabel('Q 值 (能量增益)')
plt.title('核聚變 Q 值 vs 等離子體溫度')
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('q_value_analysis.png', dpi=150)
print("\n✅ 圖表已儲存: q_value_analysis.png")

# ============================================================
# 6. 混合堆 Q 值 (加入裂變倍增)
# ============================================================

fission_multiplier = 10  # 裂變能量倍增因子
hybrid_q = q_value * fission_multiplier

print("\n【混合堆 Q 值】")
print(f"裂變倍增因子: {fission_multiplier}x")
print(f"純聚變 Q 值: {q_value:.3f}")
print(f"混合堆等效 Q 值: {hybrid_q:.1f}")

if hybrid_q >= 10:
    print("✅ 混合堆等效 Q 值 > 10，商業可行性高")
else:
    print("⚠️ 混合堆等效 Q 值偏低，需優化")

# ============================================================
# 7. 總結
# ============================================================
print("\n" + "="*60)
print("總結")
print("="*60)
print(f"""
✅ 聚變功率: {fusion_power_mw:.2f} MW
✅ 加熱功率: {heating_power_mw:.2f} MW
✅ 純聚變 Q 值: {q_value:.3f}
✅ 混合堆 Q 值: {hybrid_q:.1f}
✅ 裂變倍增可將科學門檻從 Q>10 降至 Q>1

結論: 混合堆路徑可大幅降低技術門檻，
      使核聚變在工程上更易實現。
""")
