function showCoords(event) {
    var x = event.clientX;
    var y = event.clientY;
    var coords = "X coords: " + x + ", Y coords: " + y;
    document.getElementById("demo").innerHTML = coords;
    // If less than 50 go to the task list
    /*if (x < 50) {
        var str = window.location.href;
        const myArr = str.split("/");
        
        
        // Gets the url for the new page, currently hardcoded, could be improved
        var new_url = "";
        for (let i = 0; i < 4; i++) {
            new_url += myArr[i] + "/";
        }
        
        window.location.replace(new_url + 'Todo/');
    }
    var canvas = document.getElementById("myCanvas");
    // For the mystery view
    if (x > canvas.width) {
        var str = window.location.href;
        const myArr = str.split("/");
        
        
        // Gets the url for the new page, currently hardcoded, could be improved
        var new_url = "";
        for (let i = 0; i < 4; i++) {
            new_url += myArr[i] + "/";
        }
        
        window.location.replace(new_url + 'Todo/');
    }*/
}

function getFrontUrl(date, next_week) {
    // window.location.href is a function to determine what the url of the current page is
    // it returns a string that contains the full url of the current page
    // Use whenever you want to get the url of the page
    var str = window.location.href;
    // split function to seperate the string with the character specified
    // returns an array of the string seperated when that character appears
    // Use whenever you want a string to be seperated be a certain character
    const myArr = str.split("/");
    
    // Gets the url for the new page, currently hardcoded, could be improved
    var new_url = "";
    for (let i = 0; i < 4; i++) {
        new_url += myArr[i] + "/";
    }
    
    if (date) {
        var day = myArr[6];
        var month = myArr[5];
        var year = myArr[4];
        
        var new_date = new Date(year, month - 1, day);
        if (next_week) {
            new_date.setDate(new_date.getDate() + 7);
        }
        else {
            // getDay() gets the day of the week (0-6)
            new_date.setDate(new_date.getDate() - 7);
        }   
        new_url += new_date.getFullYear() + "/" + (new_date.getMonth() + 1) + "/" + new_date.getDate() + "/";
    }
   
    return new_url;
}

function openForm() {
    document.getElementById("popupForm").style.display = "block";
}

function closeForm() {
    document.getElementById("popupForm").style.display = "none";
}

function openScheduleForm() {
    document.getElementById("schedulepopupForm").style.display = "block";
}

function closeScheduleForm() {
    document.getElementById("schedulepopupForm").style.display = "none";
}

function changeForm() {
    document.getElementById("specForm").innerHTML = '';
    var sel = document.getElementById('taskType');
    var opt = sel.options[sel.selectedIndex];
 
    switch (opt.value) {
        case 'SF':
            var friend_list_label = document.createElement("label");
            friend_list_label.for = "friends";
            friend_list_label.innerHTML = "<strong>Friend List:</strong>";
            document.getElementById("specForm").appendChild(friend_list_label);
            var friend_select = document.createElement("select");
            document.getElementById("specForm").appendChild(friend_select);
            
            var friend_desc_label = document.createElement("label");
            friend_desc_label.for = "friend_desc";
            friend_desc_label.innerHTML = "<strong>Description:</strong>";
            document.getElementById("specForm").appendChild(friend_desc_label);
            var friend_desc_input = document.createElement("input");
            friend_desc_input.type = "text";
            document.getElementById("specForm").appendChild(friend_desc_input);
            
            var friend_loc_label = document.createElement("label");
            friend_loc_label.for = "friend_loc";
            friend_loc_label.innerHTML = "<strong>Location:</strong>";
            document.getElementById("specForm").appendChild(friend_loc_label);
            var friend_loc_input = document.createElement("input");
            friend_loc_input.type = "text";
            document.getElementById("specForm").appendChild(friend_loc_input);
            break;
        case 'SR':
            break;
        case 'SA':
            break;
        case 'Tr':
            var travel_dest_label = document.createElement("label");
            travel_dest_label.for = "travel_dest";
            travel_dest_label.innerHTML = "<strong>Destination:</strong>";
            document.getElementById("specForm").appendChild(travel_dest_label);
            var travel_dest_input = document.createElement("input");
            travel_dest_input.type = "text";
            document.getElementById("specForm").appendChild(travel_dest_input);
            
            var travel_start_label = document.createElement("label");
            travel_start_label.for = "travel_start";
            travel_start_label.innerHTML = "<strong>Start:</strong>";
            document.getElementById("specForm").appendChild(travel_start_label);
            var travel_start_input = document.createElement("input");
            travel_start_input.type = "text";
            document.getElementById("specForm").appendChild(travel_start_input);
            break;
        case 'St':
            break;
        case 'Wk':
            break;
        case 'Er':
            break;
        case 'Rd':
            break;
        case 'Hb':
            break;
        default:
            break;
    }
    //var input = document.createElement("input");
    //input.type = "text";
    //document.getElementById("specForm").appendChild(input);
}

function showDay(event) {
    var canvas = document.getElementById("myCanvas");
    var rect = canvas.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    
    

    if ((y < 30) && (x < Math.floor(canvas.width/9))) {
        window.location.replace(getFrontUrl(true, false));  
    }
    else if ((y < 30) && (x > canvas.width - Math.floor(canvas.width/9))) {
        /*// window.location.href is a function to determine what the url of the current page is
        // it returns a string that contains the full url of the current page
        // Use whenever you want to get the url of the page
        var str = window.location.href;
        // split function to seperate the string with the character specified
        // returns an array of the string seperated when that character appears
        // Use whenever you want a string to be seperated be a certain character
        const myArr = str.split("/");
        console.log(myArr);
        var day = myArr[6];
        var month = myArr[5];
        var year = myArr[4];
        
        var new_date = new Date(year, month - 1, day);
        
        
        // Gets the url for the new page, currently hardcoded, could be improved
        var new_url = "";
        for (let i = 0; i < 4; i++) {
            new_url += myArr[i] + "/";
        }
        
        window.location.replace(new_url + new_date.getFullYear() + "/" + (new_date.getMonth() + 1) + "/" + new_date.getDate() + "/");  */
        window.location.replace(getFrontUrl(true, true));  
    }
    switch (Math.floor(y / 30)) {
        case 1:
            document.getElementById("temp").innerHTML = "1am";
            document.getElementById("start_hour").value = "1am";
            
            break;
        case 2:
            document.getElementById("temp").innerHTML = "2am";
            break;
        case 3:
            document.getElementById("temp").innerHTML = "3am";
            break;
        case 4:
            document.getElementById("temp").innerHTML = "4am";
            break;
        case 5:
            document.getElementById("temp").innerHTML = "5am";
            break;
        case 6:
            document.getElementById("temp").innerHTML = "6am";
            break;
        case 7:
            document.getElementById("temp").innerHTML = "7am";
            break;
        case 8:
            document.getElementById("temp").innerHTML = "8am";
            break;
        case 9:
            document.getElementById("temp").innerHTML = "9am";
            break;
        case 10:
            document.getElementById("temp").innerHTML = "10am";
            break;
        case 11:
            document.getElementById("temp").innerHTML = "11am";
            break;
        case 12:
            document.getElementById("temp").innerHTML = "12pm";
            break;
        case 13:
            document.getElementById("temp").innerHTML = "1pm";
            break;
        case 14:
            document.getElementById("temp").innerHTML = "2pm";
            break;
        case 15:
            document.getElementById("temp").innerHTML = "3pm";
            break;
        case 16:
            document.getElementById("temp").innerHTML = "4pm";
            break;
        case 17:
            document.getElementById("temp").innerHTML = "5pm";
            break;
        case 18:
            document.getElementById("temp").innerHTML = "6pm";
            break;
        case 19:
            document.getElementById("temp").innerHTML = "7pm";
            break;
        case 20:
            document.getElementById("temp").innerHTML = "8pm";
            break;
        case 21:
            document.getElementById("temp").innerHTML = "9pm";
            break;
        case 22:
            document.getElementById("temp").innerHTML = "10pm";
            break;
        case 23:
            document.getElementById("temp").innerHTML = "11pm";
            break;
        case 24:
            document.getElementById("temp").innerHTML = "12am";
            break;
        default:
            break;
    }
    switch (Math.floor(x / (canvas.width/9))) {
        case 1:
            document.getElementById("temp").innerHTML += "Sunday";
            document.getElementById("end_hour").value = "2am";
            break;
        case 2:
            document.getElementById("temp").innerHTML += "Monday";
            break;
        case 3:
            document.getElementById("temp").innerHTML += "Tuesday";
            break;
        case 4:
            document.getElementById("temp").innerHTML += "Wednesday";
            break;
        case 5:
            document.getElementById("temp").innerHTML += "Thursday";
            break;
        case 6:
            document.getElementById("temp").innerHTML += "Friday";
            break;
        case 7:
            document.getElementById("temp").innerHTML += "Saturday";
            break;
        default:
            break;
    }
    if ((y > 30) && (x > Math.floor(canvas.width/9)))
        openScheduleForm();
}



// Wait for page to load
// Contains the eventListener for most elements
document.addEventListener('DOMContentLoaded', function() {
    var e = document.getElementById("scheForm");
    //console.log(e.children);
    
    // Creates the horizontal lines in the canvas
    var canvas = document.getElementById("myCanvas");
    
    canvas.width = window.screen.width - 130;
    var ctx = canvas.getContext("2d");

    var num_days = 7;
    for (let i = 0; i < num_days + 3; i++) {
        ctx.beginPath();
        ctx.moveTo((canvas.width/9)*i, 0);
        ctx.lineTo((canvas.width/9)*i, canvas.height);
        ctx.stroke();
    }
    
    // Adds the top labels to the calendar
    const week_day_labels = ["Sunday","Monday","Tuesday", "Wednesday","Thursday","Friday","Saturday"];
    var label_line_height = 30;
    ctx.font = "25px Arial";
    ctx.strokeText("<- Previous", 0, label_line_height - 5);
    for (let i = 1; i <= week_day_labels.length; i++) {
        ctx.strokeText(week_day_labels[i-1], (canvas.width/9)*i, label_line_height - 5);
    }
    ctx.strokeText("Next ->", (canvas.width/9)*8, label_line_height - 5);
    
    // Adds the time on the left 
    for (let i = 0; i <= 23; i++) {
        ctx.beginPath();
        ctx.moveTo(0, label_line_height + 30 * i);
        ctx.lineTo(canvas.width, label_line_height + 30 * i);
        ctx.stroke();
        
        if (i < 11) {
            ctx.strokeText(((i % 12) + 1) + " am", 0, label_line_height + 30*(i + 1) - 4);
        }
        else if (i == 23) {
            ctx.strokeText("12 am", 0, label_line_height + 30*24 - 4);
        }
        else {
            ctx.strokeText(((i % 12) + 1) + " pm", 0, label_line_height + 30*(i + 1) - 4);
        }
    }
});