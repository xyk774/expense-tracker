import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

DATA_FILE = "expenses.csv"
OUTPUT_FILE = "trend_chart_sample.png"

plt.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei", "PingFang TC", "Heiti TC", "Arial Unicode MS"
]
plt.rcParams["axes.unicode_minus"] = False


def load_monthly_totals(path):
    """依月份（YYYY-MM）加總金額，並依時間排序"""
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                month = row["date"][:7]
                totals[month] += float(row["amount"])
            except (KeyError, ValueError):
                print(f"略過格式錯誤的資料：{row}")
    return dict(sorted(totals.items()))


def draw_trend(totals):
    months = list(totals.keys())
    values = list(totals.values())
    average = sum(values) / len(values)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(months, values, color="#4C72B0")

    # 每根長條上方標示金額
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.0f}",
            ha="center",
            va="bottom",
        )

    ax.axhline(average, color="#DD8452", linestyle="--",
               label=f"每月平均 {average:.0f} 元")
    ax.set_title("每月支出趨勢")
    ax.set_xlabel("月份")
    ax.set_ylabel("金額（元）")
    ax.legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    print(f"圖表已存成 {OUTPUT_FILE}")
    plt.show()


def main():
    if not os.path.exists(DATA_FILE):
        print(f"找不到 {DATA_FILE}，請先執行 python expense_input.py 新增支出")
        return
    totals = load_monthly_totals(DATA_FILE)
    if not totals:
        print("沒有可用的資料")
        return
    for month, amount in totals.items():
        print(f"{month}: {amount:.0f} 元")
    draw_trend(totals)


if __name__ == "__main__":
    main()