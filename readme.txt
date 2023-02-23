## Create VM local machine
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
$ pip install fastapi[all]
$ pip install "passlib[bcrypt]"
$ pip install "python-jose[cryptography]"
$ pip freeze                                ## To show all pkg

$ uvicorn main:app                          ## run App
uvicorn app.main:app --reload

## https://docs.sqlalchemy.org/en/14/
$ pip install SQLAlchemy




https://youtu.be/0sOvCWFmrtA?t=20688

#git commit to branch
#https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/git-push-new-branch-remote-github-gitlab-upstream-example

task-4-routers

github@branch/c/remote/push  (new-branch)
git clone https://github.com/ristonhen/fastapi.git
cd git*
git checkout -b task-2

github@branch/c/remote/push (task-2)
git branch -a
touch devolution.jpg
git add .
git commit -m "connect pg"
git push --set-upstream origin task-4-routers

github@branch/c/remote/push (new-branch)
touch eden.html
git add .
git commit -m "Completed normal API"
git push origin



### HTTP Request message status code .
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status