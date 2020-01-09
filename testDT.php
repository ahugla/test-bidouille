<!DOCTYPE html>
<html lang="en">

<title>Test Distributed Tracing</title>
<h5>Test de DT ... running ... </h5>

<h7>
<?php
	echo "Runs on : " . gethostname() . " (" . getHostByName(getHostName()) .")";

   
   exec("/usr/bin/python3 /test/script1.py");

	
    

?>
</h7>


</html>

