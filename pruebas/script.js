// Crear el mapa de Google
var map;
function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: 48.856614, lng: 2.3522219},
		zoom: 5
	});
}

// Cargar el archivo CSV y agregar marcadores al mapa
function loadCSV(file) {
	var reader = new FileReader();
	reader.onload = function(event) {
		var csv = event.target.result;
		var markers = csv.split("\n");
		for (var i = 0; i < markers.length; i++) {
			var fields = markers[i].split(",");
			var position = {lat: parseFloat(fields[2]), lng: parseFloat(fields[3])};
			var marker = new google.maps.Marker({
				position: position,
				title: fields[1],
				map: map,
				icon: 'http://maps.google.com/mapfiles/ms/icons/grey-dot.png'
			});
			marker.addListener('click', function() {
				this.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
				var list = document.getElementById('markers-list');
				list.value += this.getTitle() + "\n";
			});
		}
	};
	reader.readAsText(file);
}

// Manejar el evento de selección de archivo
var fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', function() {
	loadCSV(this.files[0]);
});
