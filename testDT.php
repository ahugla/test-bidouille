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

	
	# METTRE AU DEBUT :   #!/usr/bin/python3
	$output = shell_exec('/var/www/html/script1.py');
	echo "<pre>$output</pre>";   

?>


</html>


<!-- 
# https://wiki.centos-webpanel.com/apache-run-python-script

-->