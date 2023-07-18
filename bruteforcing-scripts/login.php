<?php
//@jockemedlinux
if (isset($_POST['login'])){
    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($username == "admin" and $password == "password"){
        header("HTTP/1.1 200");
        echo "Login successful!";
    }

    elseif ($username == "jenkins" and $password == "jenkins"){
        header("HTTP/1.1 200");
        echo "Login successful!";
    }

    elseif ($username == "jocke" and $password == "password"){
        header("HTTP/1.1 200");
        echo "Login successful!";
    }
    else {
        header("HTTP/1.1 401 Unauthorized");
        echo "Wrong username or password!";
	}
}
?>
