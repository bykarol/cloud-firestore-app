rem Activate virtual environment
call venv\Scripts\activate

rem Change to the project directory
cd mywebapp_project

rem Run the Django server
start /B python manage.py runserver

rem Return to root directory
cd ..