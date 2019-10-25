<?php
    // if($_POST["func"] == "cgi"){
    //     $ret = exec("cd work", $output, $result);
    //     exec("python -m http.server --cgi 3000");
    // }
    // else if($_POST["func"] == "websocket"){
    //     exec("python cgi-bin/server.py &");
    // }
    exec("python cgi-bin/server.py &");
    exec("python -m http.server --cgi 3000 &");
?>