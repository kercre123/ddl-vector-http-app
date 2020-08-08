function getVicstatus() {

var client = new HttpClient();

var app = document.getElementById('vicstatus')

client.get('/api/fancy/status', function(response) {

		app.innerHTML = ''

        var data = JSON.parse(response)

        const h3 = document.createElement('h3')
        h3.textContent = data.status

        app.appendChild(h3)
});
}

function getVicimage() {

var client = new HttpClient();

var imgstatus = document.getElementById('vicimagestatus');

const imgstatush3 = document.createElement('h3');
imgstatush3.textContent =  "Getting...";

imgstatus.innerHTML = '';

imgstatus.appendChild(imgstatush3);

client.get('/api/extras/get_image', function() {

		  var img = document.createElement("img");
		  img.src = "/api/extras/get_latest_image" + '?' + (new Date()).getTime();
		  var src = document.getElementById('vicimage');

		  src.innerHTML = '';
		  imgstatus.innerHTML = '';

          src.appendChild(img);
});
}

function getVicimageprocessed() {

var client = new HttpClient();

var imgstatus = document.getElementById('vicimagestatus');

const imgstatush3 = document.createElement('h3');
imgstatush3.textContent =  "Getting...";

imgstatus.innerHTML = '';

imgstatus.appendChild(imgstatush3);

client.get('/api/extras/get_image_processed', function() {

		  var img = document.createElement("img");
		  img.src = "/api/extras/get_latest_image"+ '?' + (new Date()).getTime();
		  var src = document.getElementById('vicimage');

		  src.innerHTML = '';
		  imgstatus.innerHTML = '';

          src.appendChild(img);
});
}

function getVicvimageprocessed() {

var client = new HttpClient();

var imgstatus = document.getElementById('vicimagestatus');

const imgstatush3 = document.createElement('h3');
imgstatush3.textContent =  "Getting...";

imgstatus.innerHTML = '';

imgstatus.appendChild(imgstatush3);

client.get('/api/extras/get_image_v_processed', function() {

		  var img = document.createElement("img");
		  img.src = "/api/extras/get_latest_image"+ '?' + (new Date()).getTime();
		  var src = document.getElementById('vicimage');

		  src.innerHTML = '';
		  imgstatus.innerHTML = '';

          src.appendChild(img);
});
}
