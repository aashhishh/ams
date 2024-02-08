# ams
Attendance Management system
Dependencies
Python 3.10.2 or higher, tested with 3.10.2 only

You can use pyenv to manage different version of python

Pipenv

Dependency management

Install dependencies with pipenv install

Setup
Create a log directory name logs outside AMS directory.

Make sure your current working directory is AMS.

Create a file name .env.

Install dependencies by running the command pipenv install

Start project-

i) pipenv run uvicorn app:AMS

^ these jobs should be present in the app/jobs directory

By Default it will run on the 127.0.0.1:8000.
go to -> 127.0.0.1:8000/docs     to access the swagger ui
