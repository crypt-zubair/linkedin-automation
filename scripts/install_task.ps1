$ErrorActionPreference = 'Stop'

$Project = Split-Path -Parent $PSScriptRoot
$RunScript = Join-Path $Project 'scripts\run_daily.ps1'
$TaskName = 'LinkedIn Tech Fact Autopilot'
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -ExecutionPolicy Bypass -File "' + $RunScript + '"')
$Trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 10)
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description 'Generate and publish one verified technology fact to LinkedIn daily.' -Force
Write-Host "Installed: $TaskName"
Write-Host 'Daily time: 9:00 AM'
Write-Host 'StartWhenAvailable: enabled'
