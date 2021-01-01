$(function(){
  var lat1, lng1, lat2, lng2, address, client_lat, client_lng, client_address;
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(geoSuccess);
  } else {
      alert("Geolocation is not supported by this browser.");
  }
  function geoSuccess(position)
  {
    lat1 = parseFloat(position.coords.latitude);
    lng1 = parseFloat(position.coords.longitude);
    lat2 = $('#google_map_btn').data('lat');
    lng2 = $('#google_map_btn').data('long');
    address = $('#google_map_btn').data('address');
    client_address = $('#google_map_client_btn').data('address');
    address = address.replace('#', '')
    client_address = client_address.replace('#', '');
    
    
    // if((lat2 == '' || lng2 == '')||(lat2 == 'None' || lng2 == 'None'))
    // {
    geocoder = new google.maps.Geocoder();
    if (geocoder) {
        geocoder.geocode({
            'address': address
        }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
              lat2 = parseFloat(results[0].geometry.location.lat());
              lng2 = parseFloat(results[0].geometry.location.lng());
            }
        });
    }
    // }
    // else
    // {
    //   lat2 = parseFloat(lat2);
    //   lng2 = parseFloat(lng2);
    // }

    geocoder = new google.maps.Geocoder();
    if (geocoder) {
        geocoder.geocode({
            'address': client_address
        }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
              client_lat = parseFloat(results[0].geometry.location.lat());
              client_lng = parseFloat(results[0].geometry.location.lng());
            }
        });
    }


  }
  $('#google_map_btn').click(function(){
      url = "http://maps.google.com/maps?saddr=" + lat1+ "," + lng1+ "&daddr="+ address;
      var win = window.open(url, '_blank');
      win.focus();
  });
  $('#google_map_client_btn').click(function(){
      url = "http://maps.google.com/maps?saddr=" + client_address + "&daddr="+ address;
      var win = window.open(url, '_blank');
      win.focus();
  });
});

// function plot_map(lat1,lng1,lat2,lng2){
//   map_modal = $('#map-modal');
//   height = map_modal.innerHeight();

//   $('#map-canvas').css('height',height/2);
//   initMap(lat1,lng1,lat2,lng2);
// }

// function initMap(lat1,lng1,lat2,lng2) {
//   var pointA = new google.maps.LatLng(lat1,lng1),
//     pointB = new google.maps.LatLng(lat2,lng2),
//     myOptions = {
//       zoom: 7,
//       center: pointA
//     },
//     map = new google.maps.Map(document.getElementById('map-canvas'), myOptions),
//     // Instantiate a directions service.
//     directionsService = new google.maps.DirectionsService,
//     directionsDisplay = new google.maps.DirectionsRenderer({
//       map: map
//     }),
//     markerA = new google.maps.Marker({
//       position: pointA,
//       title: "point A",
//       label: "A",
//       map: map
//     }),
//     markerB = new google.maps.Marker({
//       position: pointB,
//       title: "point B",
//       label: "B",
//       map: map
//     });

//   // get route from A to B
//   calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB);

// }

// function calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB) {
//   directionsService.route({
//     origin: pointA,
//     destination: pointB,
//     travelMode: google.maps.TravelMode.DRIVING
//   }, function(response, status) {
//     if (status == google.maps.DirectionsStatus.OK) {
//       directionsDisplay.setDirections(response);
//     } else {
//       window.alert('Directions request failed due to ' + status);
//     }
//   });
// }