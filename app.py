import subprocess
import threading
from datetime import datetime


class App:
    def __init__(self, gui):
        self.gui = gui
        self.log_file = "otimizacao_win11.log"

    # ============================================
    # LOG CENTRAL
    # ============================================
    def log(self, msg):
        self.gui.add_log(msg + "\n")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def _decode(self, raw):
        for enc in ["utf-8", "cp1252", "latin1"]:
            try:
                return raw.decode(enc).rstrip()
            except UnicodeDecodeError:
                pass
        return raw.decode("latin1", errors="replace").rstrip()

    def run_command(self, desc, cmd):
        self.log("\n=== " + desc + " ===")

        with subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as proc:
            for raw in proc.stdout:
                self.log(self._decode(raw))

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



    # ============================================
    # MAPEAMENTO DOS BOTÕES
    # ============================================
    def execute_button(self, index):

        actions = {
            0: self.disable_transparency,
            1: self.disable_gamemode,
            2: self.power_plan,
            3: self.visual_effects,
            4: self.disable_services,
            5: self.clean_temp,
            6: self.flush_dns,
            7: self.run_sfc,
            8: self.run_dism,
            9: self.optimize_all,
            10: lambda: self.run_command("Reiniciando Explorer", "taskkill /f /im explorer.exe & start explorer.exe"),
            11: lambda: self.log("Reparar rede ainda não implementado."),
            12: lambda: self.log("Desfragmentar ainda não implementado."),
            13: lambda: self.log("Reset Winsock ainda não implementado."),
            14: lambda: self.log("Limpeza avançada ainda não implementada."),
            15: lambda: self.log("Informações do sistema ainda não implementado."),
            16: self.run_massgrave,
        }

        threading.Thread(target=actions[index]).start()
