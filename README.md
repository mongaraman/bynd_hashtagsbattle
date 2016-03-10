##Beyond Hash Tags Battle
=========================


Prepare Local Enviornment
--------------------------

Requires Python 2.7 or higher
django 1.9 or higher
pyenchant using sudo pip install pyenchant
apscheduler 3.0 or higher use sudo pip install apscheduler
or download and install from
https://pypi.python.org/pypi/APScheduler/
Install dependencies: `sudo pip install -r requirements.txt`

if pip does not work try following commands on linux:
`apt-get remove python-pip`
`easy_install pip`

Install python 2.7.x or higher version from https://www.python.org/downloads/
or use following commands
 - wget https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz 
 - tar xzvf Python-2.7.6.tgz 
 - cd Python-2.7.6.tgz
 - ./configure
 - sudo make
 - sudo make install

Install and run django-1.9
sudo pip install django

- Outputs a JSON string as below:

Output:
Its a web app which has django admin and front end for hash tags battle.
It crawls twitter with provided hashtags under a battle record and then
calculate number of tweets and spelling mistakes for each individual hashtags.
It updates django tables in sqllite and show the winner on the basis of
more number of tweets or less number of spelling mistakes.


##Tests
Run tests with following command after reaching to checked out folder location

`python -m unittest test_crawler` from hashtagbattles director
`python manage.py test`


