function getCoordinates(localite) {
	var STATUS_OK = 200;

	var request = new XMLHttpRequest();
	request.addEventListener('load', function(event) {
		if (request.status === STATUS_OK) {
			if (JSON.parse(request.responseText).results[0] === undefined) {
				console.log(localite);
			} else {
				var coordinates = JSON.parse(request.responseText).results[0].geometry.location;
				console.log(localite + ',' + coordinates.lat + ',' + coordinates.lng);
			}
		} else {
			console.log(localite);
		}
	});

	var url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + localite.replace(' ', '+');
	request.open('GET', url);
	request.send();
}

var localites = ['Conakry',
'Gueckedou',
'Kankan',
'Kissidougou',
'Lofa County',
'Macenta',
'National',
'Dabola',
'Dinguiraye',
'Bong County',
'Grand Cape Mount',
'Margibi County',
'Montserrado County',
'Nimba County',
'Grand Gedeh',
'Telimele',
'Kailahun',
'Boffa',
'Bo',
'Kenema',
'Koinadugu',
'Moyamba',
'Bombali',
'Freetown',
'Kouroussa',
'Kambia',
'Kono',
'Port Loko',
'Western Area',
'Boffa',
'Conakry',
'Dabola',
'Dubreka',
'Gueckedou',
'Kissidougou',
'Kouroussa',
'Macenta',
'Nzerekore',
'Pita',
'Siguiri',
'Yomou',
'Bomi County',
'Grand Bassa',
'River Gee County',
'RiverCess County',
'Sinoe County',
'Lagos',
'Bonthe',
'Pujehun',
'Tonkolili',
'Western Area Rural',
'Western Area Urban',
'Dinguiraye',
'Pita',
'Siguiri',
'Western area rural',
'Western area urban',
'Forécariah',
'Gbarpolu County',
'Rivers',
'Dakar',
'Kerouane',
'Coyah',
'Gbarpolu County',
'District Nord',
'Mbao',
'Maryland County',
'Bomi County',
'Bong County',
'Grand Bassa',
'Grand Gedeh',
'Lofa County',
'Margibi County',
'Montserrado County',
'Nimba County',
'Dalaba',
'Maryland County',
'Bo',
'Bombali',
'Bonthe',
'Kailahun',
'Kambia',
'Kenema',
'Koinadugu',
'Kono',
'Moyamba',
'National',
'Port Loko',
'Pujehun',
'Tonkolili',
'Grand Kru',
'RiverCess County',
'Sinoe County',
'Western area urban',
'Kindia',
'Beyla',
'Lola',
'Faranah',
'Boke',
'Western Area',
'Mamou',
'Commune 2',
'Kayes',
'Commune 5',
'Commune 1',
'Koutiala',
'Selingue'];

for (var i = 100; i < 110; i++) {
	getCoordinates(localites[i]);
}