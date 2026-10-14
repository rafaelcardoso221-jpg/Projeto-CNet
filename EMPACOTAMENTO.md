# Compilar e distribuir (Windows)

## Estado desta entrega

O repositório contém o código completo, configurações comentadas, BATs, testes e um script que gera o EXE/ZIP. **Não contém um EXE Windows compilado ou testado.** O desenvolvimento/testes sem desktop foram feitos em Linux; PyInstaller não faz compilação cruzada Linux → Windows. O ZIP de fontes, se fornecido, não equivale ao ZIP executável abaixo.

Use preferencialmente Windows 10/11 x64 e Python 3.11/3.12 x64 para compilar. O código suporta Python 3.10+; versões futuras do Python podem exigir versões compatíveis das dependências/PyInstaller. Não compile pelo WSL.

## Comando PyInstaller

Em um checkout limpo, antes de personalizar config/calibração, instale Python com launcher `py`, Tcl/Tk e acesso ao PyPI. No Prompt de Comando:

```bat
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-build.txt
.venv\Scripts\python -m unittest discover -s tests -v
.venv\Scripts\python -m PyInstaller --noconfirm --clean --onefile --console --name BaseBot --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32 basebot.py
```

Resultado: `dist\BaseBot.exe`. Mantenha **`--console`**: contagem regressiva e diagnóstico precisam do console. `--onefile` reúne Python/bibliotecas em um executável, mas o processo descompacta componentes em uma pasta temporária ao iniciar. Antivírus podem retardar ou bloquear executáveis não assinados; investigue pelo log do antivírus, não desative a proteção genericamente. Assinatura de código, se desejada, depende de certificado próprio e não está incluída.

Tkinter é biblioteca padrão do Python para Windows; PyInstaller detecta Tk e Pillow/ImageTk. Os imports explícitos dos backends Windows do pynput ajudam no empacotamento de seus listeners. Tesseract é um **programa externo**, não uma dependência Python, e continua exigindo instalação separada com `eng.traineddata`.

## Gerar o ZIP automaticamente

No PowerShell, na pasta do projeto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\empacotar.ps1
```

`Bypass` vale apenas para esse processo; não modifica permanentemente a política da máquina. Em ambiente administrado, siga a política de TI, sem tentar contorná-la. Você pode executar os comandos manualmente se scripts locais não forem permitidos.

O script cria o ambiente, instala as versões fixadas, executa testes, compila, prepara a pasta de distribuição, remove webhook/caminhos locais do exemplo, desabilita a calibração e testa o **próprio EXE** com `--validar-config` e `--dry-run`. Ele para em qualquer código de erro. Não use uma configuração já personalizada como fixture dos testes: compile primeiro, configure a cópia final depois.

Saída:

```text
dist/
  BaseBot.exe
  BaseBot-Windows.zip
  BaseBot-Windows/
    BaseBot.exe
    basebot.py
    INICIAR.bat
    CALIBRAR.bat
    config.ini
    calibracao.ini
    README.md
    EMPACOTAMENTO.md
    CHECKLIST_TESTES.md
    requirements.txt
    requirements-build.txt
    empacotar.ps1
    tests/test_basebot.py
```

A pasta final não contém dependências de desenvolvimento, logs, tokens ou calibração habilitada. Os valores de exemplo e comentários dos INIs vêm do checkout; use um checkout limpo para não distribuir preferências pessoais. Não envie `.venv`, `build` ou um `config.ini` com webhook. Revise o ZIP antes de distribuir.

Extraia esse ZIP em uma segunda pasta e faça os testes reais do checklist, inclusive em uma máquina sem Python. A aprovação de duas etapas separadas é necessária:

- **Empacotamento:** EXE inicia sem Python instalado; encontra INIs ao lado mesmo com outro diretório de trabalho; dry-run e validação funcionam.
- **Integração:** Tesseract instalado, calibração válida, foco/joystick/deriva/emergência medidos no Windows/emulador de destino.

Se não houver Windows disponível, entregue apenas os fontes identificados como tal; não renomeie um executável Linux para `.exe`.
