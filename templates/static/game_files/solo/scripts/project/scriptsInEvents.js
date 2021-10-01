


const scriptsInEvents = {

		async EventSheet1_Event1_Act21(runtime, localVars)
		{
			// send highscore
			let csrftoken = "csrftoken";
			if (document.cookie && document.cookie !== '') {
			    const cookies = document.cookie.split(';');
			    for (let i = 0; i < cookies.length; i++) {
			        const cookie = cookies[i].trim();
			        // Does this cookie string begin with the name we want?
			        if (cookie.substring(0, csrftoken.length + 1) === (csrftoken + '=')) {
			            csrftoken = decodeURIComponent(cookie.substring(csrftoken.length + 1));
			            break;
			        }
			    }
			}
			runtime.globalVars.CSRFtoken = String(csrftoken)
			
			if(runtime.globalVars.CSRFtoken == runtime.globalVars.save_CSRFtoken 
			   || runtime.globalVars.save_CSRFtoken == "" || runtime.globalVars.save_CSRFtoken == null )
				runtime.globalVars.is_new_csrf=false
			
			var url = "/_api/HighScore/";
			var xhr = new XMLHttpRequest();
			xhr.open("GET", url, false);
			xhr.setRequestHeader("Content-type", "application/json");
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
			xhr.onreadystatechange = function () {
			    if (xhr.readyState == 4 && xhr.status == 200) {
			        var json = JSON.parse(xhr.responseText);
			        console.log("score received")
			    }
			}
			xhr.onload = function () {
			    var jsonResponse = JSON.parse(xhr.response);
			    runtime.globalVars.curr_highscore = parseInt(jsonResponse["highScore"])
			    runtime.globalVars.curr_high_fortune = parseInt(jsonResponse["highFortune"])
			};
			xhr.send(null);
			
			console.log("curr_highscore " + runtime.globalVars.curr_highscore);
			console.log("curr_high_fortune " + runtime.globalVars.curr_high_fortune);
			
		}

};

self.C3.ScriptsInEvents = scriptsInEvents;

