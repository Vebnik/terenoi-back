#!/bin/bash

cd terenoi
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput
deactivate
sudo systemctl restart terenoi
sudo systemctl restart nginx
