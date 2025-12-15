import subprocess
import threading
from datetime import datetime
import socket
import os
import platform


APP_ASCII = [
"           .:===++++++===:.           ",
"        .-=++==-::..::-=+++:-.        ",
"     ..=++=:...        ...::=+=:      ",
"    .-++=..          ..:-===++++=.    ",
"   .=+=...         .-++++++++++++=..  ",
"  .=+=..         .-+++++++++++++++=.  ",
"  -+=..         .-+++++++++++++++++-. ",
" .=+-.          :-:.......:==+++++=:. ",
" .++-...--                  .++=..%%: ",
" .++.:%%%..                 ::...=%%:.",
" .:#%%%%%%*-......:=+-          .*%%..",
"  +%%%%%%%%%%%%%%%%%*.          .%%+. ",
"  .#%%%%%%%%%%%%%%%*.          .%%#.  ",
"  ..#%%%%%%%%%%%%*:.         .:#%#..  ",
"    .*%%%%%##*=:.          ..*%%*..   ",
"      :#%#--..          ..-#%%#:.     ",
"        :*:%%%#+::::::+#%%%%*..       ",
"           .-##%%%%%%%%%#-...         ",
"                       ..             "
]


ACTIONS = {
    0: {
        "label": "Desativar Transparência",
        "description": "Desativa as transparências do Windows (reg edit).",
        "tab": "Otimização",
        "danger": False,
        "handler": "disable_transparency",
    },
    1: {
        "label": "Desativar Game Mode",
        "description": "Desativa Game Mode e Game Bar (reg edit).",
        "tab": "Otimização",
        "danger": False,
        "handler": "disable_gamemode",
    },
    2: {
        "label": "Plano de Energia",
        "description": "Define o plano de energia para máximo desempenho (powercfg).",
        "tab": "Otimização",
        "danger": False,
        "handler": "power_plan",
    },
    3: {
        "label": "Efeitos Visuais",
        "description": "Ajusta efeitos visuais para melhor desempenho.",
        "tab": "Otimização",
        "danger": False,
        "handler": "visual_effects",
    },
    4: {
        "label": "Desativar Serviços Pesados",
        "description": "Desativa serviços como SysMain.",
        "tab": "Otimização",
        "danger": False,
        "handler": "disable_services",
    },
    9: {
        "label": "Otimização Completa",
        "description": "Executa todas as otimizações de uma vez.",
        "tab": "Otimização",
        "danger": True,
        "handler": "optimize_all",
    },
    10: {
        "label": "Reiniciar Explorer",
        "description": "Reinicia o Explorer (a área de trabalho some por alguns segundos).",
        "tab": "Otimização",
        "danger": True,
        "handler": "restart_explorer",
    },
    5: {
        "label": "Limpar Temporários",
        "description": "Remove arquivos temporários (%TEMP%).",
        "tab": "Arquivos",
        "danger": False,
        "handler": "clean_temp",
    },
    6: {
        "label": "Limpar DNS",
        "description": "Limpa o cache DNS.",
        "tab": "Rede",
        "danger": False,
        "handler": "flush_dns",
    },
    13: {
        "label": "Reset Winsock",
        "description": "Reseta Winsock (pode desconectar a rede).",
        "tab": "Rede",
        "danger": True,
        "handler": "reset_winsock",
    },
    17: {
        "label": "IPConfig",
        "description": "Mostra configurações de rede (ipconfig /all).",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_ipconfig",
    },
    16: {
        "label": "Executar MAS",
        "description": "Executa Microsoft Activation Scripts (janela externa).",
        "tab": "Ativação",
        "danger": True,
        "handler": "run_massgrave",
    },
        18: {
        "label": "Ping Google",
        "description": "Testa conectividade com google.com.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "ping_google",
    },
    19: {
        "label": "Traceroute",
        "description": "Rastreia rota até google.com.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_tracert",
    },
    20: {
        "label": "NSLookup",
        "description": "Consulta DNS do Google.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_nslookup",
    },
    21: {
        "label": "Netstat",
        "description": "Mostra conexões de rede ativas.",
        "tab": "Rede",
        "danger": False,
        "handler": "run_netstat",
    },
    22: {
        "label": "ARP Table",
        "description": "Mostra tabela ARP.",
        "tab": "Rede",
        "danger": False,
        "handler": "run_arp",
    },
    23: {
        "label": "Rotas",
        "description": "Mostra tabela de rotas.",
        "tab": "Rede",
        "danger": False,
        "handler": "run_route",
    },
    24: {
        "label": "SystemInfo",
        "description": "Mostra informações completas do sistema.",
        "tab": "Sistema",
        "danger": False,
        "handler": "run_systeminfo",
    },
    25: {
        "label": "Processos",
        "description": "Lista processos em execução.",
        "tab": "Sistema",
        "danger": False,
        "handler": "run_tasklist",
    },
    26: {
        "label": "Drivers",
        "description": "Lista drivers instalados.",
        "tab": "Sistema",
        "danger": False,
        "handler": "run_driverquery",
    },
}

class App:
    def __init__(self, gui):
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
        self.log("=== " + desc + " ===")

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
        hostname = socket.gethostname()
        sistema = platform.system()
        release = platform.release()
        arquitetura = platform.machine()
        python_ver = platform.python_version()
        usuario = os.getlogin()
        inicio = self.start_time.strftime("%d/%m/%Y %H:%M:%S")

        info = [
            f"Usuário        : {usuario}",
            f"Máquina        : {hostname}",
            f"Sistema        : {sistema} {release}",
            f"Arquitetura    : {arquitetura}",
            f"Python         : {python_ver}",
            f"Aplicação      : Sek Optimize",
            f"Iniciado em    : {inicio}",
            f"Log            : {os.path.basename(self.log_file)}",
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
        self.run_command("Limpando temporários",
            r'del /q /f /s "%TEMP%\*.*"'
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
