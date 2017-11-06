#!/usr/bin/env bash

python ../install/key.py
cd ../OOCRAN
#Create database
python manage.py makemigrations
python manage.py migrate
#Create admin User
CODE=""
while read line
do
    CODE="$CODE$line;"
done < ../install/create_admin.py
echo "$CODE" | python manage.py shell &> /dev/null
echo ""
echo "Installation Finished!!"
echo "Write oocran start IP:PORT to start server."