@echo off
echo Recipe Collection App Setup
echo ============================

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Testing installation...
python test_setup.py

if %errorlevel% == 0 (
    echo.
    echo Setup completed successfully!
    echo.
    echo To run the application, execute:
    echo streamlit run recipe_collection.py
    echo.
    pause
) else (
    echo.
    echo Setup failed. Please check the error messages above.
    pause
)
