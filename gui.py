import tkinter as tk
from tkinter import messagebox, scrolledtext


class GUI:
    def __init__(self, root, action_handler):
        self.root = root
        self.action_handler = action_handler

        self.root.title("Otimizador Windows 11 - Painel OpenVPN Style")
        self.root.geometry("1300x550")
        self.root.configure(bg="#1e1e1e")

        # Lista TOTAL de botões (duas colunas)
        self.buttons_list = [
            # COLUNA 1
            ("Desativar Transparência", False),
            ("Desativar Game Mode", False),
            ("Plano de Energia Máx", False),
            ("Efeitos Visuais", False),
            ("Desativar Serviços Pesados", False),
            ("Limpar Temporários", False),
            ("Flush DNS", False),
            ("Executar SFC", True),
            ("Executar DISM", True),
            ("Otimização Completa", True),
            ("Reiniciar Explorer", True),

            # COLUNA 2
            ("Reparar Rede", True),
            ("Desfragmentar", True),
            ("Reset Winsock", True),
            ("Limpeza Avançada", False),
            ("Informações do Sistema", False),
            ("Executar MassGrave (Console)", True),
        ]

        # Frame da lateral (botões)
        self.left_frame = tk.LabelFrame(
            root, text="Ações", fg="white", bg="#1e1e1e",
            width=350, padx=10, pady=10
        )
        self.left_frame.pack(side="left", fill="y")

        # Frame esquerdo → duas colunas internas
        self.col1 = tk.Frame(self.left_frame, bg="#1e1e1e")
        self.col1.grid(row=0, column=0, sticky="n")

        self.col2 = tk.Frame(self.left_frame, bg="#1e1e1e")
        self.col2.grid(row=0, column=1, sticky="n", padx=10)

        # Frame para logs
        self.right_frame = tk.LabelFrame(
            root, text="Logs", fg="white", bg="#1e1e1e"
        )
        self.right_frame.pack(side="right", fill="both", expand=True)

        # ScrolledText para logs
        self.log_box = scrolledtext.ScrolledText(
            self.right_frame,
            width=70,
            height=40,
            bg="#0e0e0e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.log_box.pack(fill="both", expand=True)

        # Criar botões
        self.create_buttons()

    def create_buttons(self):
        left_buttons_count = len(self.buttons_list) // 2

        for index, (label, dangerous) in enumerate(self.buttons_list):
            parent = self.col1 if index < left_buttons_count else self.col2

            btn = tk.Button(
                parent,
                text=label,
                width=30,
                height=1,
                command=lambda i=index, d=dangerous: self._handle_button(i, d)
            )
            btn.pack(pady=4)

    def _handle_button(self, index, dangerous):
        if dangerous:
            if not messagebox.askyesno(
                "Aviso Importante",
                "Esta ação pode causar instabilidade momentânea.\nDeseja continuar?"
            ):
                return

        self.action_handler(index)

    def add_log(self, text):
        self.log_box.insert("end", text)
        self.log_box.see("end")
