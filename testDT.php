<!DOCTYPE html>
<html lang="en">

<title>Test Distributed Tracing</title>
<h5>Test de DT ... running ... </h5>

<h7>
<?php
	echo "Runs on : " . gethostname() . " (" . getHostByName(getHostName()) .")";

	$output = shell_exec('ls -al /tmp');
	echo "$output";

?>
</h7>


</html>

