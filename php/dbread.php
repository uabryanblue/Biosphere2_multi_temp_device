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
}

else { echo "Connected to mysql database. <br>"; }


// Select values from MySQL database table

$sql = "SELECT id, val1, val2, date FROM nodemcu_table ORDER BY date DESC LIMIT 10";
// echo $sql;
$result = $conn->query($sql);

echo "<center>";



if ($result->num_rows > 0) {


    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<strong> Id:</strong> " . $row["id"]. " &nbsp <strong>val:</strong> " . $row["val1"]. " &nbsp <strong>val2:</strong> " . $row["val2"]. " &nbsp <strong>Date:</strong> " . $row["date"]. " <p>";
    


}
} else {
    echo "0 results";
}

echo "</center>";

$conn->close();



?>
