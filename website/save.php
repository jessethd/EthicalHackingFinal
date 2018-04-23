<?php
session_start();
ob_start();
$key1=$_POST['key1'];
$file = fopen('log.txt', 'a');
fwrite($file, '' . $_SERVER['REMOTE_ADDR'] . '-' . $key1 . PHP_EOL);
fclose($file);
echo "Success!";
sleep(6);
ob_end_flush();
?>
