//create ajax object. Doesnt support Internet Explorer
function makeRequestObject(callback) {
	if(window.XMLHttpRequest) {
		var myajaxrequest = new XMLHttpRequest();
		myajaxrequest.onreadystatechange = function() {
			if(myajaxrequest.readyState == 4) {
				if(myajaxrequest.status == 200) //send response to callback
					callback(myajaxrequest.responseText);
				else if(myajaxrequest.status == 404)
					callback('Page not Found');
			}
		}
	}	
	else 
		return false;	
}

// generic ajax request maker
function makePostRequest(method ,url, data,callback) {
	var myrequest = makeRequestObject(callback);
	myrequest.open("POST",url,true);
	myrequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	myrequest.send(data);
} 