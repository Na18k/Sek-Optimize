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
