/**
 * Created by dor on 10/27/15.
 */

var geocoder;
var map;
var marker;
var host = "http://" + String($(location).attr('host'));

$(document).ready(function(){
    display_info(geoplugin_countryName(),geoplugin_city());
    display_on_map(geoplugin_latitude(),geoplugin_longitude());
    geocoder = new google.maps.Geocoder();
    document.getElementById("country_input").value = geoplugin_countryName();
    document.getElementById("city_input").value = geoplugin_city();
    city_list();
});

function display_on_map(lat, long){
    var mapProp = {
        center:new google.maps.LatLng(lat,long),
        zoom:13,
        mapTypeId:google.maps.MapTypeId.ROADMAP
  };
    map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
    var city = geoplugin_city();
    marker = new google.maps.Marker({
        position:new google.maps.LatLng(lat,long),
        title: city
    });
marker.setMap(map);
}

$(document).ready(function() {
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
    var DONE = this.DONE || 4;
    if (this.readyState === DONE){
    console.log("country list request ready");
    var country_list = request.responseText;
    country_list = country_list.substring(0, country_list.length -1);
    country_list = country_list.split(',');
    var options = "";
    for (i = 0; i < country_list.length; i++) {
        country_list[i] = country_list[i].substring(3, country_list[i].length-1);
        options += '<option value="'+country_list[i]+'" />';
    }
    document.getElementById('country').innerHTML = options;
    console.log("country list request done")
}
    };
    request.open("GET", host + "/new_site/country_list/", true);
    request.send(null);
});

$(document).ready(function() {
    document.getElementById("country_input").onchange = function () {
       city_list();
    };
});

function city_list(){
            if (document.getElementById("country").value == "") {city.options[city.options.length] = new Option("", "", false, false)
            }
            else {
                var country = document.getElementById("country_input").value;
                var request = new XMLHttpRequest;
                request.onreadystatechange = function () {
                    var DONE = this.DONE || 4;
                    if (this.readyState === DONE) {
                        console.log("city list request for " + country + " ready");
                        var city_list = request.responseText;
                        city_list = city_list.substring(0, city_list.length - 1);
                        city_list = city_list.split(',');
                        var options = "";
                        for (i = 0; i < city_list.length; i++) {
                            city_list[i] = city_list[i].substring(3, city_list[i].length - 1);
                            options += '<option value="'+city_list[i]+'" />';
                        }
                        document.getElementById('city').innerHTML = options;
                        console.log("city list request for " + country + " done")
                    }
                };
                var url = host + "/new_site/city_list/?name=" + country;
                request.open("GET", url, true);
                request.send(null);
            }
}

function display_info(country, city) {
    if (city) {
        $("#current_city").text(city + ":");
        var request = new XMLHttpRequest;
        request.onreadystatechange = function () {
            var DONE = this.DONE || 4;
            if (this.readyState === DONE) {
                console.log(city + " weather request ready");
                var city_weather = JSON.parse(request.responseText);
                chose_symbol(city_weather);
                console.log(city + " weather request done");
                $("#city_temp").text("temperature: " + city_weather.temp + "\xB0C");
                $("#city_humidity").text("humidity: " + city_weather.humidity + "%");
                $("#city_clouds").text("cloud coverage: " + city_weather.clouds + "%");
                $("#city_wind").text("wind speed: " + city_weather.wind + "m/s");
            }
        };
        var url = host + "/new_site/city_weather?name=" + city + "&country=" + country;
        request.open("GET", url, true);
        request.send(null);
    }
    else {
        $("#city_temp").text("unable to find city, please choose from the list");
        $("#city_humidity").text("");
        $("#city_clouds").text("");
        $("#city_wind").text("");
    }

    var second_request = new XMLHttpRequest;
    if (country) {
        second_request.onreadystatechange = function () {
            var DONE = this.DONE || 4;
            if (this.readyState === DONE) {
                console.log(country + " info request ready");
                var country_stats = JSON.parse(second_request.responseText);
                console.log(country + " info request done");
                var info = "hottest city: " + country_stats.hottest + " temp: " + country_stats.hottest_temp;
                $("#country_info_header").text("Some information about " + country);
                $("#country_hottest").text("The hottest city is " + country_stats.hottest + " at " + country_stats.hottest_temp + "\xB0C");
                $("#country_coldest").text("The coldest city is " + country_stats.coldest + " at " + country_stats.coldest_temp + "\xB0C");
                $("#country_average").text("The average temperature is " + country_stats.average_temp + "\xB0C");
            }
        };
        var second_url = host + "/new_site/country_info?name=" + country;
        second_request.open("GET", second_url, true);
        second_request.send(null);
    }
    else {
        $("#country_info_header").text("unable to find country, please choose from the list");
        $("#country_hottest").text("");
        $("#country_coldest").text("");
        $("#country_average").text("");
    }
}

function chose_symbol(weather) {
    var symbol = document.getElementById("symbol");
    if (weather.clouds < 40 && weather.temp > 25 && weather.wind < 3) {
        symbol.setAttribute("class", "wi wi-day-sunny")
    }
    if (weather.clouds < 40 && weather.temp > 25 && weather.wind > 3) {
        symbol.setAttribute("class", "wi wi-day-windy")
    }
    if (weather.clouds > 40 && weather.temp > 25 && weather.wind < 3) {
        symbol.setAttribute("class", "wi wi-day-cloudy")
    }
    if (weather.clouds > 40 && weather.temp > 25 && weather.wind > 3) {
        symbol.setAttribute("class", "wi wi-day-cloudy-windy")
    }
}

function center_map(country, city) {
    var address = city + ',' + country;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        marker.setMap(null);
        marker = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location,
            title: city
        });
      } else {
        alert("Geocode failed because: " + status);
      }
    });
}

$(document).ready(function() {
    $("#change_city_button").click(function(){
        var country = document.getElementById("country_input").value;
        var city = document.getElementById("city_input").value;
        display_info(country, city);
        center_map(country, city);
    });
});

$(document).ready(function() {
var months = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
var days= ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

var newDate = new Date();
newDate.setDate(newDate.getDate());
$('#Date').html(days[newDate.getDay()] + " " + newDate.getDate() + ' ' + months[newDate.getMonth()] + ' ' + newDate.getFullYear());

setInterval( function() {
	var seconds = new Date().getSeconds();
	$("#sec").html(( seconds < 10 ? "0" : "" ) + seconds);
	},1000);

setInterval( function() {
	var minutes = new Date().getMinutes();
	$("#min").html(( minutes < 10 ? "0" : "" ) + minutes);
    },1000);

setInterval( function() {
	var hours = new Date().getHours();
	$("#hours").html(( hours < 10 ? "0" : "" ) + hours);
    }, 1000);
});

$(document).ready(function(){
   $("#sat24_link").click(function(){
       window.open("http://en.sat24.com/en");
   });
});

$(document).ready(function(){
   $("#wind_link").click(function(){
       window.open("http://www.windfinder.com/");
   });
});

$(document).ready(function(){
   $("#rain_link").click(function(){
       window.open("http://www.ims.gov.il/IMSEng/Tazpiot/RainRadar.htm");
   });
});

$(document).ready(function(){
    map.addListener('click', function(event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        console.log( latitude + ', ' + longitude );
        try {
            var url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude;
            var request = new XMLHttpRequest;
            request.onreadystatechange = function () {
                var DONE = this.DONE || 4;
                if (this.readyState === DONE) {
                    var result = JSON.parse(request.responseText);
                    var city = result["results"][1]["address_components"][1]["long_name"];
                    var country = result["results"][1]["address_components"][1]["long_name"];
                    console.log(city);
                    console.log(country);
                    display_info(country, city);
                    display_on_map(latitude, longitude);
                }
            };
            request.open("GET", url, true);
            request.send(null);
        }
        catch(err) {
            console.log("no city")
        }
    });
});
