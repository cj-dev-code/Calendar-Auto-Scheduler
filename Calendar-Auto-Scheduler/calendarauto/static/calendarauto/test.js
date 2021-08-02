// Create one dimensional array
// Contains information about what info should be in this block
var block_info = new Array(24);

// Contains information about what type of block this is: 
// empty, text, filled
var block_types = new Array(24);

function showCoords(event) {
    var x = event.clientX;
    var y = event.clientY;
    var coords = "X coords: " + x + ", Y coords: " + y;

    document.getElementById("demo").innerHTML = coords;
    // Fix this, borken when clicking in the popup window
    // If less than 50 go to the task list
    if (event.button == -1)
        return;
    else if (x < 50) {
        var str = window.location.href;
        const myArr = str.split("/");
        
        
        // Gets the url for the new page, currently hardcoded, could be improved
        var new_url = "";
        for (let i = 0; i < 4; i++) {
            new_url += myArr[i] + "/";
        }
        
        window.location.replace(new_url + 'Todo');
    }
    var canvas = document.getElementById("myCanvas");
    // For the mystery view
    if (x > (canvas.width + 50)) {
        var str = window.location.href;
        const myArr = str.split("/");
        
        
        // Gets the url for the new page, currently hardcoded, could be improved
        var new_url = "";
        for (let i = 0; i < 4; i++) {
            new_url += myArr[i] + "/";
        }
        
        window.location.replace(new_url + 'Todo');
    }
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

function openInfoBox() {
    document.getElementById("infobox").style.display = "block";
}

function closeInfoBox() {
    document.getElementById("infobox").style.display = "none";
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
            var study_quizzes_checkbox = document.createElement("input");
            study_quizzes_checkbox.type = "checkbox";
            study_quizzes_checkbox.id = "study_quizzes";
            document.getElementById("specForm").appendChild(study_quizzes_checkbox);
            var study_quizzes_label = document.createElement("label");
            study_quizzes_label.setAttribute("for", "study_quizzes");
            study_quizzes_label.innerHTML = "<strong>Quizzes</strong>";
            document.getElementById("specForm").appendChild(study_quizzes_label);
            break;
        case 'Wk':
            break;
        case 'Er':
            var errand_route_checkbox = document.createElement("input");
            errand_route_checkbox.type = "checkbox";
            errand_route_checkbox.id = "errand_route";
            document.getElementById("specForm").appendChild(errand_route_checkbox);
            var errand_route_label = document.createElement("label");
            errand_route_label.setAttribute("for", "errand_route");
            errand_route_label.innerHTML = "<strong>Plan Route</strong>";
            document.getElementById("specForm").appendChild(errand_route_label);
            break;
        case 'Rd':
            break;
        case 'Hb':
            var hobby_grow_checkbox = document.createElement("input");
            hobby_grow_checkbox.type = "checkbox";
            hobby_grow_checkbox.id = "hobby_grow";
            document.getElementById("specForm").appendChild(hobby_grow_checkbox);
            var hobby_grow_label = document.createElement("label");
            hobby_grow_label.setAttribute("for", "hobby_grow");
            hobby_grow_label.innerHTML = "<strong>Grow</strong>";
            document.getElementById("specForm").appendChild(hobby_grow_label);
            
            var hobby_enjoy_checkbox = document.createElement("input");
            hobby_enjoy_checkbox.type = "checkbox";
            hobby_enjoy_checkbox.id = "hobby_enjoy";
            document.getElementById("specForm").appendChild(hobby_enjoy_checkbox);
            var hobby_enjoy_label = document.createElement("label");
            hobby_enjoy_label.setAttribute("for", "hobby_enjoy");
            hobby_enjoy_label.innerHTML = "<strong>Enjoy</strong>";
            document.getElementById("specForm").appendChild(hobby_enjoy_label);
            
            var hobby_review_checkbox = document.createElement("input");
            hobby_review_checkbox.type = "checkbox";
            hobby_review_checkbox.id = "hobby_review";
            document.getElementById("specForm").appendChild(hobby_review_checkbox);
            var hobby_review_label = document.createElement("label");
            hobby_review_label.setAttribute("for", "hobby_review");
            hobby_review_label.innerHTML = "<strong>Review</strong>";
            document.getElementById("specForm").appendChild(hobby_review_label);
            break;
        default:
            break;
    }
    //var input = document.createElement("input");
    //input.type = "text";
    //document.getElementById("specForm").appendChild(input);
}

function rgbToHex(r, g, b) {
    if (r > 255 || g > 255 || b > 255)
        throw "Invalid color component";
    return ((r << 16) | (g << 8) | b).toString(16);
}


/**
 * Return the location of the element (x,y) being relative to the document.
 * 
 * @param {Element} obj Element to be located
 */
function getElementPosition(obj) {
    var curleft = 0, curtop = 0;
    if (obj.offsetParent) {
        do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
        return { x: curleft, y: curtop };
    }
    return undefined;
}


/** 
 * return the location of the click (or another mouse event) relative to the given element (to increase accuracy).
 * @param {DOM Object} element A dom element (button,canvas,input etc)
 * @param {DOM Event} event An event generate by an event listener.
 */
function getEventLocation(element,event){
    // Relies on the getElementPosition function.
    var pos = getElementPosition(element);
    
    return {
    	x: (event.pageX - pos.x),
      	y: (event.pageY - pos.y)
    };
}

function getURLDate() {
    // Gets the day of the month
    var str = window.location.href;
        
    const myArr = str.split("/");
        
    var day = myArr[6];
    var month = myArr[5];
    var year = myArr[4];
    
    return {year, month, day};
}

function getTimeClicked(hour_block, day_of_week) {
    var date = getURLDate();
        
    var new_date = new Date(date.year, date.month - 1, date.day, hour_block - 1);
        
    // getDay() gets the day of the week (0-6)
    new_date.setDate(new_date.getDate() - (new_date.getDay() - (day_of_week - 1)));
    
    return new_date;
}

function showDay(event) {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    var eventLocation = getEventLocation(canvas, event);

    // Get info based on color pixel clicked, deprecated to using arrays
    var pixelData = ctx.getImageData(eventLocation.x, eventLocation.y, 1, 1).data; 

    // If transparency on the pixel , array = [0,0,0,0]
    //if((pixelData[0] == 0) && (pixelData[1] == 0) && (pixelData[2] == 0) && (pixelData[3] == 0)){
        // Do something if the pixel is transparent
    //}
    
    var rect = canvas.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    
    
    
    // Checks for clicking on the previous or next buttons
    if ((y < 30) && (x < Math.floor(canvas.width/9))) {
        window.location.replace(getFrontUrl(true, false));
        return;  
    }
    else if ((y < 30) && (x > canvas.width - Math.floor(canvas.width/9))) {
        window.location.replace(getFrontUrl(true, true));  
        return;
    }
    
    var hour_block = Math.floor(y / 30);
    var day_of_week = Math.floor(x / (canvas.width/9));
    
    if ((hour_block == 0) || (day_of_week == 0) || (day_of_week == 8))
        return;
    
    
    //var hex = "#" + ("000000" + rgbToHex(pixelData[0], pixelData[1], pixelData[2])).slice(-6);
    if (block_types[hour_block - 1][day_of_week - 1] == "filled") {
        var new_date = getTimeClicked(hour_block, day_of_week);
        
        const objects = JSON.parse(document.getElementById('blocks').textContent);
        
        for (x of objects) {
            var sche_date = new Date(x.datetime);
            // Have to set the hour back by one because the timezone of the back-end is in Chicago Time (Central Time)
            sche_date.setHours(sche_date.getHours() - 1);

            if ((sche_date.getFullYear() == new_date.getFullYear()) && (sche_date.getMonth() == new_date.getMonth()) && (sche_date.getDate() == new_date.getDate()) && (sche_date.getHours() == new_date.getHours())) {
                openInfoBox();
            }
        }
        
    }
    else if (block_types[hour_block - 1][day_of_week - 1] == "text") {
        var new_date = getTimeClicked(hour_block, day_of_week);
        
        const objects = JSON.parse(document.getElementById('blocks').textContent);
        
        for (x of objects) {
            var sche_date = new Date(x.datetime);
            // Have to set the hour back by one because the timezone of the back-end is in Chicago Time (Central Time)
            sche_date.setHours(sche_date.getHours() - 1);

            if ((sche_date.getFullYear() == new_date.getFullYear()) && (sche_date.getMonth() == new_date.getMonth()) && (sche_date.getDate() == new_date.getDate()) && (sche_date.getHours() == new_date.getHours())) {
                openInfoBox();
            }
        }
    }
    // i.e. when the cell is undefined
    else {
        switch (hour_block) {
            case 1:
                document.getElementById("start_hour").value = "12am";
                document.getElementById("end_hour").value = "1am";
                document.getElementById("start_time1").value = "12am";
                document.getElementById("end_time1").value = "1am";
                break;
            case 2:
                document.getElementById("start_hour").value = "1am";
                document.getElementById("end_hour").value = "2am";
                document.getElementById("start_time1").value = "1am";
                document.getElementById("end_time1").value = "2am";
                break;
            case 3:
                document.getElementById("start_hour").value = "2am";
                document.getElementById("end_hour").value = "3am";
                document.getElementById("start_time1").value = "2am";
                document.getElementById("end_time1").value = "3am";
                break;
            case 4:
                document.getElementById("start_hour").value = "3am";
                document.getElementById("end_hour").value = "4am";
                document.getElementById("start_time1").value = "3am";
                document.getElementById("end_time1").value = "4am";
                break;
            case 5:
                document.getElementById("start_hour").value = "4am";
                document.getElementById("end_hour").value = "5am";
                document.getElementById("start_time1").value = "4am";
                document.getElementById("end_time1").value = "5am";
                break;
            case 6:
                document.getElementById("start_hour").value = "5am";
                document.getElementById("end_hour").value = "6am";
                document.getElementById("start_time1").value = "5am";
                document.getElementById("end_time1").value = "6am";
                break;
            case 7:
                document.getElementById("start_hour").value = "6am";
                document.getElementById("end_hour").value = "7am";
                document.getElementById("start_time1").value = "6am";
                document.getElementById("end_time1").value = "7am";
                break;
            case 8:
                document.getElementById("start_hour").value = "7am";
                document.getElementById("end_hour").value = "8am";
                document.getElementById("start_time1").value = "7am";
                document.getElementById("end_time1").value = "8am";
                break;
            case 9:
                document.getElementById("start_hour").value = "8am";
                document.getElementById("end_hour").value = "9am";
                document.getElementById("start_time1").value = "8am";
                document.getElementById("end_time1").value = "9am";
                break;
            case 10:
                document.getElementById("start_hour").value = "9am";
                document.getElementById("end_hour").value = "10am";
                document.getElementById("start_time1").value = "9am";
                document.getElementById("end_time1").value = "10am";
                break;
            case 11:
                document.getElementById("start_hour").value = "10am";
                document.getElementById("end_hour").value = "11am";
                document.getElementById("start_time1").value = "10am";
                document.getElementById("end_time1").value = "11am";
                break;
            case 12:
                document.getElementById("start_hour").value = "11am";
                document.getElementById("end_hour").value = "12pm";
                document.getElementById("start_time1").value = "11am";
                document.getElementById("end_time1").value = "12pm";
                break;
            case 13:
                document.getElementById("start_hour").value = "12pm";
                document.getElementById("end_hour").value = "1pm";
                document.getElementById("start_time1").value = "12pm";
                document.getElementById("end_time1").value = "1pm";
                break;
            case 14:
                document.getElementById("start_hour").value = "1pm";
                document.getElementById("end_hour").value = "2pm";
                document.getElementById("start_time1").value = "1pm";
                document.getElementById("end_time1").value = "2pm";
                break;
            case 15:
                document.getElementById("start_hour").value = "2pm";
                document.getElementById("end_hour").value = "3pm";
                document.getElementById("start_time1").value = "2pm";
                document.getElementById("end_time1").value = "3pm";
                break;
            case 16:
                document.getElementById("start_hour").value = "3pm";
                document.getElementById("end_hour").value = "4pm";
                document.getElementById("start_time1").value = "3pm";
                document.getElementById("end_time1").value = "4pm";
                break;
            case 17:
                document.getElementById("start_hour").value = "4pm";
                document.getElementById("end_hour").value = "5pm";
                document.getElementById("start_time1").value = "4pm";
                document.getElementById("end_time1").value = "5pm";
                break;
            case 18:
                document.getElementById("start_hour").value = "5pm";
                document.getElementById("end_hour").value = "6pm";
                document.getElementById("start_time1").value = "5pm";
                document.getElementById("end_time1").value = "6pm";
                break;
            case 19:
                document.getElementById("start_hour").value = "6pm";
                document.getElementById("end_hour").value = "7pm";
                document.getElementById("start_time1").value = "6pm";
                document.getElementById("end_time1").value = "7pm";
                break;
            case 20:
                document.getElementById("start_hour").value = "7pm";
                document.getElementById("end_hour").value = "8pm";
                document.getElementById("start_time1").value = "7pm";
                document.getElementById("end_time1").value = "8pm";
                break;
            case 21:
                document.getElementById("start_hour").value = "8pm";
                document.getElementById("end_hour").value = "9pm";
                document.getElementById("start_time1").value = "8pm";
                document.getElementById("end_time1").value = "9pm";
                break;
            case 22:
                document.getElementById("start_hour").value = "9pm";
                document.getElementById("end_hour").value = "10pm";
                document.getElementById("start_time1").value = "9pm";
                document.getElementById("end_time1").value = "10pm";
                break;
            case 23:
                document.getElementById("start_hour").value = "10pm";
                document.getElementById("end_hour").value = "11pm";
                document.getElementById("start_time1").value = "10pm";
                document.getElementById("end_time1").value = "11pm";
                break;
            case 24:
                document.getElementById("start_hour").value = "11pm";
                document.getElementById("end_hour").value = "12am";
                document.getElementById("start_time1").value = "11pm";
                document.getElementById("end_time1").value = "12am";
                break;
            default:
                break;
        }

        
            
        // Gets the day of the month
        var date = getURLDate();
            
        var new_date = new Date(date.year, date.month - 1, date.day);
        
        // getDay() gets the day of the week (0-6)
        new_date.setDate(new_date.getDate() - (new_date.getDay() - (day_of_week - 1)));
        document.getElementById("DAY").value = new_date.getDate();
        document.getElementById("day_week").value = day_of_week;
        
        openScheduleForm();
    }
}

// Not used
function drawCal(hour_block, day_week) {
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    
    for (let i = 1; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo((canvas.width/9)*(i + day_week), 30 * hour_block);
        ctx.lineTo((canvas.width/9)*(i + day_week), 30 * (hour_block + 1));
        ctx.stroke();
    }
    
    // Adds the time on the left 
    for (let i = hour_block - 1; i < hour_block + 1; i++) {
        ctx.beginPath();
        ctx.moveTo((canvas.width/9)*(day_week + 1), 30 * (i + 1));
        ctx.lineTo((canvas.width/9)*(day_week + 2), 30 * (i + 1));
        ctx.stroke();
    }
}

// Wait for page to load
// Contains the eventListener for most elements
document.addEventListener('DOMContentLoaded', function() {
    // Clears the info in the global arrays
    block_info = new Array(24);
    block_types = new Array(24);
    // Fills the cells with the value of undefined
    for (var i = 0; i < block_info.length; i++) {
        block_info[i] = new Array(7);
        block_types[i] = new Array(7);
    }
    
    // Creates the horizontal lines in the canvas
    var canvas = document.getElementById("myCanvas");
    
    const objects = JSON.parse(document.getElementById('tasks').textContent);
    console.log(objects);
    const objects2 = JSON.parse(document.getElementById('blocks').textContent);
    console.log(objects2);
    const sunday = JSON.parse(document.getElementById('sunday').textContent);
    var date_sunday = new Date(sunday);
    const saturday = JSON.parse(document.getElementById('saturday').textContent);
    var date_saturday = new Date(saturday);
    date_saturday.setDate(date_saturday.getDate() + 1);
    
    
    // Only has the string version
    const hour_info = JSON.parse(document.getElementById('info').textContent);
    
    // Drawing on the canvas
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
    const week_day_labels = ["Sun","Mon","Tues","Wed","Thurs","Fri","Sat"];
    var label_line_height = 30;
    ctx.font = "25px Arial";
    ctx.strokeText("<- Previous", 0, label_line_height - 5);
    var temp_date = new Date(date_sunday);
    for (let i = 1; i <= week_day_labels.length; i++) {
        ctx.strokeText(week_day_labels[i-1] + "(" + temp_date.getDate() + ")", (canvas.width/9)*i, label_line_height - 5);
        temp_date.setDate(temp_date.getDate() + 1);
    }
    ctx.strokeText("Next ->", (canvas.width/9)*8, label_line_height - 5);
    
    // Adds the time on the left 
    for (let i = 0; i <= 23; i++) {
        ctx.beginPath();
        ctx.moveTo(0, label_line_height + 30 * i);
        ctx.lineTo(canvas.width, label_line_height + 30 * i);
        ctx.stroke();
        
        if (i == 0) {
            ctx.strokeText("12 am-1 am", 0, label_line_height + 30*(i + 1) - 4);
        }
        else if (i < 11) {
            ctx.strokeText((i % 12) + " am-" + ((i % 12) + 1) + " am", 0, label_line_height + 30*(i + 1) - 4);
        }
        else if (i == 11) {
            ctx.strokeText("11 am-12 pm", 0, label_line_height + 30*(i + 1) - 4);
        }
        else if (i == 12) {
            ctx.strokeText("12 pm-1 pm", 0, label_line_height + 30*(i + 1) - 4);
        }
        else if (i == 23) {
            ctx.strokeText("11 pm-12 am", 0, label_line_height + 30*24 - 4);
        }
        else {
            ctx.strokeText((i % 12) + " pm-" + ((i % 12) + 1) + " pm", 0, label_line_height + 30*(i + 1) - 4);
        }
    }
    // End of drawing on the canvas
    for (x of objects2) {
        var sche_date = new Date(x.datetime);
        // Have to set the hour back by one because the timezone of the back-end is in Chicago Time (Central Time)
        sche_date.setHours(sche_date.getHours() - 1);
        x.datetime = sche_date;
        ctx.fillStyle = "#FF0000";
        if ((sche_date > date_sunday) && (sche_date < date_saturday)) {
            block_info[sche_date.getHours()][sche_date.getDay()] = x;
            if (x.current_task_id != null) {
                block_types[sche_date.getHours()][sche_date.getDay()] = 'filled';
                ctx.fillRect((sche_date.getDay() + 1) * (canvas.width/9), (sche_date.getHours() + 1) * 30, (canvas.width/9), 30);
                ctx.fillStyle = 'black';
                ctx.fillText(x.hour_type + " " + objects[x.current_task_id - 1].task_name, (sche_date.getDay() + 1) * (canvas.width/9), label_line_height + 30*(sche_date.getHours() + 1) - 4);
            }
            else {
                block_types[sche_date.getHours()][sche_date.getDay()] = 'text';
                ctx.fillStyle = 'black';
                ctx.fillText(x.hour_type, (sche_date.getDay() + 1) * (canvas.width/9), label_line_height + 30*(sche_date.getHours() + 1) - 4);
            }
        }
    }
    console.table(block_info);
    
});