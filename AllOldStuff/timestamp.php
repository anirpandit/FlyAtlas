<?php // content="text/plain; charset=utf-8"
// outputs e.g.  somefile.txt was last modified: December 29 2002 22:16:23.

$now=time();
$filename = 'freezer.txt';
if (file_exists($filename)) {
    $diff=$now - filemtime($filename);
    $text='<font color=\"red\">may be DOWN!</font>';
    if ($diff<3600) {
       $text=' is UP.';
       }
$fp = @fopen('freezer.txt', "r"); 
   $line = trim(fgets($fp));
fclose($fp);
   $data = explode("\t",$line);
   $temp = $data[0];


    echo "<a href=\"http://tubules.net/test0.php\">Freezer room</a> monitor $text: $temp C.   \n";
}
$filename = 'flyroom.txt';
if (file_exists($filename)) {
    $diff=$now - filemtime($filename);
    $text='<font color=\"red\">may be DOWN!</font>';
    if ($diff<3600) {
       $text=' is UP.';
       }
//get last reading
$fp = @fopen('flyroom.txt', "r"); 
   $line = trim(fgets($fp));
fclose($fp);
   $data = explode(",",$line);
   $temp = $data[0];
   $humid= $data[1];
   $lux =$data[2];

    echo "<a href=\"http://tubules.net/flyroom.php\">Fly room</a> monitor $text: $temp C, $humid % r.h.\n";
}
?>
