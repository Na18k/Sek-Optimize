import tkinter as tk
from tkinter import scrolledtext


class GuiApp:
    def __init__(self, title="Sek Optmize"):
        # ===================== JANELA PRINCIPAL =====================
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        # ===================== FRAME ESQUERDO (BOTÕES) =====================
        self.left_frame = tk.LabelFrame(self.root, text="Ações", padx=5, pady=5)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Criar 16 botões Lorem
        lorem_buttons = [f"Lorem {i}" for i in range(1, 17)]

        self.buttons = []
        for name in lorem_buttons:
            btn = tk.Button(
                self.left_frame,
                text=name,
                width=18,
                command=lambda n=name: self.add_log(f"{n} pressionado.\n")
            )
            btn.pack(pady=3)
            self.buttons.append(btn)

        # ===================== FRAME DIREITO (LOGS) =====================
        self.right_frame = tk.LabelFrame(self.root, text="Logs", padx=5, pady=5)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.log_box = scrolledtext.ScrolledText(
            self.right_frame,
            width=80,
            height=25,
            bg="black",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.log_box.pack(fill="both", expand=True)

        self.log_box.config(state="disabled")

    # ===================== FUNÇÃO PARA ESCREVER LOGS =====================
    def add_log(self, text):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, text)
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    # ===================== EXECUTAR INTERFACE =====================
    def run(self):
        self.root.mainloop()


# ===================== EXEMPLO DE USO =====================
if __name__ == "__main__":
    ui = Gui()
    ui.add_log("Interface iniciada...\n")
    ui.run()
