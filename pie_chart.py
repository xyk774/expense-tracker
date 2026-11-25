import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"
OUTPUT_FILE = "pie_chart_sample.png"

# 中文字型（Windows 用微軟正黑體，Mac 用蘋方），避免中文類別變成方框
plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei", "PingFang TC", "Heiti TC", "Arial Unicode MS"
]
plt.rcParams["axes.unicode_minus"] = False


def load_totals(path):
    """讀取 CSV，依類別加總金額"""
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                totals[row["category"].strip()] += float(row["amount"])
            except (KeyError, ValueError):
                print(f"略過格式錯誤的資料：{row}")
    return totals


def draw_pie(totals):
    labels = list(totals.keys())
    values = list(totals.values())
    total = sum(values)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        values,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({p * total / 100:.0f})",
        startangle=90,
    )
    ax.set_title(f"各類別支出比例（總計 {total:.0f} 元）")
    ax.axis("equal")

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
    for category, amount in totals.items():
        print(f"{category}: {amount:.0f}")
    draw_pie(totals)


if __name__ == "__main__":
    main()