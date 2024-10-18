@echo off
REM Change directory to where your app.py is located
cd /d "C:\Users\abhin\Desktop\SE_Project - Copy\app.py"  REM Update this path to your app.py directory

REM Activate the virtual environment
call source mchatbot/Scripts/activate  REM Update this if your virtual environment has a different name

REM Run the Flask application
python app.py
