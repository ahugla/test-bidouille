#!/usr/bin/python3

fichier = open("/var/www/html/script1.log", "a")
fichier.write("execution de script1.py")
fichier.close()

message = 'script1.py terminé'
print(message)

