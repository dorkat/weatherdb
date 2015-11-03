/**
 * Created by dor on 10/13/15.
 */

$(document).ready(function() {
    var request = new XMLHttpRequest;
    request.onreadystatechange = function () {
    var DONE = this.DONE || 4;
    if (this.readyState === DONE){
    console.log("city weather request ready");
    var city_weather = JSON.parse(request.responseText);
    chose_symbol(city_weather);
    console.log(city_weather.temp, city_weather.humidity, city_weather.clouds, city_weather.wind);
    console.log("city weather request done")
}
    };
    var host = "http://" + String($(location).attr('host')) + "/new_site/city_weather?name=Lapid&country=Israel";
    console.log(host);
    request.open("GET", host, true);
    request.send(null);
});

function chose_symbol(weather) {
    var symbol = document.getElementById("symbol");
    if (weather.clouds < 40 && weather.temp > 25 && weather.wind < 2) {
        symbol.setAttribute("class", "wi wi-day-sunny")
    }
    if (weather.clouds < 40 && weather.temp > 25 && weather.wind > 2) {
        symbol.setAttribute("class", "wi wi-day-windy")
    }
    if (weather.clouds > 40 && weather.temp > 25 && weather.wind < 2) {
        symbol.setAttribute("class", "wi wi-day-cloudy")
    }
    if (weather.clouds > 40 && weather.temp > 25 && weather.wind > 2) {
        symbol.setAttribute("class", "wi wi-day-cloudy-windy")
    }
}

$(document).ready(function() {
    var host = $(location).attr('host') + "/new_site/city_weather?name=Lapid&country=Israel";
    alert(host)
});