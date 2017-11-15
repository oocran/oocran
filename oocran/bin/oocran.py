import os


def run(url):
    if not os.path.exists('log'):
        os.makedirs('log')
    os.system('cd oocran/django && celery -A oocran worker -l info &>> log/worker.log &')
    os.system('cd oocran/django && celery -A oocran beat -l info -S django &>> log/scheduler.log &')
    os.system('cd oocran/django && python manage.py runserver '+url)