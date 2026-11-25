import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"
OUTPUT_FILE = "pie_chart_sample.png"

plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei", "PingFang TC", "Heiti TC", "Arial Unicode MS"
]
plt.rcParams["axes.unicode_minus"] = False

# 同義類別合併：大小寫不同或中英文同義，都視為同一類
ALIASES = {
    "食物": "food", "餐飲": "food", "吃": "food",
    "交通": "transport",
    "購物": "shopping",
    "飲料": "drink",
    "娛樂": "entertainment",
}
MIN_LABEL_PERCENT = 5  # 小於這個百分比的區塊不在圖上標字，避免重疊


def normalize(category):
    name = category.strip().lower()
    return ALIASES.get(name, name)


def load_totals(path):
    """讀取 CSV，合併同義類別後依類別加總金額"""
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                totals[normalize(row["category"])] += float(row["amount"])
            except (KeyError, ValueError):
                print(f"略過格式錯誤的資料：{row}")
    return totals


def draw_pie(totals):
    # 由大到小排序
    items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    labels = [name for name, _ in items]
    values = [amount for _, amount in items]
    total = sum(values)

    palette = plt.cm.Set2.colors
    colors = [palette[i % len(palette)] for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(11, 6))
    wedges, _, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        counterclock=False,
        autopct=lambda p: f"{p:.1f}%" if p >= MIN_LABEL_PERCENT else "",
        pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(color="#333333", fontsize=11),
    )

    # 中間顯示總支出
    ax.text(0, 0, f"總支出\n{total:,.0f} 元",
            ha="center", va="center", fontsize=15, fontweight="bold")

    # 右側圖例：類別、金額、百分比
    legend_labels = [
        f"{name}  {amount:,.0f} 元（{amount / total:.1%}）"
        for name, amount in items
    ]
    ax.legend(wedges, legend_labels, title="類別",
              loc="center left", bbox_to_anchor=(1, 0.5),
              frameon=False, fontsize=11, title_fontsize=12)

    ax.set_title("各類別支出比例", fontsize=16, fontweight="bold", pad=15)
    ax.axis("equal")

    fig.subplots_adjust(left=0.02, right=0.62)
    plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")
    plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")
    print(f"圖表已存成 {OUTPUT_FILE}")
    plt.show()


def main():
    if not os.path.exists(DATA_FILE):
        print(f"找不到 {DATA_FILE}，請先執行 python expense_input.py 新增支出")
        return
    totals = load_totals(DATA_FILE)
    if not totals:
        print("沒有可用的資料")
        return
    for category, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{category}: {amount:.0f}")
    draw_pie(totals)


if __name__ == "__main__":
    main()