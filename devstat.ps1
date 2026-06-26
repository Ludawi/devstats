<#
.SYNOPSIS
    PowerShell wrapper for the devstats CLI tool.
#>
[CmdletBinding()]
param()

$ScriptDir = $PSScriptRoot
$PythonScript = Join-Path $ScriptDir "main.py"

# Splat all passed arguments
python $PythonScript @args
exit $LASTEXITCODE
