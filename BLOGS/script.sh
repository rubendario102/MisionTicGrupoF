#!/bin/bash
echo Starting my app.
cd  /home/ubuntu/MisionTicGrupoF/BLOGS
pwd
ls
source tutorial-env/bin/activate
gunicorn --workers=5 -b 0.0.0.0:443 --certfile=micertificado.pem --keyfile=llaveprivada.pem wsgi:application
