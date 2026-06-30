@echo off

echo ============================
echo Building ZIP PDF Merger
echo ============================

python -m pip install --upgrade pip
pip install -r requirements.txt

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ZipPDFMerger" ^
    app.py

echo.
echo ============================
echo Build Complete
echo ============================
pause