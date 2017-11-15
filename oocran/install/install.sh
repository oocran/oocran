###
#    Open Orchestrator Cloud Radio Access Network
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
###

#!/usr/bin/env bash

python key.py
cd ../django
#Create database
python manage.py makemigrations
python manage.py migrate
#Create admin User
CODE=""
while read line
do
    CODE="$CODE$line;"
done < oocran/install/create_admin.py
echo "$CODE" | python manage.py shell &> /dev/null