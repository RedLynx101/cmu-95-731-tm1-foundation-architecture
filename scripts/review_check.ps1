[CmdletBinding()]
param(
    [switch]$IncludeSam
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (Test-Path -LiteralPath $VenvPython) {
    $Python = $VenvPython
} else {
    $Python = (Get-Command python -ErrorAction Stop).Source
}

function Invoke-ReviewStep {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Action
    )

    Write-Host ""
    Write-Host "== $Name =="
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE."
    }
}

Push-Location $Root
try {
    Invoke-ReviewStep "Static checks" { & $Python -m ruff check . }
    Invoke-ReviewStep "Automated tests" { & $Python -m pytest -q -p no:cacheprovider }
    Invoke-ReviewStep "Live API smoke test" { & $Python scripts\smoke_test.py }
    Invoke-ReviewStep "Architecture diagram rebuild" { & $Python scripts\render_architecture.py }

    if ($IncludeSam) {
        Get-Command sam -ErrorAction Stop | Out-Null
        $PreviousTelemetry = $env:SAM_CLI_TELEMETRY
        $PreviousPath = $env:Path
        $env:SAM_CLI_TELEMETRY = "0"
        $env:Path = (Split-Path -Parent $Python) + [IO.Path]::PathSeparator + $env:Path
        try {
            Invoke-ReviewStep "SAM template validation" {
                sam validate --template-file infra\template.yaml
            }
            Invoke-ReviewStep "SAM build" {
                sam build --template-file infra\template.yaml --build-dir .aws-sam\build
            }
        } finally {
            $env:Path = $PreviousPath
            if ($null -eq $PreviousTelemetry) {
                Remove-Item Env:SAM_CLI_TELEMETRY -ErrorAction SilentlyContinue
            } else {
                $env:SAM_CLI_TELEMETRY = $PreviousTelemetry
            }
        }
    }

    Write-Host ""
    Write-Host "All requested review checks passed."
    Write-Host "Next: explain the implementation and record the human result in docs\code-provenance.md."
} finally {
    Pop-Location
}
