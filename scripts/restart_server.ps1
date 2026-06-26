# 🚀 Quick Flask Restart Script
# Run this script to restart your Flask server with cache-busting enabled

Write-Host "🔧 Restarting Flask Server with Cache-Busting..." -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\admin\OneDrive\Documents\food order system"

# Activate virtual environment
Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Clear terminal
Clear-Host

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║        🍕 SMART FOOD ORDERING SYSTEM 🍕                   ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║        Ultra-Vibrant Dashboard Active! ✨                 ║" -ForegroundColor Magenta
Write-Host "║        Cache-Busting Enabled! 🚀                          ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""
Write-Host "📍 Starting Flask server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "✨ IMPORTANT: After server starts:" -ForegroundColor Cyan
Write-Host "   1. Open browser" -ForegroundColor White
Write-Host "   2. Press Ctrl+Shift+R (hard refresh)" -ForegroundColor White
Write-Host "   3. Login as customer" -ForegroundColor White
Write-Host "   4. See the ULTRA-VIBRANT dashboard! 🌈" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Server will be at: http://localhost:5000" -ForegroundColor Green
Write-Host "🛑 Press Ctrl+C to stop server" -ForegroundColor Red
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

# Start Flask
python app.py
