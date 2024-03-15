@echo off
powercfg /batteryreport /output "battery_report.html"
echo '查看完成后请及时清理'
cmd /c start battery_report.html
pause