# CS F301 Assignment 2: verify the exact required runtimes and run all tests.
# Usage: powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1 [-InstallRuntimes]
param([switch]$InstallRuntimes)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Find-Executable([string]$Exe) {
    $cmd = Get-Command $Exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}) | Where-Object { $_ -and (Test-Path $_) }
    foreach ($directory in $roots) {
        $folders = Get-ChildItem -Path $directory -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^(Racket|swipl|SWI-Prolog)' }
        foreach ($folder in $folders) {
            foreach ($candidate in @(
                (Join-Path $folder.FullName $Exe),
                (Join-Path (Join-Path $folder.FullName 'bin') $Exe)
            )) {
                if (Test-Path $candidate) { return $candidate }
            }
        }
    }
    return $null
}

function Install-VersionedApp([string]$Id, [int]$Major) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) { throw "winget is not installed. Install $Id manually from its official website." }
    Write-Host "Finding available $Major.x versions for $Id"
    $output = & winget show --id $Id --exact --versions 2>&1
    if ($LASTEXITCODE -ne 0) { throw "winget cannot enumerate versions of $Id`n$output" }
    $versions = @()
    foreach ($line in $output) {
        $v = ([string]$line).Trim()
        if ($v -match "^$Major\.\d+(\.\d+){0,2}$") {
            $versions += $v
        }
    }
    if ($versions.Count -eq 0) {
        throw "No $Major.x version of $Id is available through winget; install that major version from the official archive."
    }
    $target = $versions | Sort-Object { [version]$_ } -Descending | Select-Object -First 1
    Write-Host "Installing $Id version $target"
    & winget install --id $Id --exact --version $target --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "Installation of $Id version $target failed" }
}

$swipl = Find-Executable 'swipl.exe'
$racket = Find-Executable 'racket.exe'
if ($InstallRuntimes) {
    if (-not $swipl) { Install-VersionedApp 'SWI-Prolog.SWI-Prolog' 9 }
    if (-not $racket) { Install-VersionedApp 'Racket.Racket' 8 }
    $swipl = Find-Executable 'swipl.exe'
    $racket = Find-Executable 'racket.exe'
}
if (-not $swipl) { throw 'SWI-Prolog not found. Run with -InstallRuntimes or install SWI-Prolog 9.x manually.' }
if (-not $racket) { throw 'Racket not found. Run with -InstallRuntimes or install Racket 8.x manually.' }

# Put resolved executable folders in this process PATH so Python tests can discover them.
$env:PATH = "$(Split-Path -Parent $swipl);$(Split-Path -Parent $racket);$env:PATH"
$swiplInfo = (& $swipl --version 2>&1 | Out-String).Trim()
$racketInfo = (& $racket --version 2>&1 | Out-String).Trim()
Write-Host "SWI-Prolog: $swiplInfo"
Write-Host "Racket: $racketInfo"
if ($swiplInfo -notmatch '\b9\.\d+') { throw 'Assignment requires SWI-Prolog 9.x; detected a different version.' }
if ($racketInfo -notmatch '\b(?:v)?8\.\d+') { throw 'Assignment requires Racket 8.x; detected a different version.' }

$python = Get-Command py -ErrorAction SilentlyContinue
$pythonArgs = @('-3')
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    $pythonArgs = @()
}
if (-not $python) { throw 'Python 3 is required for the four provided test files.' }

Set-Location $Root
Write-Host 'Running all problem tests, including runtime and stress tests...'
& $python.Source @pythonArgs -m unittest discover -s tests -v 2>&1 |
    Tee-Object -FilePath (Join-Path $Root 'verification_windows.log')
$code = $LASTEXITCODE
if ($code -ne 0) { throw "Assignment tests FAILED with exit code $code" }
$log = Get-Content (Join-Path $Root 'verification_windows.log') -Raw
if ($log -match '(?m)skipped=\d+' -or $log -match '(?m)\.\.\. skipped') {
    throw 'Test runner reported SKIPPED tests; do not treat this as a full pass.'
}
Write-Host 'PASS: all available tests executed without failures or skips.'
