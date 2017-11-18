import os


def run(args):
    if args[1] == "start" and args[2] is not None:
        if not os.path.exists('log'):
            os.makedirs('log')
        os.system('cd oocran/django && celery -A oocran worker -l info &>> log/worker.log')
        os.system('cd oocran/django && celery -A oocran beat -l info -S django &>> log/scheduler.log')
        os.system('cd oocran/django && python manage.py runserver '+args[2])
    elif args[1] == "reset":
        print "reset"
    elif args[1] == "help":
        print """
Type 'oocran help <subcommand>' for help on a specific subcommand.

Available
subcommands:

[oocran]
start
reset
help
            """
    else:
        print """
Orden not found!

Type 'oocran help <subcommand>' for help on a specific subcommand.

Available
subcommands:

[oocran]
start
reset
help
            """