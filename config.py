import subprocess
import threading
from datetime import datetime
import socket
import os
import platform
import sys
import psutil
import getpass
import time

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import defaultdict

VERSION_SOFTWARE = "0.0.3"

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
"                       ..             ",
"                                      "
]


ACTIONS = {
    0: {
        "label": "Desativar Transparência",
        "description": "Remove efeitos de transparência do Windows, reduzindo uso de GPU e memória.",
        "tab": "Otimização",
        "danger": False,
        "handler": "disable_transparency",
    },
    1: {
        "label": "Desativar Game Mode",
        "description": "Desativa Game Mode, Game Bar e gravações em segundo plano para melhor desempenho.",
        "tab": "Otimização",
        "danger": False,
        "handler": "disable_gamemode",
    },
    2: {
        "label": "Plano de Energia (Máx. Desempenho)",
        "description": "Define o plano de energia para máximo desempenho, evitando economia agressiva.",
        "tab": "Otimização",
        "danger": False,
        "handler": "power_plan",
    },
    3: {
        "label": "Efeitos Visuais (Desempenho)",
        "description": "Reduz animações e efeitos visuais para deixar o sistema mais rápido.",
        "tab": "Otimização",
        "danger": False,
        "handler": "visual_effects",
    },
    4: {
        "label": "Desativar Serviços Pesados",
        "description": "Desativa serviços conhecidos por alto uso de disco e memória, como SysMain.",
        "tab": "Otimização",
        "danger": True,
        "handler": "disable_services",
    },
    5: {
        "label": "Limpar Arquivos Temporários",
        "description": "Remove arquivos temporários do usuário e do Windows, liberando espaço em disco.",
        "tab": "Arquivos",
        "danger": False,
        "handler": "clean_temp",
    },
    6: {
        "label": "Limpar Prefetch",
        "description": "Remove arquivos de pré-carregamento antigos usados pelo Windows.",
        "tab": "Arquivos",
        "danger": False,
        "handler": "clean_prefetch",
    },
    7: {
        "label": "Limpar Cache do Windows Update",
        "description": "Remove arquivos de atualizações antigas que podem ocupar vários GB.",
        "tab": "Arquivos",
        "danger": True,
        "handler": "clean_windows_update",
    },
    8: {
        "label": "Desativar Inicialização Rápida",
        "description": "Desativa o Fast Startup para evitar problemas de boot e drivers.",
        "tab": "Sistema",
        "danger": True,
        "handler": "disable_fast_startup",
    },
    9: {
        "label": "Otimização Completa",
        "description": (
            "Executa um conjunto completo de otimizações seguras:\n"
            "- Transparência\n"
            "- Game Mode\n"
            "- Plano de Energia\n"
            "- Efeitos Visuais\n"
            "- Serviços Pesados\n"
            "- Limpeza de Temporários"
        ),
        "tab": "Otimização",
        "danger": True,
        "handler": "optimize_all",
    },
    10: {
        "label": "Reiniciar Explorer",
        "description": "Reinicia a interface gráfica do Windows sem precisar reiniciar o PC.",
        "tab": "Otimização",
        "danger": True,
        "handler": "restart_explorer",
    },
    11: {
        "label": "Limpar DNS",
        "description": "Limpa o cache DNS para corrigir falhas de acesso à internet.",
        "tab": "Rede",
        "danger": False,
        "handler": "flush_dns",
    },
    12: {
        "label": "Resetar Rede (Completo)",
        "description": "Reseta TCP/IP, Winsock e DNS. Pode exigir reinicialização.",
        "tab": "Rede",
        "danger": True,
        "handler": "reset_network",
    },
    13: {
        "label": "Reset Winsock",
        "description": "Reseta apenas o Winsock, útil para erros de conexão.",
        "tab": "Rede",
        "danger": True,
        "handler": "reset_winsock",
    },
    14: {
        "label": "Encerrar Tarefas em Segundo Plano",
        "description": "Finaliza processos comuns que consomem recursos desnecessariamente.",
        "tab": "Sistema",
        "danger": True,
        "handler": "kill_background_tasks",
    },
    15: {
        "label": "Verificar Sistema (SFC)",
        "description": "Verifica e corrige arquivos corrompidos do Windows.",
        "tab": "Manutenção",
        "danger": False,
        "handler": "run_sfc",
    },
    16: {
        "label": "Reparar Windows (DISM)",
        "description": "Repara a imagem do Windows usada pelo sistema de atualização.",
        "tab": "Manutenção",
        "danger": False,
        "handler": "run_dism",
    },
    17: {
        "label": "Verificar Disco (CHKDSK)",
        "description": "Agenda verificação completa do disco no próximo boot.",
        "tab": "Manutenção",
        "danger": True,
        "handler": "run_chkdsk",
    },
    18: {
        "label": "IPConfig",
        "description": "Mostra configurações de rede (ipconfig /all).",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_ipconfig",
    },
    19: {
        "label": "Executar MAS",
        "description": "Executa Microsoft Activation Scripts (janela externa).",
        "tab": "Ativação",
        "danger": True,
        "handler": "run_massgrave",
    },
    20: {
        "label": "Ping Google",
        "description": "Testa conectividade com google.com.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "ping_google",
    },
    21: {
        "label": "Traceroute",
        "description": "Rastreia rota até google.com.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_tracert",
    },
    22: {
        "label": "NSLookup",
        "description": "Consulta DNS do Google.",
        "tab": "Diagnóstico",
        "danger": False,
        "handler": "run_nslookup",
    },
}


AUTOCOMPLETE_COMMANDS = [
    "ipconfig",
    "ping",
    "tracert",
    "nslookup",
    "netstat",
    "arp",
    "route",
    "systeminfo",
    "tasklist",
    "driverquery",
    "sfc /scannow",
    "dism /online /cleanup-image /restorehealth",
    "cls"
]
