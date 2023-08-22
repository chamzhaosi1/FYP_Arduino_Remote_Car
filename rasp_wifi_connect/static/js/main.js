// wifi_refresh = function() {
//   // start rotate the refresh image
//   $('#refresh_btn').addClass('rotate');

  // Get response wifi list from backend
  // $.ajax({
  //   url: '/refresh_wifi',
  //   method: 'GET',
  //   success: function(data) {
  //     // console.log(data);
  //     // insert the data into the select box
  //     var options = '<option selected>Select one of the SSID</option>';
  //     for (var i = 0; i < data.length; i++) {
  //       options += '<option value="' + data[i]+ '">' + data[i] + '</option>';
  //     }
  //     $('#ssid').html(options);

  //     // stop rotate the refresh image
  //     $('#refresh_btn').removeClass('rotate');

  //   },
  //   error: function(jqXHR, textStatus, errorThrown) {
  //     console.error(errorThrown);
  //   }
  // });
// }

function wifi_refresh() {
  // start rotate the refresh image
  console.log(document.getElementById('refresh_btn'))
  document.getElementById('refresh_btn').classList.add('rotate');

  fetch('/refresh_wifi')
      .then(response => response.json())
      .then(data => {
        console.log(data)

        var options = '<option selected>Select one of the SSID</option>';
        for (var i = 0; i < data.length; i++) {
          options += '<option value="' + data[i]+ '">' + data[i] + '</option>';
        }
        document.getElementById('ssid').innerHTML = options;
        // stop rotate the refresh image
        document.getElementById('refresh_btn').classList.remove('rotate');
      })
      .catch(error => console.error(error));
}

