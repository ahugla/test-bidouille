#!/usr/bin/env python3

# Your need to tell your OS that this is a Python program, otherwise, it's interpreted as a shell script


import sys

googleDelay=sys.argv[1]
#print('argument : ' +googleDelay)

	fichier = open("/var/www/html/script2.log", "a")
	message = 'googleDelay: ' +googleDelay
	fichier.write(message)
	fichier.close()

#message = 'script2.py completed ! avec variable: ' +googleDelay
#print(message)
