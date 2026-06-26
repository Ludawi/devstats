<#
.SYNOPSIS
    PowerShell wrapper for the devstats CLI tool.
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    $RemainingArgs
)

$ScriptDir = $PSScriptRoot
$PythonScript = Join-Path $ScriptDir "main.py"

# Splat all passed arguments
python $PythonScript @RemainingArgs
exit $LASTEXITCODE
