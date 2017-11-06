import os

secret = os.urandom(32).encode('base-64').split('\n')[0]

file = open("OOCRAN/oocran/secret_key.py", "w+")
file.write("SECRET_KEY = '"+secret+"'")
file.close()

