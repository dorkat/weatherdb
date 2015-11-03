/**
 * Created by dor on 10/15/15.
 */

$(document).ready(function(){
    var lat = geoplugin_latitude();
    var long = geoplugin_longitude();
    var mapProp = {
        center:new google.maps.LatLng(lat,long),
        zoom:14,
        mapTypeId:google.maps.MapTypeId.ROADMAP
  };
    var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
    var city = geoplugin_city();
    var marker = new google.maps.Marker({
        position:new google.maps.LatLng(lat,long),
        title: city
    });
marker.setMap(map);
});

$(document).ready(function() {
    var country = geoplugin_countryName();
    var city = geoplugin_city();
    $("#name").append("<option value='1' selected>"+country+"</option>");
    $("#name").append("<option value='2' selected>"+city+"</option>");

});