console.log('Hello');

const week_day_labels = ["Sunday","Monday","Tuesday", "Wednesday","Thursday","Friday","Saturday"];

var list = document.getElementById("firstList");

var node = document.createElement('li');

node.appendChild(document.createTextNode('Sunday'));

list.appendChild(node);