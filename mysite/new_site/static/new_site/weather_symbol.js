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
    console.log("country list request done")
}
    };
    request.open("GET", "http://192.168.200.128:8000/new_site/city_weather?name=Lapid&country=Israel", true);
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