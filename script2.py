#!/usr/bin/python3

$var2 = % (sys.argv[1])

fichier = open("/var/www/html/script2.log", "a")
fichier.write("execution de script2.py")
fichier.close()

message = 'script2.py completed ! avec variable: ' $var2
print(message)

