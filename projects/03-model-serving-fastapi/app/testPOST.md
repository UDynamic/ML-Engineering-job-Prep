
``` Powershell
$body = Get-Content testSample.json -Raw
Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -Body $body -ContentType "application/json"
```