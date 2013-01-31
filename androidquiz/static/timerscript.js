var mins;
var secs;
				
function cd() {
 	mins = 1 * m("05"); // change minutes here
 	secs = 0 + s(":01"); // change seconds here (always add an additional second to your total)
 	redo();
}

function m(obj) {
 	for(var i = 0; i < obj.length; i++) {
  		if(obj.substring(i, i + 1) == ":")
  		break;
 	}
 	return(obj.substring(0, i));
}

function s(obj) {
 	for(var i = 0; i < obj.length; i++) {
  		if(obj.substring(i, i + 1) == ":")
  		break;
 	}
 	return(obj.substring(i + 1, obj.length));
}

function dis(mins,secs) {
 	var disp;
 	if(mins <= 9) {
  		disp = " 0";
 	} else {
  		disp = " ";
 	}
 	disp += mins + ":";
 	if(secs <= 9) {
  		disp += "0" + secs;
 	} else {
  		disp += secs;
 	}
 	return(disp);
}

    function redo() {
 	secs--;
 	if(secs == -1) {
  		secs = 59;
  		mins--;
 	}

 	document.getElementById('txt').innerHTML = dis(mins,secs); // setup additional displays here.
 	if((mins == 0) && (secs == 0)) {
  		call_action();
 	} else {
 		cd = setTimeout("redo()",1000);
 	}
}

function init() {
  cd();
}

function call_action() {
  var form = document.getElementById('quizform');
  form.submit();
}
