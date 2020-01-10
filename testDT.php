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

	
	$output = shell_exec('/usr/bin/python3 /tmp/script1.py');
	echo "<pre>$output</pre>";   

?>


</html>

