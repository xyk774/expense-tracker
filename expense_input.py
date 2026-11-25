import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
FIELDS = ["date", "amount", "category", "note"]


def ask_date():
    while True:
        text = input("日期 (YYYY-MM-DD，直接按 Enter 用今天): ").strip()
        if not text:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("格式錯誤，請輸入像 2026-11-21 的日期")


def ask_amount():
    while True:
        text = input("金額: ").strip()
        try:
            value = float(text)
            if value <= 0:
                print("金額必須大於 0")
                continue
            return value
        except ValueError:
            print("請輸入數字")


def ask_category():
    while True:
        text = input("類別 (例如 food、transport): ").strip()
        if text:
            return text
        print("類別不能空白")


def save_expense(expense):
    is_new = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(expense)


def main():
    print("=== 記帳輸入 ===")
    while True:
        expense = {
            "date": ask_date(),
            "amount": ask_amount(),
            "category": ask_category(),
            "note": input("備註 (可留空): ").strip(),
        }
        save_expense(expense)
        print("已儲存！\n")
        again = input("繼續新增？(y/n): ").strip().lower()
        if again != "y":
            break
    print(f"資料已存在 {DATA_FILE}")


if __name__ == "__main__":
    main()