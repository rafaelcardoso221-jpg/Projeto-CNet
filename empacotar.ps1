# Execute no PowerShell do Windows, na pasta do projeto.
# Nao instala Tesseract nem inclui webhooks/logs/calibracao ativa no ZIP.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if ($env:OS -ne 'Windows_NT') { throw 'Compile o EXE no Windows, nao no Linux/WSL.' }

function Assert-Native([string]$Step) {
    if ($LASTEXITCODE -ne 0) { throw "Falha: $Step (codigo $LASTEXITCODE)." }
}

& py -3 -c 'import sys; assert sys.version_info >= (3,10), sys.version'
Assert-Native 'Verificar Python 3.10+'
& py -3 -m venv .venv
Assert-Native 'Criar ambiente'
$Python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $Python -m pip install -r requirements-build.txt
Assert-Native 'Instalar dependencias'
& $Python -m unittest discover -s tests -v
Assert-Native 'Testes unitarios'
& $Python -m PyInstaller --noconfirm --clean --onefile --console --name BaseBot --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32 basebot.py
Assert-Native 'PyInstaller'

$Stage = Join-Path $PSScriptRoot 'dist\BaseBot-Windows'
if (Test-Path $Stage) { Remove-Item -Recurse -Force $Stage }
New-Item -ItemType Directory -Path $Stage | Out-Null
Copy-Item 'dist\BaseBot.exe' $Stage
foreach ($File in @('INICIAR.bat', 'CALIBRAR.bat', 'README.md', 'CHECKLIST_TESTES.md', 'EMPACOTAMENTO.md', 'basebot.py', 'requirements.txt', 'requirements-build.txt', 'empacotar.ps1')) {
    Copy-Item $File $Stage
}
New-Item -ItemType Directory -Path (Join-Path $Stage 'tests') | Out-Null
Copy-Item 'tests\test_basebot.py' (Join-Path $Stage 'tests')
# Preserve comentarios, mas nunca distribua tokens/caminhos locais ou uma calibracao ativa.
$Config = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'config.ini'))
$Config = [regex]::Replace($Config, '(?m)^(webhook_discord|caminho_emulador|caminho_tesseract)\s*=.*$', '$1 =')
$Calibration = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'calibracao.ini'))
$Calibration = [regex]::Replace($Calibration, '(?m)^calibrado\s*=.*$', 'calibrado = nao')
$Utf8 = New-Object System.Text.UTF8Encoding($false)
[IO.File]::WriteAllText((Join-Path $Stage 'config.ini'), $Config, $Utf8)
[IO.File]::WriteAllText((Join-Path $Stage 'calibracao.ini'), $Calibration, $Utf8)

# Smoke tests do proprio binario, sem mouse, emulador ou OCR instalado.
& (Join-Path $Stage 'BaseBot.exe') --validar-config
Assert-Native 'Validar configuracao no EXE'
& (Join-Path $Stage 'BaseBot.exe') --dry-run
Assert-Native 'Simulacao no EXE'
$Logs = Join-Path $Stage 'logs'
if (Test-Path $Logs) { Remove-Item -Recurse -Force $Logs }
$Zip = Join-Path $PSScriptRoot 'dist\BaseBot-Windows.zip'
Compress-Archive -Path (Join-Path $Stage '*') -DestinationPath $Zip -Force
Write-Host "Pronto: $Zip"
Write-Host 'Ainda e necessario testar OCR, joystick e F12 no Windows/emulador real.'
