#!/usr/bin/env python3

# Your need to tell your OS that this is a Python program, otherwise, it's interpreted as a shell script

fichier = open("/var/www/html/script1.log", "a")
fichier.write("execution de script1.py")
fichier.close()

message = 'script1.py completed !'
print(message)

