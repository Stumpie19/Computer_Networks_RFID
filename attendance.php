<!--Webpage for Viewing Attendance Database !-->
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
  <!--Attendance Table Login Form !-->
  <form action = attendance.php method = "post" style ="text-align: center;" autocomplete="off">
    <h1 align="center">Attendance Table</h1>
    <table border="1" align="center">
      <tr style = "text-align: center;">
        <th style = "text-align: center;"> username </th>
        <th style = "text-align: center;"> password </th>
      </tr>
      <tr style = "text-align: center;">
        <td><input type = "text" name = "username" size = "16" value = "" style = "text-align: center;"></td>
        <td><input type = "password" name = "password" size = "16" value = "" style = "text-align: center;"></td>
      </tr>
    </table>  
    <p style = "text-align: center;">
      <input type = "submit" value = "Login" style="font-size:17px">
    </p>
  </form>

<?php
  //if empty page is loaded don't throw error(for first opening of page)
  if(empty($_POST["username"]) && empty($_POST["password"]))
  {
    exit;
  }
  
  //connect to database
  $hostname = "localhost";//hostname
  $db = "CNattendance";//database name
  $username = $_POST["username"];//get username from form
  $password = $_POST["password"];//get password from form
  $dbconnect=mysqli_connect($hostname,$username,$password,$db);

  if (!$dbconnect)//check for successful connection if no then throw error and quit
  {
    echo "<p style = \"text-align: center;\">Either username or password are incorrect. Try again.</p>";
    exit;
  }

  //query attendance table
  $query = mysqli_query($dbconnect, "SELECT * FROM attendance") or die (mysqli_error($dbconnect));

  //add table column names to page
  echo "<table border=\"1\" align=\"center\">
    <tr>
      <td>uid</td>
      <td>name</td>
      <td>in/out</td>
      <td>time in</td>
      <td>time out</td>
    </tr>";

  //loop through table and info to table
  while ($row = mysqli_fetch_array($query)) {
    //add uid and name to table
    echo
    "<tr>
      <td>{$row['uid']}</td>
      <td>{$row['name']}</td>";
    
    //get enter boolean from table convert to in/out and add to table
    if ($row['enter'] == '1')
      echo " <td>in</td><td>";
    else
      echo " <td>out</td><td>";
    
    //convert time in epoch time to readable time and add to table
    echo date('m-d-Y H:i:s', $row['timestamp_in']);
    echo "</td><td>";
    
    //convert time out epoch time to readable time and add to table
    echo date('m-d-Y H:i:s', $row['timestamp_out']);
    echo "</td></tr>\n";


  }

?>
</table>
</body>
</html>
