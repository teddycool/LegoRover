

<?php
    $command = $_REQUEST["command"];
    $sys_c = "echo " . $command . " >> /home/pi/named_pipe.fifo";
	system($sys_c);
?>