$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    $python = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $python -or -not (Test-Path -LiteralPath $python)) {
    throw 'Install Python 3.11+ or create the project virtual environment first.'
}

New-Item -ItemType Directory -Force -Path '.local' | Out-Null
if (-not $env:DJANGO_DATABASE_URL -and -not $env:DATABASE_URL) {
    $env:DJANGO_DATABASE_URL = 'sqlite:///.local/django.sqlite3'
}

& $python manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) { throw 'Django migrations failed; the development server was not started.' }

if (-not (Test-NetConnection -ComputerName 127.0.0.1 -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue)) {
    $taskWeb = Start-Process -FilePath $python -ArgumentList @('manage.py', 'runserver', '127.0.0.1:8000', '--noreload') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput '.local/website.log' -RedirectStandardError '.local/website-error.log'
    $taskWeb.Id | Set-Content '.local/website.pid'
}
Write-Output 'Website: http://127.0.0.1:8000'
Write-Output 'Admin: http://127.0.0.1:8000/admin/'
