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

client.get('/api/extras/get_image', function() {

		  var img = document.createElement("img")
		  img.src = "/image/vector_img.png"
		  var src = document.getElementById('vicimage')

		  src.innerHTML = ''

          src.appendChild(img)
});
}