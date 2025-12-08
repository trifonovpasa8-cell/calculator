import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import math

# Файл для збереження історії
HISTORY_FILE = "history.json"


# Завантаження історії з файлу
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# Збереження історії в файл
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


class SmartCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartCalc")
        self.expression = ""
        self.history = load_history()

        # Вивід введення
        self.entry_text = tk.StringVar()
        entry = tk.Entry(root, textvariable=self.entry_text, font=("Arial", 20), bd=5, relief=tk.RIDGE, justify='right')
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        # Кнопки
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '(', ')', 'H'
        ]
        row = 1
        col = 0
        for b in buttons:
            action = lambda x=b: self.click(x)
            tk.Button(root, text=b, width=5, height=2, font=("Arial", 15),
                      command=action).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, key):
        if key == "=":
            self.calculate()
        elif key == "C":
            self.expression = ""
            self.entry_text.set("")
        elif key == "H":
            self.show_history()
        else:
            self.expression += str(key)
            self.entry_text.set(self.expression)

    def calculate(self):
        try:
            # Виконання обчислення (підтримує math)
            result = eval(self.expression, {"__builtins__": None}, {"sqrt": math.sqrt, "sin": math.sin,
                                                                    "cos": math.cos, "tan": math.tan,
                                                                    "log": math.log, "pi": math.pi,
                                                                    "e": math.e})
            self.entry_text.set(str(result))
            # Збереження в історію
            self.history.append({
                "expression": self.expression,
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_history(self.history)
            self.expression = str(result)
        except Exception as e:
            messagebox.showerror("Помилка", f"Невірний вираз!\n{e}")
            self.expression = ""
            self.entry_text.set("")

    def show_history(self):
        if not self.history:
            messagebox.showinfo("Історія", "Історія порожня")
            return
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Історія обчислень")
        hist_text = tk.Text(hist_window, width=40, height=20, font=("Arial", 12))
        hist_text.pack(padx=10, pady=10)
        for item in self.history:
            hist_text.insert(tk.END, f"{item['timestamp']} : {item['expression']} = {item['result']}\n")
        hist_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    calc = SmartCalc(root)
    root.mainloop()
