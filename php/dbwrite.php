<?php



$host = "localhost";		         // host = localhost because database hosted on the same server where PHP files are hosted
$dbname = "id20554738_biosphere2";              // Database name
$username = "id20554738_lazuline";		// Database username
$password = "o%Ts+!&LZGY5K~Rt";	        // Database password


// Establish connection to MySQL database
$conn = new mysqli($host, $username, $password, $dbname);


// Check if connection established successfully
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    echo "Connected to mysql database: " . $host . "<p>"; 
}

   
// Get date and time variables
    //date_default_timezone_set('Asia/Kolkata');  // for other timezones, refer:- https://www.php.net/manual/en/timezones.asia.php
//    $d = date("Y-m-d");
//    $t = date("H:i:s");

// htmlspecialchars($_GET['val1']);

echo "post data: <p>";
foreach( $_GET as $stuff => $val ) {
    if( is_array( $stuff ) ) {
        foreach( $stuff as $thing) {
            echo $thing . "<p>";
        }
    } else {
        echo $stuff . " : " . $val . "<p>";
        // echo $val;
    }
}
echo "wrote out post data <p>";    

// If values send by NodeMCU are not empty then insert into MySQL database table
$val1 = htmlspecialchars($_GET['val1']);
$val2 = htmlspecialchars($_GET['val2']);

echo $val1 . " : " . $val2 . "<p>";

  if(!empty($val1) && !empty($val2) )
    {


        echo "creating SQL with:" . $val1 . " and " . $val2 . "<p>";
// Update your tablename here
	    $sql = "INSERT INTO nodemcu_table (val1, val2) VALUES ('".$val1."','".$val2."')"; 
        echo "Trying sql: " . $sql;
 


		if ($conn->query($sql) === TRUE) {
		    echo "Values inserted in MySQL database table.";
		} else {
		    echo "Error: " . $sql . "<p>" . $conn->error;
		}
	}


// Close MySQL connection
$conn->close();
echo "Closed connection to db. <p>"


?>
