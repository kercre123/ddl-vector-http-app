function getVicstatus() {
   const app = document.getElementById('root')
   
   var client = new HttpClient();
client.get('/api/fancy/status', function(response) {

          var data = JSON.parse(response)

          const h3 = document.createElement('h3')
          h3.textContent = data.status

          app.appendChild(h3)
});
}