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


def load_expenses():
    """讀取所有支出，檔案不存在時回傳空清單"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_expense(expense):
    """新增一筆支出到檔案最後面"""
    is_new = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(expense)


def write_all(expenses):
    """用整份清單覆寫檔案（刪除後使用）"""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def add_expenses():
    while True:
        expense = {
            "date": ask_date(),
            "amount": ask_amount(),
            "category": ask_category(),
            "note": input("備註 (可留空): ").strip(),
        }
        save_expense(expense)
        print("已儲存！\n")
        if input("繼續新增？(y/n): ").strip().lower() != "y":
            break


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("目前沒有任何支出紀錄")
        return expenses
    print("\n編號  日期          金額      類別 / 備註")
    print("-" * 45)
    total = 0
    for i, e in enumerate(expenses, 1):
        amount = float(e["amount"])
        total += amount
        note = f" / {e['note']}" if e["note"] else ""
        print(f"{i:>3}.  {e['date']}  {amount:>8.0f}  {e['category']}{note}")
    print("-" * 45)
    print(f"共 {len(expenses)} 筆，總計 {total:.0f} 元")
    return expenses


def delete_expense():
    expenses = list_expenses()
    if not expenses:
        return
    text = input("\n輸入要刪除的編號（直接按 Enter 取消）: ").strip()
    if not text:
        print("已取消")
        return
    if not text.isdigit() or not 1 <= int(text) <= len(expenses):
        print("編號不存在")
        return
    target = expenses[int(text) - 1]
    confirm = input(
        f"確定刪除 {target['date']} {target['category']} "
        f"{float(target['amount']):.0f} 元？(y/n): "
    ).strip().lower()
    if confirm != "y":
        print("已取消")
        return
    expenses.pop(int(text) - 1)
    write_all(expenses)
    print("已刪除！")


def main():
    while True:
        print("\n=== 記帳工具 ===")
        print("1. 新增支出")
        print("2. 列出所有支出")
        print("3. 刪除支出")
        print("4. 離開")
        choice = input("請選擇 (1-4): ").strip()
        if choice == "1":
            add_expenses()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            print(f"資料已存在 {DATA_FILE}，再見！")
            break
        else:
            print("請輸入 1 到 4")


if __name__ == "__main__":
    main()