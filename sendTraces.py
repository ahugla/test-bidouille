#!/usr/bin/env python3

# Your need to tell your OS that this is a Python program, otherwise, it's interpreted as a shell script


import sys

timeBefore=sys.argv[1]
timeAfter=sys.argv[2]
#print('arguments : ' +timeBefore +' et ' +timeAfter)

timeDelta=timeAfter-timeBefore



fichier = open("/var/www/html/script2.log", "a")
message = 'timeBefore: ' +timeBefore +'  et   timeAfter: ' +timeAfter +'   =>   timeDelta=' +timeDelta
fichier.write(message)
fichier.close()








#message = 'script2.py completed ! avec variable: ' +googleDelay
#print(message)
