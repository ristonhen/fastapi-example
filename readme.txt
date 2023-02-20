## Create VM local machine
$ py -3 -m venv venv
$ venv\Scripts\activate.bat
$ pip install fastapi[all]
$ pip freeze                                ## To show all pkg

$ uvicorn main:app                          ## run App
uvicorn main:app --reload







#git commit to branch
#https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/git-push-new-branch-remote-github-gitlab-upstream-example



github@branch/c/remote/push  (new-branch)
git clone https://github.com/ristonhen/fastapi.git
cd git*
git checkout -b task-1

github@branch/c/remote/push (task-1)
git branch -a
touch devolution.jpg
git add .
git commit -m "Are we not gender neutral people? We are Devo?"
git push --set-upstream origin task-1

github@branch/c/remote/push (new-branch)
touch eden.html
git add .
git commit -m "Eden added"
git push origin



### HTTP Request message status code .
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status