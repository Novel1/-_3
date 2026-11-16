import tkinter as tk
from tkinter import ttk

from engine import InferenceEngine
from knowledge_base import QUESTIONS, build_rules


class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sulpak — Консультант по подбору смартфона (прототип ЭС)")
        self.geometry("560x480")
        self.resizable(False, False)

        self.answers = {}
        self.step = 0
        self.selected = tk.StringVar()

        self.header = ttk.Label(self, text="", font=("Segoe UI", 13, "bold"), wraplength=520)
        self.header.pack(pady=(20, 10), padx=20, anchor="w")

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(pady=10, padx=20, anchor="w", fill="x")

        self.progress = ttk.Label(self, text="", foreground="#666")
        self.progress.pack(padx=20, anchor="w")

        btns = ttk.Frame(self)
        btns.pack(pady=20)
        self.back_btn = ttk.Button(btns, text="< Назад", command=self.go_back)
        self.back_btn.grid(row=0, column=0, padx=5)
        self.next_btn = ttk.Button(btns, text="Далее >", command=self.go_next)
        self.next_btn.grid(row=0, column=1, padx=5)

        self.render_question()

    def clear_options(self):
        for w in self.options_frame.winfo_children():
            w.destroy()

    def render_question(self):
        self.clear_options()
        q = QUESTIONS[self.step]
        self.header.config(text=f"Вопрос {self.step + 1} из {len(QUESTIONS)}:\n{q['text']}")
        self.progress.config(text=f"Собрано фактов: {len(self.answers)} / {len(QUESTIONS)}")
        self.selected.set(self.answers.get(q["fact"], q["options"][0][0]))
        for value, label in q["options"]:
            ttk.Radiobutton(self.options_frame, text=label, value=value,
                             variable=self.selected).pack(anchor="w", pady=3)
        self.back_btn.config(state=("normal" if self.step > 0 else "disabled"))
        self.next_btn.config(text="Готово" if self.step == len(QUESTIONS) - 1 else "Далее >")

    def go_back(self):
        self.answers[QUESTIONS[self.step]["fact"]] = self.selected.get()
        self.step -= 1
        self.render_question()

    def go_next(self):
        self.answers[QUESTIONS[self.step]["fact"]] = self.selected.get()
        if self.step < len(QUESTIONS) - 1:
            self.step += 1
            self.render_question()
        else:
            self.show_result()

    def show_result(self):
        engine = InferenceEngine(build_rules())
        facts = engine.run(self.answers)

        for w in self.winfo_children():
            w.destroy()

        lines = []
        lines.append(f"Рекомендуемая категория: {facts.get('category', '—')}")
        lines.append(f"Рекомендуемая линейка: {facts.get('recommended_line', '— уточните у продавца —')}")
        if "note_5g" in facts:
            lines.append(f"\n⚠ {facts['note_5g']}")
        if "note_storage" in facts:
            lines.append(f"⚠ {facts['note_storage']}")
        lines.append("\n— Ход рассуждений экспертной системы (объяснение) —")
        lines.append(engine.explain())

        ttk.Label(self, text="Результат консультации", font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))
        text = tk.Text(self, wrap="word", height=20, width=68)
        text.insert("1.0", "\n".join(lines))
        text.config(state="disabled")
        text.pack(padx=15, pady=5, fill="both", expand=True)
        ttk.Button(self, text="Начать заново", command=self.restart).pack(pady=10)

    def restart(self):
        for w in self.winfo_children():
            w.destroy()
        self.__init__()


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()
