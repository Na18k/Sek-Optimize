# Sek Optimize
```text
           .:===++++++===:.              +   Repositório   + : + ------------------------------- +
        .-=++==-::..::-=+++:-.           Nome              : Sek Optimize
     ..=++=:...        ...::=+=:         Autor             : Kainan Santos
    .-++=..          ..:-===++++=.       Linguagem         : Python
   .=+=...         .-++++++++++++=..     Interface         : Tkinter
  .=+=..         .-+++++++++++++++=.     Plataforma        : Windows 10 / 11
  -+=..         .-+++++++++++++++++-.    Tipo              : Otimizador / Diagnóstico
 .=+-.          :-:.......:==+++++=:.    Execução          : Script (.py) / EXE (PyInstaller)
 .++-...--                  .++=..%%:    Arquitetura       : x64
 .++.:%%%..                 ::...=%%:.   Licença           : MIT
 .:#%%%%%%*-......:=+-          .*%%..   Status            : Em desenvolvimento
  +%%%%%%%%%%%%%%%%%*.          .%%+.    Última versão     : 0.0.3
  .#%%%%%%%%%%%%%%%*.          .%%#.     Repositório       : github.com/kainansantos/sek-optimize
  ..#%%%%%%%%%%%%*:.         .:#%#..
    .*%%%%%##*=:.          ..*%%*..      +   Módulos    + : + ------------------------------- +
      :#%#--..          ..-#%%#:.        ✔ Limpeza de sistema
        :*:%%%#+::::::+#%%%%*..          ✔ Otimização de desempenho
           .-##%%%%%%%%%#-...            ✔ Diagnóstico de hardware
                       ..                ✔ Relatórios estilo AIDA
```

**Sek Optimize** é uma ferramenta gráfica em Python para **otimização, manutenção e diagnóstico do Windows**, focada em desempenho, estabilidade e praticidade para técnicos e usuários avançados.

O projeto centraliza, em uma única interface, comandos e ajustes que normalmente exigiriam conhecimento técnico, execução manual no Prompt de Comando ou edição do Registro do Windows.

---

## Principais Recursos

### Otimização do Sistema
- Desativação de transparências do Windows
- Desativação do Game Mode e Game Bar
- Ajuste automático do plano de energia para **Máximo Desempenho**
- Ajustes de efeitos visuais focados em performance
- Desativação de serviços considerados pesados (ex: SysMain)
- Reinício rápido do Explorer

---

### Limpeza
- Limpeza de arquivos temporários do usuário (`%TEMP%`)
- Limpeza da pasta temporária do Windows (`C:\Windows\Temp`)
- Exibição detalhada:
  - Quantidade de arquivos
  - Espaço ocupado (em GB)
- Limpeza de cache DNS

---

### Rede
- Flush de DNS
- Reset de Winsock
- Netstat (conexões ativas)
- ARP Table
- Tabela de rotas
- Testes de conectividade:
  - Ping
  - Traceroute
  - NSLookup

---

### Manutenção do Sistema
- Verificação de integridade com **SFC**
- Reparação da imagem do Windows com **DISM**
- Visualização de informações completas do sistema
- Listagem de processos em execução
- Listagem de drivers instalados

---

### Diagnóstico
- IPConfig completo (`/all`)
- Informações detalhadas do sistema
- Monitoramento rápido para suporte técnico

---

### 🔑 Ativação (opcional)
- Execução do **Microsoft Activation Scripts (MAS)** em janela externa  
  > ⚠️ Recurso avançado, destinado apenas a ambientes de teste/laboratório.

---

## Interface

- Interface gráfica baseada em **Tkinter**
- Execução assíncrona (não trava a UI)
- Sistema de abas por categoria:
  - Otimização
  - Arquivos
  - Rede
  - Sistema
  - Diagnóstico
  - Ativação
- Terminal integrado para execução de comandos personalizados
- Autocomplete de comandos comuns

---

## Logs e Auditoria

- Geração automática de logs detalhados
- Logs salvos em pasta dedicada (`/logs`)
- Registro de:
  - Data e hora
  - Comando executado
  - Saída padrão e erros
- Ideal para auditoria técnica e suporte

---

## Requisitos

- Windows 10 ou superior
- Python 3.10+ (para execução em script)
- Bibliotecas:
  - `psutil`
  - `tkinter` (já incluso no Python para Windows)

Se estiver utilizado o executavel não será necessário nenhum das bibliotecas.

---

## Permissões

Algumas funcionalidades exigem execução como Administrador, como:

- Limpeza da pasta C:\Windows\Temp
- Desativação de serviços
- DISM / SFC
- Reset de Winsock

Caso o programa não esteja em modo administrador, certas ações podem ser parcialmente executadas.

### Estrutura do Projeto

```sh
SekOptimize/
│
├── app.py          # Lógica principal e handlers
├── gui.py          # Interface gráfica (Tkinter)
├── config.py       # Configurações, ações e metadados
├── logs/           # Logs gerados automaticamente
├── main.py         # Ponto de entrada
└── README.md
```

### 🚧 Aviso Importante

Este software realiza alterações no sistema operacional.
Embora todas as ações tenham sido pensadas para serem seguras, recomenda-se:

- Utilizar em ambientes de teste antes de produção
- Executar apenas funcionalidades compreendidas pelo usuário

### Licença

Este projeto é distribuído sob licença MIT, permitindo uso pessoal e comercial, desde que mantidos os créditos.

### Contribuições

Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests.