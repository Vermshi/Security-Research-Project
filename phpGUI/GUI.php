
<?php



if(isset($_POST["startTest"])){
$host="127.0.0.1" ;
$port=12345;
$timeout=30;
$sk=fsockopen($host,$port,$errnum,$errstr,$timeout) ;

if (!is_resource($sk)) {
    exit("connection fail: ".$errnum." ".$errstr) ;
} else {
    echo "Connected";
    $data = json_decode(fgets($sk,128));
    echo "<br>";
    echo "Input from server: ";
    foreach ($data as $d) {
    	echo "<br>";
    	echo $d;
    }
}
}


?>

<h2>Start tests</h2>
<form method="post" action="gui.php">
  <input type="submit" name="startTest" value="Start tests">  
</form>
