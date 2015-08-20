<?php
/*  JATD test  */
header("Pragma: no-cache");

error_reporting(E_ERROR | E_WARNING | E_PARSE);
 echo "<h1>Add a new fly stock</h1>";
?>
<form action="<?php echo $PHP_SELF;?>" method="POST">
Stock tray/number location (e.g. A14, Julian Office tray): <input type="text" name="location" size="60"><br>
Genotype (e.g. w[1118], actin-GAL4/CyO): <input type="text" name="genotype" size="60"><br>
Chromosomes affected (e.g. X, II): <input type="chromosome" name="chromosome" size="60"><br>
Description (e.g. orange eyes, stubble): <input type="text" name="description" size="60"><br>
Source/ comments (e.g. gift of Karl Thummel, EcR promoter-GFP fusion): <input type="text" name="comments" size="60"><br>
<input type="submit" /><br>
</form>
<?php
$searchstring = $_POST["location"];
if (strlen ($searchstring)>1) {
   $stringData = $_POST["location"]."\t".$_POST["genotype"]."\t".$_POST["chromosome"]."\t".$_POST["description"]."\t".$_POST["comments"]."\n";
   $myFile = "stocks.txt";
   $fh = fopen($myFile, 'a') or die("can't open file");
   fwrite($fh, $stringData);
   fclose($fh);
  echo "<p>Wrote the following to the database:<br>".$stringData."</p>";
   echo "<p>If you spot an error, ask Julian to correct it!</p>"; 
}


?>
