@echo off
REM Скрипт запуска визуализатора алгоритмов шифрования

echo ========================================
echo Визуализатор Алгоритмов Шифрования
echo ========================================
echo.

REM Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не установлен или не в PATH
    echo Пожалуйста установите Python 3.8+
    pause
    exit /b 1
)

echo ✓ Python найден

REM Проверяем виртуальное окружение
if not exist "venv" (
    echo.
    echo 📦 Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Ошибка при создании виртуального окружения
        pause
        exit /b 1
    )
    echo ✓ Виртуальное окружение создано
)

REM Активируем окружение
echo.
echo 🔌 Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Устанавливаем зависимости
echo.
echo 📥 Установка зависимостей...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)
echo ✓ Зависимости установлены

REM Запускаем приложение
echo.
echo 🚀 Запуск приложения...
echo.
echo ========================================
echo ✓ Сервер запущен!
echo ========================================
echo.
echo 🌐 Откройте браузер и перейдите на:
echo    http://127.0.0.1:5000
echo.
echo Нажмите Ctrl+C для остановки сервера
echo ========================================
echo.

python app.py

pause
