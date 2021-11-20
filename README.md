# AskPython
Q&amp;A forum for Python developers

## How To Run
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createcachetable
python3 manage.py generate_database --profiles 5 --question 100 --answers 5 --tags 10 --votes 10
python3 manage.py runserver 0.0.0.0:8080
```