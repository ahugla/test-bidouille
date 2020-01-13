#!/usr/bin/env python3

# Your need to tell your OS that this is a Python program, otherwise, it's interpreted as a shell script


import sys

var2='OK'
print('var2 : ' +var2)

var3=sys.argv[1]
print('argument : ' +var3)

fichier = open("/var/www/html/script2.log", "a")
fichier.write("execution de script2.py")
fichier.close()

message = 'script2.py completed ! avec variable: ' +var3
print(message)
