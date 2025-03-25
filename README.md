This Project runs in a virtual environment which in future wont get affected of new environmental updates

How to create a Virtual environment?
- cd into the project directory
- python3 -m venv <envName> 
- finally set the interpreter path to the venv's python exe.
- set the terminals is also using the virtual env path: venv\Scripts\activate.bat

- In this project following will be the steps:
    - open main.py in terminal
    - python3 -m venv venv
    - control+shift+P and select  Python: Select Interpreter
    - put the following path: .\venv\Scripts\python3.exe (where . means current dir)
    - now in the terminal run this command: venv\Scripts\activate.bat

- pip install fastapi
- pip install uvicorn

