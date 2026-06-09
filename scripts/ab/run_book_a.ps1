param(
  [string]$ConfigPath = ".\\config.yml",
  [string]$LogPrefix = "book_a"
)

$ErrorActionPreference = "Stop"
Set-Location "e:\Programming Stuff\Chess Engines\SlowMate Chess Engine\slowmate-chess-engine\lichess-bot"

# Variant A: baseline/default opening book.
if (Test-Path Env:SLOWMATE_OPENING_BOOK_PATH) {
  Remove-Item Env:SLOWMATE_OPENING_BOOK_PATH
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = ".\\lichess_bot_auto_logs\\ab"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "$LogPrefix`_$timestamp.log"

Write-Output "Starting Variant A (baseline book)."
Write-Output "Log file: $logFile"

C:/Users/Pat/AppData/Local/Python/pythoncore-3.14-64/python.exe .\\lichess-bot.py --config $ConfigPath -l $logFile
