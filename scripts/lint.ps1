Write-Host "Running isort..." -ForegroundColor Cyan
isort .

Write-Host "`nRunning black..." -ForegroundColor Cyan
black .

Write-Host "`nRunning flake8..." -ForegroundColor Cyan
flake8 .

Write-Host "`nDone!" -ForegroundColor Green
