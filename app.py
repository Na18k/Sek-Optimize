from config import *

class App:
    def __init__(self):
        self.gui = None
        self.start_time = datetime.now()
        self.log_file = self.gerar_log_file()

        self.show_fetch()

    def set_gui(self, gui):
        self.gui = gui

    # ============================================
    # LOG CENTRAL
    # ============================================
    def gerar_log_file(self):
        hostname = socket.gethostname()
        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome = f"{hostname}-{data_hora}.log"

        pasta_logs = "logs"
        os.makedirs(pasta_logs, exist_ok=True)

        return os.path.join(pasta_logs, nome)

    def log(self, msg):
        timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M:%S] ")
        texto = timestamp + msg

        # Interface
        self.gui.add_log(texto)

        # Arquivo
        with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
            f.write(texto + "\n")


    def _decode(self, raw):
        try:
            return raw.decode("cp850", errors="replace")
        except Exception:
            return raw.decode("latin-1", errors="replace")


    def run_command(self, desc, cmd):
        self.log("" + desc)

        with subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as proc:
            for raw in proc.stdout:
                line = self._decode(raw).replace("\r\n", "\n")
                self.log(line.rstrip("\n"))


    # ============================================
    # FAST FETCH
    # ============================================
    def on_gui_ready(self, gui):
        self.gui = gui
        self.show_fetch()

    def log_fetch(self, msg):
        if self.gui is None:
            return  # não mostra fetch fora da GUI

        self.gui.add_log(msg)

        with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
            f.write(msg + "\n")


    def show_fetch(self):
        inicio = self.start_time.strftime("%d/%m/%Y %H:%M:%S")

        usuario = getpass.getuser()
        hostname = socket.gethostname()

        sistema = platform.system()
        release = platform.release()
        version = platform.version()
        arquitetura = platform.machine()
        processador = platform.processor()
        python_ver = platform.python_version()

        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)

        ram_total = round(psutil.virtual_memory().total / (1024**3), 1)

        boot_mode = "UEFI" if os.path.exists("C:\\Windows\\System32\\SecureBoot.exe") else "Legacy"

        uptime_seconds = time.time() - psutil.boot_time()
        uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

        exec_mode = "EXE (PyInstaller)" if getattr(sys, "frozen", False) else "Script (.py)"

        info = [
            f"+   Máquina   + : + ------------------------------- +",
            f"Usuário         : {usuario}",
            f"Máquina         : {hostname}",
            f"Sistema         : {sistema} {release}",
            f"Versão SO       : {version}",
            f"Arquitetura     : {arquitetura}",
            f"Processador     : {processador}",
            f"CPU (núcleos)   : {cpu_cores} físicos / {cpu_threads} lógicos",
            f"Memória RAM     : {ram_total} GB",
            f"Boot Mode       : {boot_mode}",
            f"Uptime          : {uptime}",
            f"Iniciado em     : {inicio}",
            f"Log salvo como  : {os.path.basename(self.log_file)}",
            f"|",
            f"+   Software  + : + ------------------------------- +",
            f"Aplicação       : Sek Optimize",
            f"Versão          : {VERSION_SOFTWARE}",
            f"Python          : {python_ver}",
            f"Executável      : {exec_mode}",
            f"Diretório base  : {os.getcwd()}",
        ]

        self.log_fetch("")  # linha em branco inicial

        max_lines = max(len(APP_ASCII), len(info))

        for i in range(max_lines):
            left = APP_ASCII[i] if i < len(APP_ASCII) else ""
            right = info[i] if i < len(info) else ""

            self.log_fetch(f"{left:<30}   {right}")

        self.log_fetch("")

    # ============================================
    # FUNÇÕES INDIVIDUAIS
    # ============================================

    def disable_transparency(self):
        self.run_command("Desativando transparências",
            r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v EnableTransparency /t REG_DWORD /d 0 /f'
        )

    def disable_gamemode(self):
        self.run_command("Desativando Game Mode e Game Bar",
            r'reg add "HKCU\Software\Microsoft\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 0 /f'
        )

    def power_plan(self):
        self.run_command("Ajustando plano de energia", "powercfg -setactive SCHEME_MIN")

    def visual_effects(self):
        self.run_command("Ajustando efeitos visuais",
            r'reg add "HKCU\Control Panel\Desktop" /v DragFullWindows /t REG_SZ /d 0 /f'
        )

    def disable_services(self):
        self.run_command("Desativando serviços pesados",
            r'sc config SysMain start=disabled'
        )

    def clean_temp(self):
        user_temp = os.environ.get("TEMP")
        windows_temp = r"C:\Windows\Temp"

        size_gb, file_count = self.get_folder_info(user_temp)

        table = (
            "\n\n==============================================\n"
            "        LIMPEZA DE ARQUIVOS TEMP          \n"
            "==================================================\n"
            f"Pasta analisada : {user_temp}\n"
            "--------------------------------------------------\n"
            f"Total de arquivos : {file_count}\n"
            f"Tamanho ocupado  : {size_gb} GB\n"
            "==================================================\n\n"
        )

        # TEMP do usuário
        self.run_command(
            table,
            rf'del /q /f /s "{user_temp}\*.*"'
        )

        # TEMP do Windows
        self.run_command(
            "\n\n==================================================\n"
            "     LIMPEZA TEMP DO WINDOWS              \n"
            "==================================================\n"
            f"Pasta : {windows_temp}\n"
            "==================================================\n\n",
            rf'del /q /f /s "{windows_temp}\*.*"'
        )

    def flush_dns(self):
        self.run_command("Limpando DNS", "ipconfig /flushdns")

    def run_sfc(self):
        self.run_command("Executando SFC", "sfc /scannow")

    def run_dism(self):
        self.run_command("Executando DISM", "dism /online /cleanup-image /restorehealth")

    def optimize_all(self):
        self.log("Iniciando otimização completa...")
        self.disable_transparency()
        self.disable_gamemode()
        self.power_plan()
        self.visual_effects()
        self.disable_services()
        self.clean_temp()
        self.flush_dns()
        self.run_sfc()
        self.run_dism()
        self.log("Otimização completa finalizada!")

    def run_massgrave(self):
        self.log("Abrindo Microsoft Activation Scripts (MAS)...")

        cmd = (
            r'start "" cmd.exe /c powershell -NoLogo -NoProfile -Command '
            r'"iwr -useb https://get.activated.win | iex"'
        )

        subprocess.Popen(cmd, shell=True)

    def run_ipconfig(self):
        self.run_command("Executando IPConfig", "ipconfig /all")

    def restart_explorer(self):
        self.run_command(
            "Reiniciando Explorer",
            "taskkill /f /im explorer.exe & start explorer.exe"
        )

    def reset_winsock(self):
        self.run_command(
            "Resetando Winsock",
            "netsh winsock reset"
        )

    def ping_google(self):
        self.run_command("Ping Google", "ping google.com")

    def run_tracert(self):
        self.run_command("Traceroute Google", "tracert google.com")

    def run_nslookup(self):
        self.run_command("NSLookup Google", "nslookup google.com")

    def run_netstat(self):
        self.run_command("Netstat", "netstat -ano")

    def run_arp(self):
        self.run_command("Tabela ARP", "arp -a")

    def run_route(self):
        self.run_command("Tabela de Rotas", "route print")

    def run_systeminfo(self):
        self.run_command("SystemInfo", "systeminfo")

    def run_tasklist(self):
        self.run_command("Lista de Processos", "tasklist")

    def run_driverquery(self):
        self.run_command("Lista de Drivers", "driverquery")

    # ============================================
    # MAPEAMENTO DOS BOTÕES
    # ============================================
    def execute_button(self, index):
        action = ACTIONS.get(index)
        if not action:
            return

        handler_name = action["handler"]
        handler = getattr(self, handler_name, None)

        if not handler:
            self.log(f"Ação '{handler_name}' não implementada.")
            return

        threading.Thread(target=handler).start()


    # ============================================
    # EXECUTAR COMANDO DIGITADO (TERMINAL)
    # ============================================
    def _run_command(self, command):
        self.log(f"> {command}")

        try:
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            for raw in proc.stdout:
                line = self._decode(raw).rstrip("\r\n")
                if line:
                    self.log(line)

            proc.wait()

        except Exception as e:
            self.log(f"ERRO: {e}")



    # ============================================
    # COMANDO DIGITADO PELO TERMINAL DA GUI
    # ============================================
    def run_custom_command(self, command):
        self._run_command(command)

    # ============================================
    # Obtem informações de uma pasta especifica.
    # ============================================
    def get_folder_info(self, folder_path):
        total_size = 0
        total_files = 0

        for root, dirs, files in os.walk(folder_path):
            total_files += len(files)
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
                except (OSError, PermissionError):
                    pass

        size_gb = total_size / (1024 ** 3)
        return round(size_gb, 2), total_files