<!DOCTYPE html>
<html lang="en">

<title>Test Distributed Tracing</title>
<h5>Test de DT ... running ... </h5>


<?php
	echo "Runs on : " . gethostname() . " (" . getHostByName(getHostName()) .")";

  	#  OK
    #$output = 'ma chaine';
	#echo "$output";

	# OK
    #$output = shell_exec('pwd');
	#echo "<pre>$output</pre>";      # => /var/www/html
    #$output = shell_exec('whoami'); 
	#echo "<pre>$output</pre>";      # => apache

	# OK
	# configurer le <Directory "/var/www/html"> dans /etc/httpd/conf/httpd.conf  
	# METTRE AU DEBUT :   #!/usr/bin/python3    INDISPENSABLE
	# RENDRE LES FICHIERS EXECUTABLES (chmod)
	$output = shell_exec('/var/www/html/script1.py');
	echo "<pre>$output</pre>";   

    	/*   EXEMPLE DE SCRIPT PYTHON
     	#!/usr/bin/python3
	    fichier = open("/var/www/html/script1.log", "a")
	    fichier.write("ca marche")
	    fichier.close()
	    message = 'en cours'
	    print(message)
	    */

	sleep(1);    # Attends que le sleep se termine pour afficher la totalité de la page web 
	

    #shell_exec returns all of the output stream as a string.
    #exec returns the last line of the output by default, but can provide all output as an array specifed as the second parameter.

    $output2 = shell_exec('/var/www/html/script2.py ARG1');
	echo "<pre>$output2</pre>";   

	#$output = shell_exec('/tmp/test-bidouille/sendTrace-proxy.py');
	#echo "<pre>$output</pre>";   


	$cmd = "/var/www/html/script2.py ID_123";
	$result = shell_exec($cmd);
	echo "<pre>$result</pre>";




   # ROOT TRACE





























?>


</html>


<!-- 
# https://wiki.centos-webpanel.com/apache-run-python-script

-->