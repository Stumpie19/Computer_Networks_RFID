<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<style>
body
{
  font-family: 'Times New Roman', Times, serif, white;
  background-color: #1394eb;
  text-align: "center";
}
</style>
<body>
<?php

$hostname = "localhost";
$username = "CNuser";
$password = "CNpassword";
$db = "CNattendance";

$dbconnect=mysqli_connect($hostname,$username,$password,$db);

if ($dbconnect->connect_error) {
  die("Database connection failed: " . $dbconnect->connect_error);
}

?>
<h1 align="center">Attendance Table<h1>
<table border="1" align="center">
<tr>
  <td>uid</td>
  <td>name</td>
  <td>in/out</td>
  <td>time in</td>
  <td>time out</td>
</tr>

<?php

$query = mysqli_query($dbconnect, "SELECT * FROM attendance")
   or die (mysqli_error($dbconnect));

while ($row = mysqli_fetch_array($query)) {
  echo
   "<tr>
    <td>{$row['uid']}</td>
    <td>{$row['name']}</td>";
    
    if ($row['enter'] == '1')
      echo " <td>in</td>";
    else
      echo " <td>out</td>";
    echo "<td>";
    echo date('m-d-Y H:i:s', $row['timestamp_in']);
    echo "</td><td>";
    echo date('m-d-Y H:i:s', $row['timestamp_out']);
    echo "</td></tr>\n";


}

?>
</table>
</body>
</html>
