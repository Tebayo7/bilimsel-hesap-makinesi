import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🔬 Bilimsel Hesap Makinesi")
        self.geometry("500x600")
        self.configure(bg="lightgray")

        self.expression = ""
        self.history = []

        self._create_widgets()

    def _create_widgets(self):
        # Giriş alanı
        self.entry = ttk.Entry(self, font=("Courier", 20), justify='right')
        self.entry.pack(fill='x', padx=10, pady=10)

        # Sonuç etiketi
        self.result_label = ttk.Label(self, text="Sonuç: ", font=("Courier", 14), background="lightgray")
        self.result_label.pack(padx=10, anchor='w')

        # Tuşlar
        button_frame = tk.Frame(self)
        button_frame.pack()

        buttons = [
            ['7', '8', '9', '/', 'sin'],
            ['4', '5', '6', '*', 'cos'],
            ['1', '2', '3', '-', 'tan'],
            ['0', '.', '(', ')', '+'],
            ['π', 'e', 'log', '√', '^'],
            ['C', '⌫', '=', 'H']
        ]

        for row in buttons:
            row_frame = tk.Frame(button_frame)
            row_frame.pack(expand=True, fill='both')
            for btn in row:
                action = lambda x=btn: self._on_button_click(x)
                b = tk.Button(row_frame, text=btn, width=6, height=2, command=action, font=("Courier", 14))
                b.pack(side='left', expand=True, fill='both', padx=2, pady=2)

        # Geçmiş kutusu
        self.history_box = tk.Text(self, height=8, font=("Courier", 10), bg="white")
        self.history_box.pack(fill='both', padx=10, pady=10)

    def _on_button_click(self, char):
        if char == "C":
            self.entry.delete(0, tk.END)
            self.result_label.config(text="Sonuç: ")
        elif char == "⌫":
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])
        elif char == "=":
            expr = self.entry.get()
            try:
                expr = expr.replace('π', str(math.pi))
                expr = expr.replace('e', str(math.e))
                expr = expr.replace('^', '**')
                expr = expr.replace('√', 'math.sqrt')

                # Destekli fonksiyonları izinli alanlara ekle
                allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                result = eval(expr, {"__builtins__": {}}, allowed)
                self.result_label.config(text=f"Sonuç: {result}")
                self.history.append(f"{expr} = {result}")
                self._update_history()
            except Exception as e:
                self.result_label.config(text=f"Hata: {e}")
        elif char == "H":
            self._update_history()
        elif char in ['sin', 'cos', 'tan', 'log', '√']:
            self.entry.insert(tk.END, f"{char}(")
        else:
            self.entry.insert(tk.END, char)

    def _update_history(self):
        self.history_box.delete(1.0, tk.END)
        for item in self.history[-10:][::-1]:  # Son 10 işlem
            self.history_box.insert(tk.END, item + "\n")

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
