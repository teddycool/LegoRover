
$( "#speedSlider" ).slider();
$( "#turnSlider" ).slider();
$( "#turnSlider" ).slider({
  change: function( event, ui ) {
  var t = $( "#turnSlider" ).slider( "value" );
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("phpinfo").innerHTML = xmlhttp.responseText;
            }
        };
  var get_str = "send_command.php?command=set_turn " + t;
  xhttp.open("GET", get_str, true);
  xhttp.send();
  }
});

$( "#speedSlider" ).slider({
  change: function( event, ui ) {
  var s = $( "#speedSlider" ).slider( "value" );
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                document.getElementById("phpinfo").innerHTML = xmlhttp.responseText;
            }
        };

  var get_str = "send_command.php?command=set_speed " + s;
  xhttp.open("GET", get_str, true);
  xhttp.send();

  $("#speed").text("Speed: " + s);
  }
});
