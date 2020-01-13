#!/usr/bin/python3

fichier = open("/var/www/html/script2.log", "a")
fichier.write("execution de script2.py")
fichier.close()

message = 'script2.py completed !'
print(message)

