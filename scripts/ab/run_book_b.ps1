param(
  [string]$ConfigPath = ".\\config.yml",
  [string]$BookPath = "e:\\Programming Stuff\\Chess Engines\\SlowMate Chess Engine\\slowmate-chess-engine\\data\\openings\\opening_book_generated_v3_5.json",
  [string]$LogPrefix = "book_b"
)

$ErrorActionPreference = "Stop"
Set-Location "e:\Programming Stuff\Chess Engines\SlowMate Chess Engine\slowmate-chess-engine\lichess-bot"

# Variant B: generated opening book.
$env:SLOWMATE_OPENING_BOOK_PATH = $BookPath

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logDir = ".\\lichess_bot_auto_logs\\ab"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "$LogPrefix`_$timestamp.log"

Write-Output "Starting Variant B (generated book)."
Write-Output "Book path: $BookPath"
Write-Output "Log file: $logFile"

C:/Users/Pat/AppData/Local/Python/pythoncore-3.14-64/python.exe .\\lichess-bot.py --config $ConfigPath -l $logFile
