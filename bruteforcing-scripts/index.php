<html>
    <body>
        <h1>Login</h1>
        <form action="login" method="POST">
            <label for="username">Username:</label>
            <input type="text" name="username">
            <label for="password">Password:</label>
            <input type="password" name="password">
            <input type="submit" name="login" value="Login">
        </form>
    </body>
</html>

<?php
$nl = "\r\n ";

// should exist in a sql-db instead!
$valid_password ='$2y$10$8YptZF7jjcqfHunw77sjkOdKeoqyvCMmJV6vjEBJ0SLzTXGunUJ.a'; //megasecurepasswordlol
$valid_username = 'admin';

if (isset($_POST['login'])){
  $username = $_POST['username'];
  $password = $_POST['password'];

  $valid_password = password_hash($password, PASSWORD_DEFAULT); 
  $verify = password_verify($password, $valid_password); 
  
    if ($verify == 1 and $username === $valid_username) {
        header("HTTP/1.1 200");
        echo nl2br("$nl$nl Login successful! =)"); 
         }
    else { 
        header("HTTP/1.1 401 Unauthorized");
        echo nl2br("$nl$nl Login failed");
         }
} 
?>