echo " BUILD START"
python3.9.6  -m pip install -r requirements.txt
python3.9.6 manage.py collectstatic  --noinput --clear
echo " BUILD END"