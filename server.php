<?php
    if($_POST["func"] == "start_server"){
        $ret = exec("cd work", $output, $result);
        exec("python -m http.server --cgi 8888");
        echo($result);
    }
?>