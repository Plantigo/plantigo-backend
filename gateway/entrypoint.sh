#!/bin/bash
set -e

/code/generate_proto_files.sh

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
