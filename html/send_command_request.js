

  function send_command_request(command,value) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                document.getElementById("phpinfo").innerHTML = xhttp.responseText;
            }
        };
  var get_str = "send_command.php?command=" + command +" " + value;
  xhttp.open("GET", get_str, true);
  xhttp.send();
  }
