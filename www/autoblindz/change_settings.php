<html>
	<head>
		<title>The Results </title>
	</head>

	<?php
		ini_set('display_errors', 1); //set to 0 for production version
		error_reporting(E_ALL);

		$priority = $_REQUEST['priority'];
		$light_thr = $_REQUEST['light_thr'];
		$sch_blin = $_REQUEST['sch_blin'];
		$sch_shut = $_REQUEST['sch_shut'];
	?>
	<body bgcolor="#FFFFFF" text="#000000">

	I will now check what you want changed... <br>
	<?php
		$fn = "/home/pi/Desktop/AutoBlindz/settings.txt"; //file name
		$fh = fopen($fn, 'r') or die("<br> can't open file"); //file handle
		$theData = fread($fh, filesize($fn));
		fclose($fh);
		print ("The file says $theData.<br>");
	?>

	<br> What you did not leave blank was... <br>
	<?php
		$update = "X";
		if ($priority != "") {
			print ($priority);
			$update = $update."&".$priority;
		} else {
			$update = $update."&no";
		}

		if ($light_thr != "") {
			print ($light_thr);
			$update = $update."&".$light_thr;
		} else {
			$update = $update."&no";
		}

		if ($sch_blin != "") {
			print ($sch_blin);
			$update = $update."&".$sch_blin;
		} else {
			$update = $update."&no";
		}

		if ($sch_shut != "") {
			print ($sch_shut);
			$update = $update."&".$sch_shut;
		} else {
			$update = $update."&no";
		}
	?>

	<br> 
	<br> I will make the changes now... <br>

	The text file will say:
	<?php
	print ("$update.<br>");
	

	$fh = fopen($fn, 'w') or die("<br> can't open file");
	$sd = $update;
	fwrite($fh, $sd);
	fclose($fh);

	print("The file now says ");
	$fh = fopen($fn, 'r') or die("<br> can't open file");
	$theData = fread($fh, filesize($fn));
	fclose($fh);
	print ($theData);

	?>

	<br> 
	<br> The changes have been made. <br> 
	The priority is now <b> <?php print ($priority); ?>.</b><br> 
	The light threshold is now <b> <?php print ($light_thr); ?>.</b><br> 
	The schedule for the looveres is now <b> <?php print ($sch_blin); ?>.</b><br> 
	The schedule for the shutters is now <b> <?php print ($sch_shut); ?>.</b><br> 
	<p>
	Thank you for using AutoBlindz.
	</body>
</html>
