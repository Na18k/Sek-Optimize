import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import defaultdict
from app import *

class GUI:

    def __init__(self, root, action_handler):
        self.root = root
        self.action_handler = action_handler

        self.root.title("Sek Optmize")
        self.root.geometry("1300x700")
        self.root.configure(bg="#1e1e1e")

        self.selected_index = None

        # índices perigosos (confirmação antes de executar)
        self.danger_indices = {9, 10, 11, 13, 16}

        self._build_layout()
        self._build_tabs()

    # ----------------------------------------------------------
    # LAYOUT PRINCIPAL
    # ----------------------------------------------------------
    def _build_layout(self):

        # PALETA DE CORES
        self.bg_main = "#1e1e1e"
        self.bg_frame = "#2b2b2b"
        self.bg_button = "#3a3a3a"
        self.fg_text = "#e0e0e0"

        self.root.configure(bg=self.bg_main)

        # ============================
        # FRAME ESQUERDO COMPLETO
        # ============================
        self.left_container = tk.Frame(self.root, bg=self.bg_main)
        self.left_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # FRAME SUPERIOR (TABS)
        self.top_left = tk.Frame(self.left_container, bg=self.bg_main)
        self.top_left.pack(fill=tk.X)

        # FRAME INFERIOR (Descrição + Executar)
        self.bottom_left = tk.Frame(self.left_container, bg=self.bg_main)
        self.bottom_left.pack(fill=tk.X, pady=(10, 0))

        # ============================
        # ESTILO DAS TABS
        # ============================
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.bg_frame,
                        foreground=self.fg_text,
                        padding=[10, 5],
                        font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", "#3d3d3d")])

        self.tab_control = ttk.Notebook(self.top_left)
        self.tab_control.pack(fill=tk.X, expand=False)

        # ============================
        # DESCRIÇÃO
        # ============================
        desc_frame = tk.LabelFrame(self.bottom_left,
                                   text="Descrição da Ação",
                                   fg="white",
                                   bg="#2d2d2d")
        desc_frame.pack(fill="x", expand=False)

        desc_inner = tk.Frame(desc_frame, bg="#2d2d2d")
        desc_inner.pack(fill="both", expand=True)

        self.desc_text = tk.Text(
            desc_inner,
            width=45,
            height=6,
            wrap="word",
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            state="disabled"
        )
        self.desc_text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(desc_inner, command=self.desc_text.yview)
        scroll.pack(side="right", fill="y")
        self.desc_text.config(yscrollcommand=scroll.set)

        # BOTÃO EXECUTAR
        self.execute_btn = tk.Button(
            desc_frame,
            text="Executar",
            state=tk.DISABLED,
            bg=self.bg_main,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            command=self._execute_selected
        )
        self.execute_btn.pack(pady=8)

        # ============================
        # LOGS À DIREITA
        # ============================
        right_frame = tk.LabelFrame(self.root,
                                    text="Logs",
                                    fg=self.fg_text,
                                    bg=self.bg_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True,
                         padx=10, pady=10)

        self.log_box = scrolledtext.ScrolledText(
            right_frame,
            bg="black",
            fg="#00ff00",
            insertbackground="white",
            font=("Consolas", 9),       # fonte ajustada p/ menos spacing
            state="disabled",
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # Reduz o espaçamento ENTRE as linhas
        self.log_box.tag_configure("tight",
            spacing1=0,   # antes da linha
            spacing2=-2,  # ENTRE linhas (valor negativo aproxima)
            spacing3=0    # depois da linha
        )

    # ----------------------------------------------------------
    # TABS + BOTÕES
    # ----------------------------------------------------------
    def _build_tabs(self):

        tabs = defaultdict(list)

        for idx, cfg in ACTIONS.items():
            tabs[cfg["tab"]].append(idx)

        self.labels = {i: cfg["label"] for i, cfg in ACTIONS.items()}
        self.danger_indices = {i for i, cfg in ACTIONS.items() if cfg["danger"]}

        for tab_name, indices in tabs.items():
            frame = tk.Frame(self.tab_control, bg=self.bg_main)
            self.tab_control.add(frame, text=tab_name)

            for idx in sorted(indices):
                tk.Button(
                    frame,
                    text=self.labels[idx],
                    width=35,
                    anchor="w",
                    command=lambda i=idx: self._select_button(i)
                ).pack(fill="x", pady=3, padx=5)

    # ----------------------------------------------------------
    # SELEÇÃO DE AÇÃO (NÃO EXECUTA)
    # ----------------------------------------------------------
    def _select_button(self, index):
        self.selected_index = index
        desc = ACTIONS[index]["description"]

        self.desc_text.config(state="normal")
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, desc)
        self.desc_text.config(state="disabled")

        self.execute_btn.config(state=tk.NORMAL)

    # ----------------------------------------------------------
    # EXECUTAR AÇÃO
    # ----------------------------------------------------------
    def _execute_selected(self):

        if self.selected_index is None:
            return

        idx = self.selected_index
        label = self.labels[idx]

        if idx in self.danger_indices:
            if not messagebox.askyesno(
                "Atenção",
                f"A ação '{label}' pode modificar configurações do sistema.\nDeseja continuar?"
            ):
                return

        # CHAMA O APP
        self.action_handler(idx)

        # Bloquear novamente após execução
        self.execute_btn.config(state=tk.DISABLED)

    # ----------------------------------------------------------
    # LOG
    # ----------------------------------------------------------
    def add_log(self, text):
        self.log_box.config(state="normal")
        self.log_box.insert("end", text + "\n", "tight")
        self.log_box.see("end")
        self.log_box.config(state="disabled")


