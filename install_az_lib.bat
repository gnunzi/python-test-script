@echo off
echo Downloading package
echo Unzipping
echo Creating python virtual environment
python -m venv .venv
pause
echo Switching to virtual environment
pause
echo Installing dependencies
pip install -r azlib_requirements.txt