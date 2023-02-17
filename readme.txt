## Create VM local machine
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
$ pip install fastapi[all]
$ pip freeze ## To show all pkg

$ uvicorn main:app                          ## run App
uvicorn main:app --reload
