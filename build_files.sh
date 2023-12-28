python3.9 -m pip install -r requirements.txt
python3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput --clear
python3.9 manage.py python-decouple
python3.9 manage.py decouple
