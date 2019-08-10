function makeRow() {
	console.log('test');
	var table = document.getElementById("av");

	var row = table.insertRow(1);
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	var cell3 = row.insertCell(2);
	var cell4 = row.insertCell(3);
	var cell5 = row.insertCell(4);

	cell1.innerHTML ="Hollandsch nieuwsblad";
	cell2.innerHTML ="Rotterdam";
	cell3.innerHTML ="1943";
	cell4.innerHTML ="science";
	cell5.innerHTML ="-";
}

function row(){
	document.getElementById("demo").innerHTML= Date();
}
