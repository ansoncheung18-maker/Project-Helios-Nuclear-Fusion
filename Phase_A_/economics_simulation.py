# ============================================================
# 核聚變專案：經濟可行性模擬
# 目標：計算投資回報期、成本效益、敏感度分析
# ============================================================

import matplotlib.pyplot as plt
import numpy as np

print("="*60)
print("核聚變電廠經濟可行性模擬")
print("="*60)

# ============================================================
# 1. 基本參數
# ============================================================

# 電廠參數
plant_capacity_mw = 500  # 500 MW
capacity_factor = 0.90    # 可用率 90%（模塊化設計）
annual_generation_mwh = plant_capacity_mw * 24 * 365 * capacity_factor
electricity_price_per_mwh = 50  # 美元 (工業用電)

# 成本參數
total_capital_billion = 5.0  # 總投資 50 億美元
annual_opex_billion = 0.2    # 年營運成本 2 億美元
fuel_cost_billion = 0.05     # 年燃料成本 0.5 億美元（小爐更換）

print("\n【基本參數】")
print(f"電廠容量: {plant_capacity_mw} MW")
print(f"可用率: {capacity_factor*100}%")
print(f"年發電量: {annual_generation_mwh/1e6:.2f} TWh")
print(f"電價: ${electricity_price_per_mwh}/MWh")
print(f"總投資: ${total_capital_billion:.1f} 億")
print(f"年營運成本: ${annual_opex_billion:.1f} 億")
print(f"年燃料成本: ${fuel_cost_billion:.1f} 億")

# ============================================================
# 2. 收入與利潤
# ============================================================

annual_revenue_billion = annual_generation_mwh * electricity_price_per_mwh / 1e8
annual_profit_billion = annual_revenue_billion - annual_opex_billion - fuel_cost_billion

print("\n【收入與利潤】")
print(f"年收入: ${annual_revenue_billion:.2f} 億")
print(f"年利潤: ${annual_profit_billion:.2f} 億")

# ============================================================
# 3. 投資回收期
# ============================================================

payback_years = total_capital_billion / annual_profit_billion
payback_days = payback_years * 365

print("\n【投資回收期】")
print(f"回收期: {payback_years:.2f} 年 ≈ {payback_days:.0f} 天")
if payback_years < 5:
    print("✅ 回收期極短，經濟可行性高")
elif payback_years < 10:
    print("✅ 回收期合理，可接受")
else:
    print("⚠️ 回收期較長，需優化成本")

# ============================================================
# 4. 10 年現金流
# ============================================================

years = 10
cumulative_profit = 0
print("\n【10 年現金流】")
print("| 年份 | 累積利潤 (億美元) | 狀態 |")
print("|:---|:---|:---|")
for year in range(1, years+1):
    cumulative_profit += annual_profit_billion
    if cumulative_profit >= total_capital_billion and year <= 3:
        status = "✅ 回本"
    elif cumulative_profit >= total_capital_billion:
        status = "💰 營利"
    else:
        status = "🔄 回收中"
    print(f"| {year:<2} | {cumulative_profit:<15.2f} | {status} |")

# ============================================================
# 5. 敏感度分析：投資成本變化
# ============================================================

capital_variations = [0.7, 0.85, 1.0, 1.15, 1.3]  # 投資成本倍數
payback_list = []

print("\n【敏感度分析：投資成本】")
print("| 投資倍數 | 總投資 (億美元) | 回收期 (年) |")
print("|:---|:---|:---|")
for factor in capital_variations:
    capital = total_capital_billion * factor
    payback = capital / annual_profit_billion
    payback_list.append(payback)
    print(f"| {factor:.2f}x | {capital:.1f} | {payback:.2f} |")

# ============================================================
# 6. 敏感度分析：電價變化
# ============================================================

price_variations = [0.03, 0.04, 0.05, 0.06, 0.07]  # 電價 ($/kWh)
payback_price = []

print("\n【敏感度分析：電價】")
print("| 電價 ($/kWh) | 年收入 (億美元) | 回收期 (年) |")
print("|:---|:---|:---|")
for price in price_variations:
    revenue = annual_generation_mwh * price * 1000 / 1e8
    profit = revenue - annual_opex_billion - fuel_cost_billion
    payback = total_capital_billion / profit if profit > 0 else 999
    payback_price.append(payback)
    print(f"| ${price:.2f} | {revenue:.2f} | {payback:.2f} |")

# ============================================================
# 7. 繪圖：回收期 vs 投資成本
# ============================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 圖 1：投資成本敏感度
factors = [f*100 for f in capital_variations]
ax1.plot(factors, payback_list, 'ro-', linewidth=2, markersize=8)
ax1.axhline(y=5, color='b', linestyle='--', label='5 年回收基準')
ax1.set_xlabel('投資成本 (%)')
ax1.set_ylabel('回收期 (年)')
ax1.set_title('回收期 vs 投資成本')
ax1.grid(True, alpha=0.3)
ax1.legend()

# 圖 2：電價敏感度
prices = [p*100 for p in price_variations]
ax2.plot(prices, payback_price, 'go-', linewidth=2, markersize=8)
ax2.axhline(y=5, color='b', linestyle='--', label='5 年回收基準')
ax2.set_xlabel('電價 (美分/kWh)')
ax2.set_ylabel('回收期 (年)')
ax2.set_title('回收期 vs 電價')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('economics_sensitivity.png', dpi=150)
print("\n✅ 圖表已儲存: economics_sensitivity.png")

# ============================================================
# 8. 總結
# ============================================================
print("\n" + "="*60)
print("總結")
print("="*60)
print(f"""
✅ 年發電量: {annual_generation_mwh/1e6:.2f} TWh
✅ 年利潤: ${annual_profit_billion:.2f} 億
✅ 投資回收期: {payback_years:.2f} 年
✅ 即使投資增加 30%，回收期仍在 6 年以內
✅ 即使電價降至 $0.03/kWh，回收期仍少於 8 年

結論: 核聚變電廠經濟可行性高，適合商業投資。
""")
